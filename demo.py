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

from main import USE_LIVE_AWS

def setup_test_environment():
    if USE_LIVE_AWS:
        s3_client = boto3.client('s3')
    else:
        s3_client = boto3.client(
            's3',
            endpoint_url=LOCALSTACK_ENDPOINT,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1',
            config=Config(signature_version='s3v4')
        )
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except Exception:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
    topic = "Extract data from S3, format the files, and summarize the key figures into a clean structure."
    s3_client.put_object(
        Bucket=BUCKET_NAME, Key=INPUT_FILE, Body=topic.encode('utf-8'), ContentType='text/plain'
    )

def run_mesh(daily_limit: float):
    print("=" * 70)
    print(f"INITIALIZING MESH (Daily Limit: ${daily_limit:.4f})")
    print("=" * 70)
    
    accountant = AccountantAgent(global_budget=10.0, daily_limit=daily_limit)
    base_brain = LLMBrain()
    
    research_guard = BudgetGuardInterceptor(base_brain, accountant, "Researcher", use_live_aws=USE_LIVE_AWS)
    writer_guard = BudgetGuardInterceptor( base_brain, accountant, "Writer", use_live_aws=USE_LIVE_AWS)
    
    researcher = ResearcherAgent(brain=research_guard, use_live_aws=USE_LIVE_AWS)
    writer = WriterAgent(brain=writer_guard, use_live_aws=USE_LIVE_AWS)
    
    try:
        print("\n--- PHASE 3.1: RESEARCH ---")
        researcher.research_and_summarize()
        time.sleep(1)
        
        print("\n--- PHASE 3.2: WRITING ---")
        writer.polish_and_publish()
        
        print("\n>>> PIPELINE SUCCESSFUL: Tasks completed within budget.")
    except BudgetExceededException as e:
        print(f"\n[!!!] FINOPS INTERVENTION [!!!]\n{str(e)}")
        print(">>> PIPELINE HALTED: Circuit Breaker triggered.")
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed for non-budget reasons: {e}")
    finally:
        ledger = accountant.get_ledger()
        print("\n" + "=" * 70)
        print("FINAL FINANCIAL LEDGER")
        print("=" * 70)
        print(f"Daily Limit:     ${ledger.daily_limit:.6f}")
        print(f"Total Spent:     ${ledger.current_spend:.6f}")
        print(f"Total Saved:     ${ledger.total_savings:.6f}")
        print("Spend by Agent:")
        for agent, spend in ledger.agent_spends.items():
            print(f"  - {agent}: ${spend:.6f}")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    setup_test_environment()
    
    # We set it to 0.0075. Researcher usually costs ~0.006. 
    # That will push the ratio past 80% (0.006 / 0.0075 = 80%)
    # And then the Writer will trigger the Dynamic Model Routing to "mistral"
    run_mesh(daily_limit=0.0075)
