# services/tuner.py
from typing import Dict, Any

def suggest_hyperparams(rows:int, features:int, task:str="classification"):
    """
    Very simple heuristic tuner. Expand later with Bayesian/Optuna etc.
    """
    # base suggestions
    params = {
        "lr": 1e-3,
        "batch_size": 32,
        "epochs": 10,
        "hidden_layers": [max(64, features*2), 64]  # two-layer heuristic
    }
    # adjust for dataset size
    if rows > 50000:
        params["lr"] = 5e-4
        params["batch_size"] = 128
        params["epochs"] = 6
    elif rows > 10000:
        params["lr"] = 8e-4
        params["batch_size"] = 64
        params["epochs"] = 8
    # task-specific tweaks
    if task == "regression":
        params["loss"] = "mse"
    else:
        params["loss"] = "crossentropy"
    return params
