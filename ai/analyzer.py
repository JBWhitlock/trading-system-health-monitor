import json
from datetime import datetime


class AIEnhancedAnalyzer:
    """
    AI-ready analysis layer for infrastructure health data.

    This version does not require an external LLM API.
    It produces deterministic AI-style operational analysis that can later
    be upgraded to OpenAI, Azure OpenAI, Bedrock, or local LLMs.
    """

    def __init__(self, health_data: dict):
        self.health_data = health_data
        self.findings = []
        self.recommendations = []
        self.risk_score = 0

    def analyze(self) -> dict:
        self._analyze_cpu()
        self._analyze_memory()
        self._analyze_services()
        self._analyze_endpoints()
        self._correlate_findings()

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "risk_score": self.risk_score,
            "risk_level": self._risk_level(),
            "findings": self.findings,
            "recommendations": self.recommendations,
            "executive_summary": self._executive_summary(),
            "raw_health_data": self.health_data,
        }

    def _analyze_cpu(self):
        cpu = self.health_data.get("cpu_percent")
        if cpu is not None and cpu >= 85:
            self.risk_score += 20
            self.findings.append(f"High CPU utilization detected: {cpu}%")
            self.recommendations.append("Review active processes and recent workload changes.")

    def _analyze_memory(self):
        memory = self.health_data.get("memory_percent")
        if memory is not None and memory >= 85:
            self.risk_score += 20
            self.findings.append(f"High memory utilization detected: {memory}%")
            self.recommendations.append("Check for memory leaks, runaway services, or capacity pressure.")

    def _analyze_services(self):
        services = self.health_data.get("services", [])

        for service in services:
            name = service.get("name")
            status = service.get("status")

            if status and status.lower() not in ["running", "ok"]:
                self.risk_score += 25
                self.findings.append(f"Service issue detected: {name} is {status}")
                self.recommendations.append(f"Validate dependencies and restart path for service: {name}")

    def _analyze_endpoints(self):
        endpoints = self.health_data.get("endpoints", [])

        for endpoint in endpoints:
            url = endpoint.get("url")
            status = endpoint.get("status")
            attempts = endpoint.get("attempts", 1)

            if status != "reachable" and attempts >= 2:
                self.risk_score += 25
                self.findings.append(f"Endpoint failure detected after retries: {url}")
                self.recommendations.append(f"Check DNS, firewall, proxy, certificate, or service availability for {url}")

    def _correlate_findings(self):
        service_failures = any("Service issue" in f for f in self.findings)
        endpoint_failures = any("Endpoint failure" in f for f in self.findings)
        high_memory = any("High memory" in f for f in self.findings)

        if service_failures and endpoint_failures:
            self.risk_score += 15
            self.findings.append("Correlation detected: service failures and endpoint failures are occurring together.")
            self.recommendations.append("Investigate dependent application services before treating endpoint failures as network-only issues.")

        if high_memory and service_failures:
            self.risk_score += 10
            self.findings.append("Correlation detected: service instability may be related to memory pressure.")
            self.recommendations.append("Check service logs for crashes, memory exhaustion, or dependency failures.")

    def _risk_level(self):
        if self.risk_score >= 70:
            return "High"
        if self.risk_score >= 35:
            return "Medium"
        return "Low"

    def _executive_summary(self):
        if not self.findings:
            return "No significant operational health risks detected."

        return (
            f"{len(self.findings)} finding(s) detected with an overall "
            f"{self._risk_level()} risk level. Immediate review recommended."
        )


def save_ai_report(report: dict, path: str = "reports/latest_report.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)