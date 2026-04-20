import time

from ops_toolkit.config import load_config
from ops_toolkit.logger import log
from ops_toolkit.checks.cpu import check_cpu
from ops_toolkit.checks.memory import check_memory
from ops_toolkit.checks.windows_services import check_services
from ops_toolkit.checks.endpoints import check_endpoints


def run_checks(config_path: str = "config/config.yaml") -> None:
    config = load_config(config_path)

    log("INFO", "---- Running Health Checks ----")

    level, message = check_cpu(config["cpu_threshold"])
    log(level, message)

    level, message = check_memory(config["memory_threshold"])
    log(level, message)

    for level, message in check_services(config["services"]):
        log(level, message)

    for level, message in check_endpoints(config["endpoints"]):
        log(level, message)


def run_loop(config_path: str = "config/config.yaml") -> None:
    config = load_config(config_path)
    interval = config.get("interval_seconds", 30)

    log("INFO", "Ops Toolkit started")

    try:
        while True:
            run_checks(config_path)
            time.sleep(interval)
    except KeyboardInterrupt:
        log("INFO", "Ops Toolkit stopped by user")
    except Exception as exc:
        log("ERROR", f"Unhandled runtime error: {exc}")
        raise