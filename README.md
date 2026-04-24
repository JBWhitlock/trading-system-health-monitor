# AI-Enhanced Infrastructure Monitor

A lightweight Python-based monitoring tool designed to validate system health across CPU, memory, services, and network endpoints — enhanced with an AI-style analysis engine for operational risk detection and intelligent reporting.

---

## 🚀 Overview

This tool simulates real-world enterprise monitoring workflows by combining:

- System health checks (CPU, memory, services)
- Endpoint availability validation with retry logic
- Structured logging
- AI-assisted operational analysis (risk scoring, correlation, recommendations)

Built to reflect production-grade thinking around reliability, observability, and security.

---

## 🧠 AI-Enhanced Analysis

Includes a deterministic AI-style analysis engine that:

- Assigns **risk scores** based on system health signals  
- Performs **correlation analysis** (e.g., service failures + endpoint failures)  
- Reduces **false positives** using retry logic and thresholds  
- Generates **executive summaries** and actionable recommendations  
- Outputs structured **JSON reports** for integration with dashboards or SIEM tools  

> Designed as a foundation for future integration with:
> - Azure OpenAI  
> - AWS Bedrock  
> - OpenAI API  

---

## 📁 Project Structure

```
ResourceMonitor/
├── monitor.py
├── config.yaml
├── ai/
│   ├── __init__.py
│   ├── analyzer.py
│   └── prompts.py
├── logs/
├── reports/
└── README.md
```

---

## ⚙️ Features

- CPU and memory monitoring with thresholds  
- Windows service health validation  
- HTTP/S endpoint monitoring with retries and latency tracking  
- Structured logging to file  
- AI-style analysis with:
  - Risk scoring  
  - Root-cause hints  
  - Recommended actions  
- JSON report generation  

---

## 🛠️ Installation

```
pip install psutil requests pyyaml
```

---

## ▶️ Usage

```
python monitor.py
```

Stop with:

```
Ctrl + C
```

---

## 📊 Sample Output

```
AI-Enhanced Operational Analysis
--------------------------------
3 finding(s) detected with an overall Medium risk level.
Risk Level: Medium
Risk Score: 45

- High memory utilization detected: 89%
- Service issue detected: Spooler is stopped
- Endpoint failure detected after retries: https://example.com
```

---

## 📄 Sample Report (JSON)

```json
{
  "risk_score": 45,
  "risk_level": "Medium",
  "findings": [
    "High memory utilization detected",
    "Service issue detected",
    "Endpoint failure detected"
  ],
  "recommendations": [
    "Check memory usage and running processes",
    "Restart service and validate dependencies",
    "Validate DNS/firewall/network path"
  ]
}
```

---

## 🎯 Purpose

This project demonstrates:

- Automation-driven infrastructure monitoring  
- Practical application of AI concepts to operations and security  
- Structured data analysis and reporting  
- Production-style system design and extensibility  

---

## 🔮 Roadmap

- Integration with LLMs for advanced analysis  
- Historical trend analysis and anomaly detection  
- Dashboard visualization (Grafana / web UI)  
- SIEM integration  
- Multi-node monitoring support  

---

## 👤 Author

James Whitlock  
Enterprise Architect | Systems & Security Engineering  
https://www.linkedin.com/in/jbwhitlock/
