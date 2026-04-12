"""
bridge.py - Phase 1: Digital Office Milestone

=============================================================================
PHASE 1 COMPLETE: THE DIGITAL OFFICE ($0.00 CLOUD COST)
=============================================================================

This script demonstrates the foundational connection between our AI agents
and cloud infrastructure. By using:

    - Ollama (local LLM) instead of cloud-based models
    - LocalStack (local AWS simulation) instead of real AWS

We achieve our first milestone with ZERO cloud expenditure. This is the
essence of budget-aware agentic computing: prove the concept locally before
incurring real costs.

The "bridge" represents the connection point where AI reasoning meets
cloud action - a critical junction that the Accountant Agent will later
govern with circuit breakers.

=============================================================================
"""

from brain import ask_llama
import boto3
from botocore.config import Config


# =============================================================================
# LOCALSTACK CONFIGURATION
# =============================================================================

LOCALSTACK_ENDPOINT = "http://localhost:4566"
BUCKET_NAME = "milestone-bucket"
FILE_NAME = "hello_agent.txt"

# Configure boto3 for LocalStack
# No real AWS credentials needed - LocalStack accepts any credentials
localstack_config = Config(
    signature_version='s3v4',
    retries={'max_attempts': 3}
)

# Initialize S3 client pointing to LocalStack
s3_client = boto3.client(
    's3',
    endpoint_url=LOCALSTACK_ENDPOINT,
    aws_access_key_id='test',           # LocalStack default
    aws_secret_access_key='test',       # LocalStack default
    region_name='us-east-1',
    config=localstack_config
)


# =============================================================================
# PHASE 1 MILESTONE EXECUTION
# =============================================================================

def check_bucket_exists(bucket_name: str) -> bool:
    """Check if an S3 bucket exists in LocalStack."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except s3_client.exceptions.ClientError:
        return False
    except Exception:
        return False


def create_bucket_if_not_exists(bucket_name: str) -> bool:
    """Create S3 bucket if it doesn't already exist."""
    if check_bucket_exists(bucket_name):
        print(f"[INFO] Bucket '{bucket_name}' already exists.")
        return True
    
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"[INFO] Bucket '{bucket_name}' created successfully.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create bucket: {e}")
        return False


def upload_message_to_s3(message: str, bucket: str, key: str) -> bool:
    """Upload a text message to S3 bucket."""
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=message.encode('utf-8'),
            ContentType='text/plain'
        )
        return True
    except Exception as e:
        print(f"[ERROR] Failed to upload: {e}")
        return False


def main():
    """
    Execute Phase 1 Milestone: Digital Office Setup
    
    This proves our agent can:
        1. Think (via Ollama LLM)
        2. Act (via LocalStack S3)
        3. Track costs (simulated at $0.00 cloud cost)
    """
    print("=" * 60)
    print("PHASE 1: DIGITAL OFFICE MILESTONE")
    print("=" * 60)
    print(f"LocalStack Endpoint: {LOCALSTACK_ENDPOINT}")
    print(f"Target Bucket: {BUCKET_NAME}")
    print("-" * 60)
    
    # Step 1: Generate message using local LLM
    print("\n[STEP 1] Asking Llama for a Hello World message...")
    
    llm_message = ask_llama(
        prompt="Generate a one-sentence 'Hello World' message for a 2026 Cloud Governance project. Be creative and mention AI agents.",
        system_message="You are a friendly AI assistant helping launch a budget-aware cloud governance system."
    )
    
    print(f"[LLM RESPONSE] {llm_message}")
    
    # Step 2: Ensure bucket exists
    print(f"\n[STEP 2] Checking/creating bucket '{BUCKET_NAME}'...")
    
    if not create_bucket_if_not_exists(BUCKET_NAME):
        print("[FAILED] Could not create bucket. Is LocalStack running?")
        print("         Start it with: localstack start")
        return
    
    # Step 3: Upload the LLM-generated message
    print(f"\n[STEP 3] Uploading message as '{FILE_NAME}'...")
    
    if upload_message_to_s3(llm_message, BUCKET_NAME, FILE_NAME):
        print("[SUCCESS] File uploaded!")
    else:
        print("[FAILED] Upload failed.")
        return
    
    # Step 4: Success feedback
    print("\n" + "=" * 60)
    print("PHASE 1 MILESTONE COMPLETE!")
    print("=" * 60)
    print(f"\nUploaded Content:")
    print(f"  \"{llm_message}\"")
    print(f"\nLocation:")
    print(f"  s3://{BUCKET_NAME}/{FILE_NAME}")
    print(f"\nCloud Cost: $0.00 (LocalStack simulation)")
    print(f"LLM Cost:   $0.00 (Ollama local execution)")
    print("-" * 60)
    
    # ==========================================================================
    # PHASE 1 'DIGITAL OFFICE' MILESTONE COMPLETED FOR $0.00
    # 
    # This proves our architecture works:
    #   - Local LLM (Ollama) generates intelligent content
    #   - Local cloud simulation (LocalStack) handles infrastructure
    #   - Zero cloud spend achieved
    #
    # Next: Add the Accountant Agent to govern real cloud spend.
    # ==========================================================================


if __name__ == "__main__":
    main()
