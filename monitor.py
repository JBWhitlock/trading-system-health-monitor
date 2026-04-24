import os
import time
from datetime import datetime

import psutil
import requests
import yaml

from ai.analyzer import AIEnhancedAnalyzer, save_ai_report

CONFIG_FILE = "config.yaml"
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "monitor.log")
REQUIRED_KEYS = ["cpu_threshold", "memory_threshold", "services", "endpoints"]


# ---------------------------
# CONFIG
# ---------------------------
def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config:
        raise ValueError(f"{CONFIG_FILE} is empty or invalid.")

    for key in REQUIRED_KEYS:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    return config


# ---------------------------
# LOGGING
# ---------------------------
def log(level, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {msg}"
    print(entry)

    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


# ---------------------------
# CHECKS (RETURN DATA)
# ---------------------------
def check_cpu(threshold):
    cpu = psutil.cpu_percent(interval=1)

    status = "ok"
    if cpu > threshold:
        status = "alert"
        log("ALERT", f"CPU usage high: {cpu}% (threshold: {threshold}%)")
    else:
        log("INFO", f"CPU OK: {cpu}%")

    return {
        "cpu_percent": cpu,
        "status": status
    }


def check_memory(threshold):
    mem = psutil.virtual_memory().percent

    status = "ok"
    if mem > threshold:
        status = "alert"
        log("ALERT", f"Memory usage high: {mem}% (threshold: {threshold}%)")
    else:
        log("INFO", f"Memory OK: {mem}%")

    return {
        "memory_percent": mem,
        "status": status
    }


def check_services(services):
    results = []

    for service in services:
        try:
            svc = psutil.win_service_get(service)
            status = svc.as_dict()["status"]

            if status.lower() != "running":
                log("ALERT", f"Service '{service}' is {status}")
                state = "alert"
            else:
                log("INFO", f"Service OK: {service}")
                state = "ok"

            results.append({
                "name": service,
                "status": state
            })

        except Exception as e:
            log("ERROR", f"Failed to check service '{service}': {e}")
            results.append({
                "name": service,
                "status": "error"
            })

    return results


def check_endpoints(endpoints, retries=3):
    results = []

    for ep in endpoints:
        name = ep.get("name", "Unnamed Endpoint")
        url = ep.get("url")
        timeout = ep.get("timeout", 2)

        success = False

        for attempt in range(1, retries + 1):
            try:
                start = time.time()
                response = requests.get(url, timeout=timeout)
                latency = (time.time() - start) * 1000

                if response.status_code == 200:
                    log("INFO", f"{name} OK ({latency:.2f} ms)")
                    success = True
                    break
                else:
                    log("WARNING", f"{name} HTTP {response.status_code}")

            except Exception as e:
                log("WARNING", f"{name} failed attempt {attempt}: {e}")

        results.append({
            "url": url,
            "status": "reachable" if success else "failed",
            "attempts": retries
        })

    return results


# ---------------------------
# MAIN LOOP
# ---------------------------
def main():
    try:
        config = load_config()
    except Exception as e:
        print(f"Startup error: {e}")
        return

    interval = config.get("interval_seconds", 30)

    log("INFO", "Monitor started")

    while True:
        log("INFO", "---- Running Health Checks ----")

        cpu_result = check_cpu(config["cpu_threshold"])
        memory_result = check_memory(config["memory_threshold"])
        service_results = check_services(config["services"])
        endpoint_results = check_endpoints(config["endpoints"])

        # 🔥 THIS is where AI belongs
        health_data = {
            "cpu_percent": cpu_result["cpu_percent"],
            "memory_percent": memory_result["memory_percent"],
            "services": service_results,
            "endpoints": endpoint_results
        }

        analyzer = AIEnhancedAnalyzer(health_data)
        ai_report = analyzer.analyze()
        save_ai_report(ai_report)

        print("\nAI-Enhanced Operational Analysis")
        print("--------------------------------")
        print(ai_report["executive_summary"])
        print(f"Risk Level: {ai_report['risk_level']}")
        print(f"Risk Score: {ai_report['risk_score']}")

        for finding in ai_report["findings"]:
            print(f"- {finding}")

        time.sleep(interval)


if __name__ == "__main__":
    main()