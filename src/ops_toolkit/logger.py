from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "monitor.log"


def log(level: str, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level.upper()}] {message}"
    print(entry)

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(entry + "\n")