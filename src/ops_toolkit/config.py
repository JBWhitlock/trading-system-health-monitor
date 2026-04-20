from pathlib import Path
import yaml


REQUIRED_KEYS = ["cpu_threshold", "memory_threshold", "services", "endpoints"]


def load_config(config_path: str = "config/config.yaml") -> dict:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config:
        raise ValueError(f"Config file is empty or invalid: {path}")

    for key in REQUIRED_KEYS:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    if not isinstance(config["services"], list):
        raise ValueError("'services' must be a list")

    if not isinstance(config["endpoints"], list):
        raise ValueError("'endpoints' must be a list")

    config.setdefault("interval_seconds", 30)

    return config