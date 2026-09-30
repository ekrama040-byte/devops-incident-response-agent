from langchain_core.tools import tool

@tool
def query_logs(service: str, tail_lines: int = 50) -> str:
    """Query recent error logs and stack traces for a given microservice."""
    logs_db = {
        "db-primary": "[ERROR] 2026-09-28 09:10:12 - Connection pool exhausted. Max connections (100) reached.\n[FATAL] Transaction timeout on table 'users'.",
        "checkout-service": "[ERROR] 2026-09-28 09:14:02 - Payment gateway timeout for deployment v2.4.1.\n[ERROR] Unhandled exception in /api/v1/checkout: NullPointerException.",
        "report-worker": "[INFO] Worker processing batch 402.\n[WARN] High memory consumption detected (85%)."
    }
    return logs_db.get(service, "No recent error logs found for this service.")

@tool
def get_metrics(service: str) -> str:
    """Get current CPU, memory, disk, and error rate metrics for a service."""
    metrics_db = {
        "db-primary": "CPU: 45%, Memory: 60%, Disk Usage: 94% (CRITICAL), Error Rate: 2.1%",
        "checkout-service": "CPU: 88%, Memory: 75%, Disk Usage: 45%, Error Rate: 18.4% (SPIKE)",
        "report-worker": "CPU: 91% for 2 mins (now recovering), Memory: 82%, Disk: 50%, Error Rate: 0.5%"
    }
    return metrics_db.get(service, "Metrics unavailable for this service.")

@tool
def get_recent_deployments(service: str) -> str:
    """Fetch metadata on the last 3 deployments for a service."""
    deployments_db = {
        "db-primary": "1. v1.9.0 (2026-09-25) - Stable\n2. v1.8.2 (2026-09-10)",
        "checkout-service": "1. v2.4.1 (2026-09-28 09:00:00Z) - Author: dev-lead (CURRENT ACTIVE)\n2. v2.4.0 (2026-09-20) - Stable",
        "report-worker": "1. v1.1.2 (2026-09-27) - Stable"
    }
    return deployments_db.get(service, "No deployment history found.")

def execute_runbook(action: str, service: str) -> str:
    """Execute a remediation runbook action on the target service."""
    valid_actions = ["restart_service", "clear_logs", "scale_up", "rollback_deployment"]
    if action not in valid_actions:
        return f"failed: unknown action '{action}'"
    
    # Mock successful execution
    return f"success: successfully executed '{action}' on service '{service}'."