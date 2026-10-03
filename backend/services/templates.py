# services/templates.py
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TemplateInfo:
    id: str
    name: str
    kind: str  # tabular|image|text
    task: str  # classification|regression
    default_params: Dict[str, Any]
    # an approximate samples/sec baseline for ETA (adjust to your box)
    throughput_samples_per_sec: float

TEMPLATES: Dict[str, TemplateInfo] = {
    "tabular_mlp_classification": TemplateInfo(
        id="tabular_mlp_classification",
        name="Tabular MLP (Classification)",
        kind="tabular",
        task="classification",
        default_params={"epochs": 15, "batch_size": 64, "lr": 1e-3, "hidden": [128, 64]},
        throughput_samples_per_sec=32000.0,  # rough CPU baseline, tweak
    ),
    "tabular_mlp_regression": TemplateInfo(
        id="tabular_mlp_regression",
        name="Tabular MLP (Regression)",
        kind="tabular",
        task="regression",
        default_params={"epochs": 20, "batch_size": 64, "lr": 1e-3, "hidden": [128, 64]},
        throughput_samples_per_sec=32000.0,
    ),
    "image_cnn_classification": TemplateInfo(
        id="image_cnn_classification",
        name="Image CNN (Classification)",
        kind="image",
        task="classification",
        default_params={"epochs": 10, "batch_size": 32, "lr": 1e-3},
        throughput_samples_per_sec=512.0,  # images/sec baseline
    ),
    "text_lstm_classification": TemplateInfo(
        id="text_lstm_classification",
        name="Text LSTM (Classification)",
        kind="text",
        task="classification",
        default_params={"epochs": 6, "batch_size": 64, "lr": 2e-3},
        throughput_samples_per_sec=4000.0,
    ),
}
