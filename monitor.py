import os
import time
from datetime import datetime

import psutil
import requests
import yaml


CONFIG_FILE = "config.yaml"
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "monitor.log")
REQUIRED_KEYS = ["cpu_threshold", "memory_threshold", "services", "endpoints"]


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config:
        raise ValueError(f"{CONFIG_FILE} is empty or invalid.")

    for key in REQUIRED_KEYS:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    if not isinstance(config["services"], list):
        raise ValueError("'services' must be a list.")

    if not isinstance(config["endpoints"], list):
        raise ValueError("'endpoints' must be a list.")

    return config


def log(level, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {msg}"
    print(entry)

    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def check_cpu(threshold):
    cpu = psutil.cpu_percent(interval=1)
    if cpu > threshold:
        log("ALERT", f"CPU usage high: {cpu}% (threshold: {threshold}%)")
    else:
        log("INFO", f"CPU OK: {cpu}% (threshold: {threshold}%)")


def check_memory(threshold):
    mem = psutil.virtual_memory().percent
    if mem > threshold:
        log("ALERT", f"Memory usage high: {mem}% (threshold: {threshold}%)")
    else:
        log("INFO", f"Memory OK: {mem}% (threshold: {threshold}%)")


def check_services(services):
    for service in services:
        try:
            svc = psutil.win_service_get(service)
            status = svc.as_dict()["status"]

            if status.lower() != "running":
                log("ALERT", f"Service '{service}' is {status}")
            else:
                log("INFO", f"Service OK: {service}")
        except Exception as e:
            log("ERROR", f"Failed to check service '{service}': {e}")


def check_endpoints(endpoints, retries=3):
    for ep in endpoints:
        name = ep.get("name", "Unnamed Endpoint")
        url = ep.get("url")
        timeout = ep.get("timeout", 2)

        if not url:
            log("ERROR", f"Endpoint '{name}' is missing a URL")
            continue

        success = False

        for attempt in range(1, retries + 1):
            try:
                start = time.time()
                response = requests.get(url, timeout=timeout)
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    log(
                        "INFO",
                        f"{name} OK ({latency:.2f} ms) on attempt {attempt}"
                    )
                    success = True
                    break
                else:
                    log(
                        "WARNING",
                        f"{name} returned HTTP {response.status_code} on attempt {attempt}"
                    )

            except requests.exceptions.RequestException as e:
                log("WARNING", f"{name} failed on attempt {attempt}: {e}")

        if not success:
            log("ALERT", f"{name} failed after {retries} attempts")


def main():
    try:
        config = load_config()
    except Exception as e:
        print(f"Startup error: {e}")
        return

    interval = config.get("interval_seconds", 30)

    log("INFO", "Resource monitor started")

    try:
        while True:
            log("INFO", "---- Running Health Checks ----")
            check_cpu(config["cpu_threshold"])
            check_memory(config["memory_threshold"])
            check_services(config["services"])
            check_endpoints(config["endpoints"])
            time.sleep(interval)

    except KeyboardInterrupt:
        log("INFO", "Resource monitor stopped by user")
    except Exception as e:
        log("ERROR", f"Unhandled runtime error: {e}")


if __name__ == "__main__":
    main()