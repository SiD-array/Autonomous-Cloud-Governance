"""
main.py - Phase 3 Orchestrator

=============================================================================
BUDGET-AWARE AI SQUAD: PHASE 3
=============================================================================

This orchestrator script ties together the entire multi-agent mesh:
    1. Initializes the Accountant Agent (Financial Authority)
    2. Initializes the base LLMBrain (Ollama connection)
    3. Wraps the Brain in Budget Guards for the explicit agents
    4. Executes the Researcher -> Writer pipeline
    
This demonstrates FinOps circuit breakers in action. The agents are fiscally
self-aware, requesting funds before making outbound calls.
=============================================================================
"""

import os
import sys

# Add project root to path to resolve local module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
from accountant_agent import AccountantAgent, BudgetExceededException
from budget_guard import BudgetGuardInterceptor
from brain import LLMBrain
from researcher import ResearcherAgent, BUCKET_NAME, INPUT_FILE, LOCALSTACK_ENDPOINT
from writer import WriterAgent
import boto3
from botocore.config import Config

def setup_test_environment():
    """Seed the LocalStack bucket with a test research topic."""
    s3_client = boto3.client(
        's3',
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1',
        config=Config(signature_version='s3v4')
    )
    
    # Ensure bucket exists
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except Exception:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        
    topic = "The impact of autonomous LLM agents on unexpected cloud infrastructure costs when allowed to provision AWS resources dynamically."
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=INPUT_FILE,
        Body=topic.encode('utf-8'),
        ContentType='text/plain'
    )
    print(f"[SETUP] Seeded research topic into s3://{BUCKET_NAME}/{INPUT_FILE}")

def run_mesh(daily_limit: float):
    """
    Execute the multi-agent mesh pipeline with a specific budget limit.
    """
    print("=" * 70)
    print(f"INITIALIZING MESH (Daily Limit: ${daily_limit:.4f})")
    print("=" * 70)
    
    # 1. Initialize the central financial authority
    accountant = AccountantAgent(global_budget=10.0, daily_limit=daily_limit)
    
    # 2. Initialize the shared local brain
    base_brain = LLMBrain()
    
    # 3. Create intercepted brains for the agents
    research_guard = BudgetGuardInterceptor(base_brain, accountant, "Researcher")
    writer_guard = BudgetGuardInterceptor(base_brain, accountant, "Writer")
    
    # 4. Instantiate the workers with DI
    researcher = ResearcherAgent(brain=research_guard)
    writer = WriterAgent(brain=writer_guard)
    
    try:
        print("\n--- PHASE 3.1: RESEARCH ---")
        researcher.research_and_summarize()
        time.sleep(1) # Simulated processing delay
        
        print("\n--- PHASE 3.2: WRITING ---")
        writer.polish_and_publish()
        
        print("\n>>> PIPELINE SUCCESSFUL: Tasks completed within budget.")
        
    except BudgetExceededException as e:
        print(f"\n[!!!] FINOPS INTERVENTION [!!!]\n{str(e)}")
        print(">>> PIPELINE HALTED: Circuit Breaker triggered.")
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed for non-budget reasons: {e}")
        
    finally:
        # Print the final financial ledger
        ledger = accountant.get_ledger()
        print("\n" + "=" * 70)
        print("FINAL FINANCIAL LEDGER")
        print("=" * 70)
        print(f"Daily Limit:     ${ledger.daily_limit:.6f}")
        print(f"Total Spent:     ${ledger.current_spend:.6f}")
        print("Spend by Agent:")
        for agent, spend in ledger.agent_spends.items():
            print(f"  - {agent}: ${spend:.6f}")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    setup_test_environment()
    
    # Test 1: Sufficient Budget
    run_mesh(daily_limit=2.00)
    
    # Test 2: Starved Budget (Expect Circuit Breaker to trip)
    # 0.0001 is almost certainly lower than the mocked CtC
    run_mesh(daily_limit=0.0001)
