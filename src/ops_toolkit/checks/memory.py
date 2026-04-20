import psutil


def check_memory(threshold: int) -> tuple[str, str]:
    memory = psutil.virtual_memory().percent

    if memory > threshold:
        return "ALERT", f"Memory usage high: {memory}% (threshold: {threshold}%)"

    return "INFO", f"Memory OK: {memory}% (threshold: {threshold}%)"