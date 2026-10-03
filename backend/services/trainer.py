# services/trainer.py
import os, time, json, threading, uuid
from typing import Dict, Any, Optional, Tuple
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
from .data_io import load_tabular_csv
from .templates import TEMPLATES, TemplateInfo

MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# In-memory job store (for demo). Replace with Redis/DB in prod.
JOBS: Dict[str, Dict[str, Any]] = {}

def _estimate_eta(samples: int, params: Dict[str, Any], tpl: TemplateInfo) -> float:
    epochs = int(params.get("epochs", tpl.default_params["epochs"]))
    # crude: total samples processed ~ epochs * samples; divide by throughput
    return max(1.0, (epochs * samples) / max(1.0, tpl.throughput_samples_per_sec))

# Simple MLP for tabular
class MLP(nn.Module):
    def __init__(self, in_features: int, hidden: list, out_dim: int, task: str):
        super().__init__()
        layers = []
        last = in_features
        for h in hidden:
            layers += [nn.Linear(last, h), nn.ReLU(), nn.Dropout(0.1)]
            last = h
        layers.append(nn.Linear(last, out_dim))
        self.net = nn.Sequential(*layers)
        self.task = task

    def forward(self, x):
        return self.net(x)

def _prepare_tabular_dataloaders(X, y, batch_size: int, task: str):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder

    # scale numeric
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X.values.astype(np.float32))

    # encode y for classification
    y_arr = y.values
    label_encoder = None
    if task == "classification":
        if y.dtype == object or len(np.unique(y_arr)) <= 50:
            label_encoder = LabelEncoder()
            y_arr = label_encoder.fit_transform(y_arr)
    y_arr = y_arr.astype(np.float32 if task == "regression" else np.int64)

    X_train, X_val, y_train, y_val = train_test_split(Xs, y_arr, test_size=0.2, random_state=42, stratify=(y_arr if task=="classification" else None))
    tr_ds = TensorDataset(torch.tensor(X_train, dtype=torch.float32),
                          torch.tensor(y_train))
    va_ds = TensorDataset(torch.tensor(X_val, dtype=torch.float32),
                          torch.tensor(y_val))
    tr_dl = DataLoader(tr_ds, batch_size=batch_size, shuffle=True)
    va_dl = DataLoader(va_ds, batch_size=batch_size, shuffle=False)
    meta = {"scaler_mean": scaler.mean_.tolist(), "scaler_scale": scaler.scale_.tolist()}
    if label_encoder:
        meta["label_classes"] = list(label_encoder.classes_)
    return tr_dl, va_dl, meta

def _train_tabular_mlp(job: Dict[str, Any]):
    # unpack config
    job_id = job["job_id"]
    path = job["dataset_path"]
    target = job["target_col"]
    params = job["params"]
    tpl = job["template"]
    task = tpl.task
    epochs = int(params["epochs"])
    batch_size = int(params["batch_size"])
    lr = float(params["lr"])
    hidden = list(map(int, params["hidden"]))

    try:
        X, y = load_tabular_csv(path, target)
        in_features = X.shape[1]
        # out dim
        if task == "classification":
            num_classes = int(np.unique(y).shape[0])
            out_dim = num_classes
            criterion = nn.CrossEntropyLoss()
        else:
            out_dim = 1
            criterion = nn.MSELoss()

        tr_dl, va_dl, enc_meta = _prepare_tabular_dataloaders(X, y, batch_size, task)
        model = MLP(in_features, hidden, out_dim, task)
        opt = torch.optim.Adam(model.parameters(), lr=lr)

        # train loop
        total_steps = epochs * len(tr_dl)
        step_done = 0
        best_val = None
        history = {"epoch": [], "train_loss": [], "val_loss": [], "val_metric": []}

        for epoch in range(1, epochs+1):
            model.train()
            running = 0.0
            for xb, yb in tr_dl:
                opt.zero_grad()
                out = model(xb)
                if task == "classification":
                    loss = criterion(out, yb)
                else:
                    loss = criterion(out.squeeze(-1), yb.float())
                loss.backward()
                opt.step()
                running += loss.item()
                step_done += 1

            train_loss = running / max(1, len(tr_dl))

            # validate
            model.eval()
            val_loss, correct, total = 0.0, 0, 0
            with torch.no_grad():
                for xb, yb in va_dl:
                    out = model(xb)
                    if task == "classification":
                        loss = criterion(out, yb)
                        preds = out.argmax(dim=1)
                        correct += (preds == yb).sum().item()
                        total += yb.numel()
                    else:
                        loss = criterion(out.squeeze(-1), yb.float())
                    val_loss += loss.item()
            val_loss /= max(1, len(va_dl))
            if task == "classification":
                val_metric = correct / max(1, total)
            else:
                val_metric = float(val_loss)  # or use RMSE later

            history["epoch"].append(epoch)
            history["train_loss"].append(float(train_loss))
            history["val_loss"].append(float(val_loss))
            history["val_metric"].append(float(val_metric))

            # update job status
            JOBS[job_id]["progress"] = round(step_done / max(1, total_steps), 4)
            JOBS[job_id]["status"] = "running"
            JOBS[job_id]["message"] = f"Epoch {epoch}/{epochs}"
            JOBS[job_id]["history"] = history

            if best_val is None or val_loss < best_val:
                best_val = val_loss
                # save checkpoint
                torch.save(model.state_dict(), os.path.join(MODELS_DIR, f"{job_id}.pt"))
                # save simple meta for inference
                meta = {
                    "in_features": in_features,
                    "task": task,
                    "hidden": hidden,
                    "out_dim": out_dim,
                    **enc_meta
                }
                with open(os.path.join(MODELS_DIR, f"{job_id}.json"), "w") as f:
                    json.dump(meta, f)

        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["eta_seconds"] = 0
        JOBS[job_id]["message"] = "Training complete"
        JOBS[job_id]["metrics"] = {
            "final_val_loss": history["val_loss"][-1],
            "final_val_metric": history["val_metric"][-1],
            "metric_name": "accuracy" if task == "classification" else "val_loss"
        }

    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["message"] = str(e)

def start_training_job(dataset_path: str, template_id: str, target_col: str, user_params: Dict[str, Any]) -> Tuple[str, float]:
    if template_id not in TEMPLATES:
        raise ValueError(f"Unknown template '{template_id}'")
    tpl = TEMPLATES[template_id]
    params = {**tpl.default_params, **(user_params or {})}
    # crude ETA
    try:
        import pandas as pd
        samples = pd.read_csv(dataset_path, nrows=0).shape[0]  # header only (0). We need full rows:
        # do a cheap count without loading all:
        samples = sum(1 for _ in open(dataset_path, "rb")) - 1
        if samples < 1: samples = 1000  # fallback
    except Exception:
        samples = 1000
    eta = _estimate_eta(samples, params, tpl)

    job_id = uuid.uuid4().hex
    JOBS[job_id] = {
        "job_id": job_id,
        "template_id": template_id,
        "template": tpl,
        "dataset_path": dataset_path,
        "target_col": target_col,
        "params": params,
        "status": "queued",
        "progress": 0.0,
        "eta_seconds": round(eta, 1),
        "message": "Queued",
        "history": None,
        "metrics": None
    }

    # spawn thread
    def _runner():
        JOBS[job_id]["status"] = "starting"
        JOBS[job_id]["message"] = "Initializing…"
        t0 = time.time()
        if tpl.kind == "tabular":
            _train_tabular_mlp(JOBS[job_id])
        else:
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["message"] = f"Template '{tpl.id}' not implemented yet."
        # adjust ETA to zero when done
        JOBS[job_id]["eta_seconds"] = max(0, round(eta - (time.time() - t0), 1))

    threading.Thread(target=_runner, daemon=True).start()
    return job_id, eta

def get_status(job_id: str) -> Optional[Dict[str, Any]]:
    job = JOBS.get(job_id)
    if not job: return None
    # simple decreasing ETA while running (purely cosmetic)
    if job["status"] in ("starting", "running") and job["eta_seconds"] > 0:
        job["eta_seconds"] = max(0, round(job["eta_seconds"] - 0.5, 1))
    # return a shallow copy without the template object (not JSON serializable)
    j = {k: v for k, v in job.items() if k != "template"}
    j["template_name"] = job["template"].name
    return j
