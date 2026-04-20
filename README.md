# Trading System Health Monitor (TSHM)

Lightweight Python-based monitoring tool designed for production trading environments.

## Features
- CPU / Memory monitoring
- Windows service health checks
- Endpoint latency & availability monitoring
- Config-driven architecture
- Extensible modular design

## Use Case
Designed for environments requiring high uptime and rapid incident detection, such as trading platforms and real-time systems.

## Tech Stack
- Python
- psutil
- requests
- YAML config

- ## Installation

pip install psutil requests pyyaml

## Configuration

Example `config.yaml`:

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
