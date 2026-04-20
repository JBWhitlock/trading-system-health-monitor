import psutil


def check_cpu(threshold: int) -> tuple[str, str]:
    cpu = psutil.cpu_percent(interval=1)

    if cpu > threshold:
        return "ALERT", f"CPU usage high: {cpu}% (threshold: {threshold}%)"

    return "INFO", f"CPU OK: {cpu}% (threshold: {threshold}%)"