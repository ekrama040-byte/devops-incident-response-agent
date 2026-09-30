# DevOps Incident Response Commander

An advanced, production-grade DevOps incident response automation framework built with **LangGraph**, **SQLite persistence**, and **local LLM execution (Ollama)**. 

The system automates the lifecycle of production alerts—from intake and severity classification, through concurrent telemetry investigation, reflection validation, automated runbook execution, human-in-the-loop approval gates, and incident reporting.

---

## 🏗️ Architecture & Graph Workflow

The agent runs on a sophisticated multi-node state graph designed with **LangGraph**:

```mermaid
graph TD;
    __start__ --> intake;
    intake --> classifier;
    classifier -.-> notification_node;
    classifier -.-> report_writer;
    classifier -.-> log_investigator;
    log_investigator --> reflection_reviewer;
    metrics_investigator --> reflection_reviewer;
    deployment_investigator --> reflection_reviewer;
    reflection_reviewer --> fix_proposal;
    fix_proposal -.-> apply_fix;
    fix_proposal -.-> human_approval;
    human_approval -.-> apply_fix;
    human_approval -.-> notification_node;
    apply_fix -.-> report_writer;
    apply_fix -.-> log_investigator;
    notification_node --> report_writer;
    report_writer --> __end__;

Core Pipeline Steps:
Intake Node: Validates and ingests incoming webhook alert payloads.

Classifier Node: Evaluates alert severity (Noise, SEV1, SEV2, SEV3) using structured analysis.

Parallel Investigation Fan-out (Send): Concurrently dispatches three specialized worker nodes:

Log Investigator: Queries system logs for stack traces and error patterns.

Metrics Investigator: Pulls CPU, memory, and resource usage telemetry.

Deployment Investigator: Checks recent release histories and version changes.

Reflection Reviewer: Validates investigation findings and ensures root cause validity against telemetry data.

Fix Proposal Node: Synthesizes parallel findings, determines root cause, and proposes remediation with a risk score.

Human-in-the-Loop (interrupt()): Pauses execution for high-risk fixes awaiting operator approval (approve / reject).

Apply Fix Node: Programmatically executes runbooks (e.g., rollback_deployment, clear_logs) with a built-in retry loop for handling transient network failures.

Notification & Report Writer Nodes: Dispatches webhook escalation alerts and compiles a comprehensive Markdown incident report saved in SQLite.

🚀 Key Features
Concurrent Investigation Fan-out: Parallelizes telemetry gathering for high efficiency.

State Persistence & History: Uses SqliteSaver to track incident state history and compile global metrics (auto-fix and escalation rates).

Human-in-the-Loop Control: Safe execution gates pausing for human sign-off on risky operations via LangGraph interrupt().

Offline-First / Local AI: Configured for local inference via Ollama (llama3.2), ensuring zero external cloud service dependencies or paid API keys. Includes a robust fallback mechanism for seamless testing.

Comprehensive Test Suite: Covers distinct test scenarios (Noise filtering, Low-risk automation, Human Approval, Rejection Escalation, and Failure Retry Loops).

⚙️ Prerequisites & Installation
Clone the repository:

Bash
git clone [https://github.com/ekrama040-byte/devops-incident-response-agent.git](https://github.com/ekrama040-byte/devops-incident-response-agent.git)
cd devops-incident-response-agent
Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Copy the example file to create your local .env:

Bash
cp .env.example .env
🕹️ How to Run
Execute the complete test suite (which runs all scenarios, validates graph transitions, and generates global statistics) using a single command:

Bash
python main.py
📂 Project Structure
agent.py — LangGraph workflow definition, nodes, conditional routing, and state graph compilation.

state.py — Pydantic state definitions and TypedDict configurations.

tools.py — Mock DevOps tooling (query_logs, get_metrics, get_recent_deployments, execute_runbook).

main.py — Test runner executing all scenarios and database statistics queries.

.env.example — Template outlining required environment variables.

requirements.txt — Project package dependencies.