"""
researcher.py - The Cloud Researcher Agent

=============================================================================
RESEARCHER AGENT: THE CLOUD WORKER
=============================================================================

In the Budget-Aware AI Squad, the Researcher Agent is the "hands" of the
system. It performs cloud operations (via Boto3) and generates analytical
content (via LLM Brain).

CRITICAL CONSTRAINT (Future Implementation):
    In the full system, this agent CANNOT execute until the Accountant Agent
    approves the forecasted spend. For now, we demonstrate its capabilities
    directly.

Responsibilities:
    1. READ data from cloud storage (S3/LocalStack)
    2. ANALYZE content using the LLM Brain
    3. WRITE results back to cloud storage
    4. REPORT costs for budget tracking

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
INPUT_FILE = "research_topic.txt"
OUTPUT_FILE = "research_notes.txt"


# =============================================================================
# RESEARCHER AGENT
# =============================================================================

class ResearcherAgent:
    """
    The Cloud Researcher Agent - Expert analyst for the AI Squad.
    
    This agent specializes in:
        - Reading research topics from cloud storage
        - Generating technical summaries via LLM
        - Persisting research notes back to the cloud
    
    In the full Budget-Aware system, all operations are gated by the
    Accountant Agent's circuit breaker. The Researcher must submit a
    cost forecast and receive approval before executing.
    
    Attributes:
        brain (LLMBrain): The central LLM interface
        s3_client: Boto3 S3 client configured for LocalStack
        system_prompt (str): The agent's persona definition
    
    Example:
        >>> researcher = ResearcherAgent()
        >>> summary = researcher.research_and_summarize()
        >>> print(f"Research cost: ${researcher.get_session_cost():.6f}")
    """
    
    # Agent Persona - defines behavior and expertise
    SYSTEM_PROMPT = (
        "You are an expert Cloud Researcher. Your goal is to analyze raw topics "
        "and provide a 3-point technical summary. Be concise, accurate, and "
        "focus on actionable insights for cloud governance."
    )
    
    def __init__(self, endpoint_url: str = LOCALSTACK_ENDPOINT):
        """
        Initialize the Researcher Agent.
        
        Args:
            endpoint_url: The LocalStack endpoint (default: http://localhost:4566)
        """
        # Initialize the LLM Brain for intelligent analysis
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
            Exception: If file cannot be read
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
        
        Args:
            bucket: The S3 bucket name
            key: The file key/path
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
    
    def analyze_topic(self, topic: str) -> LLMResponse:
        """
        Analyze a research topic and generate a 3-point summary.
        
        This method sends the topic to the LLM Brain with the Researcher's
        persona, requesting a structured technical analysis.
        
        Args:
            topic: The raw research topic text
            
        Returns:
            LLMResponse: Structured response with summary and cost metadata
        """
        prompt = f"""Analyze the following research topic and provide a 3-point technical summary.

RESEARCH TOPIC:
{topic}

Provide your analysis as:
1. [First key insight]
2. [Second key insight]
3. [Third key insight]

Be concise and focus on cloud governance implications."""

        return self.brain.generate_response(
            prompt=prompt,
            system_message=self.system_prompt
        )
    
    def research_and_summarize(
        self, 
        bucket: str = BUCKET_NAME,
        input_key: str = INPUT_FILE,
        output_key: str = OUTPUT_FILE
    ) -> str:
        """
        Execute the full research workflow.
        
        Workflow:
            1. Read research topic from S3
            2. Analyze with LLM Brain
            3. Save research notes to S3
            4. Return the summary
        
        Args:
            bucket: The S3 bucket name
            input_key: The input file key (research topic)
            output_key: The output file key (research notes)
            
        Returns:
            str: The generated research summary
        """
        # Step 1: Read the research topic from S3
        print(f"[RESEARCHER] Reading topic from s3://{bucket}/{input_key}...")
        topic = self.read_from_s3(bucket, input_key)
        print(f"[RESEARCHER] Topic loaded: {topic[:100]}...")
        
        # Step 2: Analyze with LLM Brain
        print("[RESEARCHER] Analyzing topic with LLM Brain...")
        response = self.analyze_topic(topic)
        summary = response.text
        
        print(f"[RESEARCHER] Analysis complete. Tokens used: {response.estimated_tokens}")
        print(f"[RESEARCHER] Simulated cost: ${response.simulated_cost:.6f}")
        
        # Step 3: Save research notes to S3
        print(f"[RESEARCHER] Saving notes to s3://{bucket}/{output_key}...")
        
        # Format the output with metadata
        notes_content = f"""RESEARCH NOTES
==============
Generated by: Researcher Agent
Source: s3://{bucket}/{input_key}
Tokens Used: {response.estimated_tokens}
Simulated Cost: ${response.simulated_cost:.6f}

ORIGINAL TOPIC:
{topic}

ANALYSIS:
{summary}
"""
        self.write_to_s3(bucket, output_key, notes_content)
        
        return summary
    
    def get_session_cost(self) -> float:
        """
        Get the total simulated cost for this session.
        
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
    print("RESEARCHER AGENT - Cloud Analysis Task")
    print("=" * 60)
    print(f"LocalStack: {LOCALSTACK_ENDPOINT}")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Input: {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("-" * 60)
    
    # Initialize the Researcher Agent
    researcher = ResearcherAgent()
    
    try:
        # Execute the research workflow
        print("\n[STARTING RESEARCH WORKFLOW]\n")
        summary = researcher.research_and_summarize()
        
        # Success output
        print("\n" + "=" * 60)
        print("Research complete. Notes saved to S3.")
        print("=" * 60)
        print("\nRESEARCH SUMMARY:")
        print("-" * 60)
        print(summary)
        print("-" * 60)
        
        # Fiscal summary
        fiscal = researcher.get_fiscal_summary()
        print(f"\nSession Cost: ${fiscal['total_cost_incurred']:.6f}")
        print(f"Total Tokens: {fiscal['total_tokens_used']}")
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("\nTo test this agent, first create a research topic:")
        print(f"  1. Upload a file named '{INPUT_FILE}' to '{BUCKET_NAME}'")
        print("  2. The file should contain a cloud topic to research")
        print("\nExample using AWS CLI:")
        print(f'  aws --endpoint-url={LOCALSTACK_ENDPOINT} s3 cp topic.txt s3://{BUCKET_NAME}/{INPUT_FILE}')
        
    except Exception as e:
        print(f"\n[ERROR] Research failed: {e}")
        print("\nMake sure LocalStack is running:")
        print("  localstack start")
