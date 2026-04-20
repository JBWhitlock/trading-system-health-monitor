# Ops Toolkit (Trading System Health Monitor)

Python-based operations reliability toolkit for monitoring system health, Windows services, and endpoint availability in production environments.

Originally designed for trading systems, but built to be reusable across enterprise workloads.

---

## Core Capabilities

- CPU & memory threshold monitoring  
- Windows service health validation  
- Endpoint availability & latency checks (with retry logic)  
- Config-driven execution (YAML)  
- Structured logging  
- CLI-based operation (no manual script execution)  
- Modular architecture for extension  

---

## Why This Exists

Most environments rely on:
- ad hoc scripts  
- fragmented monitoring  
- slow manual troubleshooting  

This toolkit provides:
- fast health visibility  
- consistent checks  
- extensible foundation for automation and remediation  

---

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

---

## Usage

Run continuous monitoring:

```bash
ops-toolkit run
```

Run a single health check pass:

```bash
ops-toolkit check-now
```

Validate configuration:

```bash
ops-toolkit test-config
```

---

## Configuration

Edit:

config/config.yaml

Example:

```yaml
cpu_threshold: 85
memory_threshold: 90
interval_seconds: 30

services:
  - Spooler
  - W32Time

endpoints:
  - name: Google
    url: https://www.google.com
    timeout: 2
  - name: Dummy API
    url: https://dummy-api.local/health
    timeout: 2
```

---

## Example Output

```text
[INFO] ---- Running Health Checks ----
[INFO] CPU OK: 23%
[INFO] Memory OK: 51%
[INFO] Service OK: Spooler
[ALERT] Endpoint failure: Dummy API (timeout after retries)
```

---

## Project Structure

```text
src/ops_toolkit/
  cli.py
  main.py
  config.py
  logger.py
  checks/
    cpu.py
    memory.py
    windows_services.py
    endpoints.py
```

---

## Roadmap

- Windows service installation mode  
- Auto-remediation (restart services, retry endpoints)  
- Local dashboard (Flask-based)  
- Alerting integrations (email / webhook)  

---

## Positioning

This is not a toy monitor.

It is a foundation for:
- production operations tooling  
- reliability engineering workflows  
- automated incident detection  

---
## Output (Example)
$ ops-toolkit run
[2026-04-20 13:24:15] [INFO] Ops Toolkit started
[2026-04-20 13:24:15] [INFO] ---- Running Health Checks ----
[2026-04-20 13:24:16] [INFO] CPU OK: 3.1% (threshold: 85%)
[2026-04-20 13:24:16] [INFO] Memory OK: 50.8% (threshold: 90%)
[2026-04-20 13:24:16] [INFO] Service OK: Spooler
[2026-04-20 13:24:16] [INFO] Service OK: W32Time
[2026-04-20 13:24:25] [INFO] Google OK (438.83 ms) on attempt 1
[2026-04-20 13:24:25] [WARNING] Dummy API failed on attempt 1: HTTPSConnectionPool(host='dummy-api.local', port=443): Max retries exceeded with url: /health (Caused by NameResolutionError("HTTPSConnection(host='dummy-api.local', port=443): Failed to resolve 'dummy-api.local' ([Errno 11001] getaddrinfo failed)"))
[2026-04-20 13:24:25] [WARNING] Dummy API failed on attempt 2: HTTPSConnectionPool(host='dummy-api.local', port=443): Max retries exceeded with url: /health (Caused by NameResolutionError("HTTPSConnection(host='dummy-api.local', port=443): Failed to resolve 'dummy-api.local' ([Errno 11001] getaddrinfo failed)"))
[2026-04-20 13:24:25] [WARNING] Dummy API failed on attempt 3: HTTPSConnectionPool(host='dummy-api.local', port=443): Max retries exceeded with url: /health (Caused by NameResolutionError("HTTPSConnection(host='dummy-api.local', port=443): Failed to resolve 'dummy-api.local' ([Errno 11001] getaddrinfo failed)"))
[2026-04-20 13:24:25] [ALERT] Dummy API failed after 3 attempts
[2026-04-20 13:24:55] [INFO] ---- Running Health Checks ----
[2026-04-20 13:24:56] [INFO] CPU OK: 2.5% (threshold: 85%)
[2026-04-20 13:24:56] [INFO] Memory OK: 51.5% (threshold: 90%)
[2026-04-20 13:24:56] [INFO] Service OK: Spooler
[2026-04-20 13:24:56] [INFO] Service OK: W32Time
[2026-04-20 13:25:04] [INFO] Google OK (433.95 ms) on attempt 1
[2026-04-20 13:25:04] [WARNING] Dummy API failed on attempt 1: HTTPSConnectionPool(host='dummy-api.local', port=443): Max retries exceeded with url: /health (Caused by NameResolutionError("HTTPSConnection(host='dummy-api.local', port=443): Failed to resolve 'dummy-api.local' ([Errno 11001] getaddrinfo failed)"))
[2026-04-20 13:25:04] [WARNING] Dummy API failed on attempt 2: HTTPSConnectionPool(host='dummy-api.local', port=443): Max retries exceeded with url: /health (Caused by NameResolutionError("HTTPSConnection(host='dummy-api.local', port=443): Failed to resolve 'dummy-api.local' ([Errno 11001] getaddrinfo failed)"))
[2026-04-20 13:25:04] [WARNING] Dummy API failed on attempt 3: HTTPSConnectionPool(host='dummy-api.local', port=443): Max retries exceeded with url: /health (Caused by NameResolutionError("HTTPSConnection(host='dummy-api.local', port=443): Failed to resolve 'dummy-api.local' ([Errno 11001] getaddrinfo failed)"))
[2026-04-20 13:25:04] [ALERT] Dummy API failed after 3 attempts
