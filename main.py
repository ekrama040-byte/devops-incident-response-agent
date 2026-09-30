import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from agent import graph , print_incident_statistics

load_dotenv()

def run_scenarios():
    print("==================================================")
    print("  DEVOPS INCIDENT RESPONSE COMMANDER - TEST SUITE")
    print("\n--- GRAPH MERMAID DIAGRAM ---")
    print(graph.get_graph().draw_mermaid())
    print("-" * 40) 

    """ SCENARIO 1: CPU spike that recovered (Noise) Expected path: Intake -> Classifier -> Report Writer"""
    
    print("\n--- RUNNING SCENARIO 1: Noise Alert ---")
    config_1: RunnableConfig = {"configurable": {"thread_id": "thread-scenario-1"}}
    alert_1 = {
        "alert_id": "INC-2029",
        "service": "report-worker",
        "message": "CPU at 91% for 2 minutes on report-worker, now back to normal",
        "timestamp": "2026-09-28T09:10:00Z"
    }
    graph.invoke(alert_1, config=config_1)

    
    """ SCENARIO 2: Disk at 94% on db-primary (Low-risk fix)
    Expected path: Intake -> Classifier -> Investigator -> Tools -> Fix Proposal -> Apply Fix -> Report Writer"""
    
    print("\n--- RUNNING SCENARIO 2: Disk Usage (Low-risk fix) ---")
    config_2: RunnableConfig = {"configurable": {"thread_id": "thread-scenario-2"}}
    alert_2 = {
        "alert_id": "INC-2030",
        "service": "db-primary",
        "message": "Database disk usage at 94%",
        "timestamp": "2026-09-28T09:12:00Z"
    }
    graph.invoke(alert_2, config=config_2)

    
    """ SCENARIO 3: Error spike after deployment, rollback APPROVED (High-risk fix)
    Expected path: Intake -> Classifier -> Investigator -> Tools -> Fix Proposal -> Human Approval (interrupt) -> [Resume: approve] -> Apply Fix -> Report Writer"""
    
    print("\n--- RUNNING SCENARIO 3 (Part 1): Error Spike - Pausing at Human Approval ---")
    config_3: RunnableConfig = {"configurable": {"thread_id": "thread-scenario-3"}}
    alert_3 = {
        "alert_id": "INC-2031",
        "service": "checkout-service",
        "message": "Error rate spiked to 18% after deployment v2.4.1 on checkout-service",
        "timestamp": "2026-09-28T09:14:00Z"
    }
    
    """ First invocation reaches interrupt() and pauses"""
    
    result_3_paused = graph.invoke(alert_3, config=config_3)
    print(f"\n[INTERRUPT REACHED] Graph paused state: {result_3_paused}")

    print("\n--- RUNNING SCENARIO 3 (Part 2): Resuming with APPROVAL ---")
    """ Resume execution using Command(resume="approve") with the exact same thread_id"""
    graph.invoke(Command(resume="approve"), config=config_3)

    
    """ SCENARIO 4: Error spike after deployment, rollback REJECTED
    Expected path: Intake -> Classifier -> Investigator -> Tools -> Fix Proposal -> Human Approval (interrupt) -> [Resume: reject] -> Report Writer (Escalated)"""
    
    print("\n--- RUNNING SCENARIO 4 (Part 1): Error Spike - Pausing at Human Approval ---")
    config_4: RunnableConfig = {"configurable": {"thread_id": "thread-scenario-4"}}
    alert_4 = {
        "alert_id": "INC-2032",
        "service": "checkout-service",
        "message": "Error rate spiked to 18% after deployment v2.4.1 on checkout-service",
        "timestamp": "2026-09-28T09:20:00Z"
    }
    
    graph.invoke(alert_4, config=config_4)

    print("\n--- RUNNING SCENARIO 4 (Part 2): Resuming with REJECTION ---")
    graph.invoke(Command(resume="reject"), config=config_4)
    
    """ SCENARIO 5 (BONUS): Retry Loop Demonstration"""
    
    print("\n--- RUNNING SCENARIO 5: Retry Loop on Failure ---")
    config_5: RunnableConfig = {"configurable": {"thread_id": "thread-scenario-5-retry"}}
    alert_5 = {
        "alert_id": "INC-7777",
        "service": "fail-service", # This triggers our simulated failure in the node!
        "message": "Testing the automatic retry mechanism",
        "timestamp": "2026-09-28T10:00:00Z"
    }
    graph.invoke(alert_5, config=config_5)

    print_incident_statistics()

    print("\n==================================================")
    print("  ALL SCENARIOS COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_scenarios()