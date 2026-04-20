import psutil


def check_services(services: list[str]) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []

    for service in services:
        try:
            svc = psutil.win_service_get(service)
            status = svc.as_dict()["status"]

            if status.lower() != "running":
                results.append(("ALERT", f"Service '{service}' is {status}"))
            else:
                results.append(("INFO", f"Service OK: {service}"))

        except Exception as exc:
            results.append(("ERROR", f"Failed to check service '{service}': {exc}"))

    return results