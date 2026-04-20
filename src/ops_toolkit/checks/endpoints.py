import time
import requests


def check_endpoints(endpoints: list[dict], retries: int = 3) -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []

    for endpoint in endpoints:
        name = endpoint.get("name", "Unnamed Endpoint")
        url = endpoint.get("url")
        timeout = endpoint.get("timeout", 2)

        if not url:
            results.append(("ERROR", f"Endpoint '{name}' is missing a URL"))
            continue

        success = False

        for attempt in range(1, retries + 1):
            try:
                start = time.time()
                response = requests.get(url, timeout=timeout)
                latency_ms = (time.time() - start) * 1000

                if response.status_code == 200:
                    results.append(
                        ("INFO", f"{name} OK ({latency_ms:.2f} ms) on attempt {attempt}")
                    )
                    success = True
                    break

                results.append(
                    ("WARNING", f"{name} returned HTTP {response.status_code} on attempt {attempt}")
                )

            except requests.exceptions.RequestException as exc:
                results.append(("WARNING", f"{name} failed on attempt {attempt}: {exc}"))

        if not success:
            results.append(("ALERT", f"{name} failed after {retries} attempts"))

    return results