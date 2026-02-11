"""
writer.py - The Technical Writer Agent

=============================================================================
WRITER AGENT: THE POLISHER
=============================================================================

In the Budget-Aware AI Squad, the Writer Agent transforms raw research into
polished, executive-ready documents. It takes the analytical output from the
Researcher Agent and elevates it into professional communications.

CRITICAL CONSTRAINT (Future Implementation):
    Like all agents in the squad, the Writer CANNOT execute until the 
    Accountant Agent approves the forecasted spend. Every token counts.

Responsibilities:
    1. READ raw research notes from cloud storage
    2. TRANSFORM content into executive-quality documents
    3. WRITE polished reports back to cloud storage
    4. TRACK costs for budget governance

Workflow Position:
    Researcher Agent → [research_notes.txt] → Writer Agent → [executive_summary.txt]

=============================================================================
"""

import boto3
from botocore.config import Config
from brain import LLMBrain, LLMResponse


# =============================================================================
# LOCALSTACK CONFIGURATION
# =============================================================================

LOCALSTACK_ENDPOINT = "http://localhost:4566"
BUCKET_NAME = "milestone-bucket"
INPUT_FILE = "research_notes.txt"
OUTPUT_FILE = "reports/executive_summary.txt"


# =============================================================================
# WRITER AGENT
# =============================================================================

class WriterAgent:
    """
    The Technical Writer Agent - Document polisher for the AI Squad.
    
    This agent specializes in:
        - Reading raw research notes from cloud storage
        - Transforming technical content into executive summaries
        - Producing professional, well-structured documents
    
    In the full Budget-Aware system, all operations are gated by the
    Accountant Agent's circuit breaker. The Writer must submit a
    cost forecast and receive approval before executing.
    
    Cost Model:
        - $0.015 per 1,000 tokens (input + output)
        - Approximately 1 token per 4 characters
    
    Attributes:
        brain (LLMBrain): The central LLM interface
        s3_client: Boto3 S3 client configured for LocalStack
        system_prompt (str): The agent's persona definition
    
    Example:
        >>> writer = WriterAgent()
        >>> summary = writer.polish_and_publish()
        >>> print(f"Writing cost: ${writer.get_session_cost():.6f}")
    """
    
    # Agent Persona - defines behavior and writing style
    SYSTEM_PROMPT = (
        "You are a Professional Technical Writer. Your job is to take raw "
        "research notes and transform them into a polished, executive summary "
        "with clear headings. Use professional language, be concise, and "
        "structure the content for C-level readability."
    )
    
    def __init__(self, endpoint_url: str = LOCALSTACK_ENDPOINT):
        """
        Initialize the Writer Agent.
        
        Args:
            endpoint_url: The LocalStack endpoint (default: http://localhost:4566)
        """
        # Initialize the LLM Brain for content transformation
        self.brain = LLMBrain()
        
        # Configure S3 client for LocalStack
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1',
            config=Config(signature_version='s3v4')
        )
        
        self.system_prompt = self.SYSTEM_PROMPT
    
    def read_from_s3(self, bucket: str, key: str) -> str:
        """
        Read a text file from S3 bucket.
        
        Args:
            bucket: The S3 bucket name
            key: The file key/path
            
        Returns:
            str: The file contents
            
        Raises:
            FileNotFoundError: If file doesn't exist
            Exception: If read fails for other reasons
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')
            return content
        except self.s3_client.exceptions.NoSuchKey:
            raise FileNotFoundError(f"File '{key}' not found in bucket '{bucket}'")
        except Exception as e:
            raise Exception(f"Failed to read from S3: {e}")
    
    def write_to_s3(self, bucket: str, key: str, content: str) -> bool:
        """
        Write text content to S3 bucket.
        
        Note: S3 automatically handles "folder" creation when keys contain '/'.
        
        Args:
            bucket: The S3 bucket name
            key: The file key/path (e.g., 'reports/executive_summary.txt')
            content: The text content to write
            
        Returns:
            bool: True if successful
        """
        try:
            self.s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=content.encode('utf-8'),
                ContentType='text/plain'
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to write to S3: {e}")
    
    def format_executive_summary(self, raw_notes: str) -> LLMResponse:
        """
        Transform raw research notes into a polished executive summary.
        
        This method sends the raw notes to the LLM Brain with the Writer's
        persona, requesting professional formatting and structure.
        
        Args:
            raw_notes: The raw research notes text
            
        Returns:
            LLMResponse: Structured response with summary and cost metadata
        """
        prompt = f"""Format this into a professional executive summary.

RAW RESEARCH NOTES:
{raw_notes}

Create an executive summary with:
- A clear title
- An executive overview paragraph
- Key findings with professional headings
- A brief conclusion with recommendations

Use professional business language suitable for C-level executives."""

        return self.brain.generate_response(
            prompt=prompt,
            system_message=self.system_prompt
        )
    
    def polish_and_publish(
        self, 
        bucket: str = BUCKET_NAME,
        input_key: str = INPUT_FILE,
        output_key: str = OUTPUT_FILE
    ) -> str:
        """
        Execute the full writing workflow.
        
        Workflow:
            1. Read raw research notes from S3
            2. Transform into executive summary via LLM Brain
            3. Save polished report to S3 (in /reports/ folder)
            4. Return the executive summary
        
        Args:
            bucket: The S3 bucket name
            input_key: The input file key (research notes)
            output_key: The output file key (executive summary)
            
        Returns:
            str: The polished executive summary
        """
        # Step 1: Read the research notes from S3
        print(f"[WRITER] Reading notes from s3://{bucket}/{input_key}...")
        raw_notes = self.read_from_s3(bucket, input_key)
        print(f"[WRITER] Notes loaded: {len(raw_notes)} characters")
        
        # Step 2: Transform into executive summary
        print("[WRITER] Polishing content with LLM Brain...")
        response = self.format_executive_summary(raw_notes)
        executive_summary = response.text
        
        print(f"[WRITER] Transformation complete. Tokens used: {response.estimated_tokens}")
        print(f"[WRITER] Simulated cost: ${response.simulated_cost:.6f}")
        
        # Step 3: Save executive summary to S3
        print(f"[WRITER] Saving report to s3://{bucket}/{output_key}...")
        
        # Format the output with metadata header
        report_content = f"""{'=' * 70}
EXECUTIVE SUMMARY
Generated by: Writer Agent | Budget-Aware AI Squad
{'=' * 70}

{executive_summary}

{'=' * 70}
DOCUMENT METADATA
{'=' * 70}
Source: s3://{bucket}/{input_key}
Output: s3://{bucket}/{output_key}
Tokens Used: {response.estimated_tokens}
Generation Cost: ${response.simulated_cost:.6f}
Cost Rate: $0.015 per 1,000 tokens
{'=' * 70}
"""
        self.write_to_s3(bucket, output_key, report_content)
        
        return executive_summary
    
    def get_session_cost(self) -> float:
        """
        Get the total simulated cost for this session.
        
        Cost is calculated at $0.015 per 1,000 tokens.
        
        Returns:
            float: Total cost in dollars
        """
        return self.brain.total_cost_incurred
    
    def get_fiscal_summary(self) -> dict:
        """
        Get the fiscal summary from the LLM Brain.
        
        Returns:
            dict: Fiscal metrics including tokens and costs
        """
        return self.brain.get_fiscal_summary()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("WRITER AGENT - Document Polishing Task")
    print("=" * 60)
    print(f"LocalStack: {LOCALSTACK_ENDPOINT}")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Input: {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("-" * 60)
    
    # Initialize the Writer Agent
    writer = WriterAgent()
    
    try:
        # Execute the writing workflow
        print("\n[STARTING WRITING WORKFLOW]\n")
        summary = writer.polish_and_publish()
        
        # Success output
        print("\n" + "=" * 60)
        print("Report polished and saved to /reports/.")
        print("=" * 60)
        print("\nEXECUTIVE SUMMARY:")
        print("-" * 60)
        print(summary)
        print("-" * 60)
        
        # Fiscal summary with cost tracking
        fiscal = writer.get_fiscal_summary()
        print(f"\nSession Cost: ${fiscal['total_cost_incurred']:.6f}")
        print(f"Total Tokens: {fiscal['total_tokens_used']}")
        print(f"Cost Rate: ${fiscal['cost_per_1k_tokens']}/1k tokens")
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("\nThe Writer Agent requires research notes to exist.")
        print("Run the Researcher Agent first:")
        print("  python researcher.py")
        
    except Exception as e:
        print(f"\n[ERROR] Writing failed: {e}")
        print("\nMake sure LocalStack is running:")
        print("  localstack start")
