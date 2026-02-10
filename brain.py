"""
brain.py - The Central Voice Box for Budget-Aware AI Squad

=============================================================================
AGENTIC ERA GOVERNANCE MODEL
=============================================================================

In the Agentic Era (2024-2026+), autonomous AI systems execute tasks without
human intervention. This creates a critical challenge: COST CONTROL.

Traditional cloud governance is reactive - you see the bill after the damage.
Agentic governance must be PROACTIVE - costs are forecasted and approved
BEFORE execution.

This module serves as the "Voice Box" - the single point of LLM interaction
for all agents in our multi-agent system. By centralizing LLM calls here, we:

    1. TRACK every token used across the entire agent mesh
    2. SIMULATE costs before they hit real infrastructure  
    3. ENABLE the Accountant Agent to enforce budget circuit breakers
    4. FAVOR local execution (Ollama) over expensive cloud LLMs

Architecture Position:
    ┌─────────────────┐
    │  Supervisor     │
    │  Accountant     │──────► LLMBrain (this module)──────► Ollama (local)
    │  Researcher     │                                          │
    └─────────────────┘                                     Llama 3.1
    
Every agent speaks through this brain. Every token is logged. Every cost
is simulated. This is fiscal self-awareness at the agent level.

=============================================================================
"""

import ollama
from dataclasses import dataclass
from typing import Optional


# Cost simulation constants (based on typical LLM pricing models)
COST_PER_1K_TOKENS = 0.015  # $0.015 per 1,000 tokens
CHARS_PER_TOKEN = 4  # Approximate: 1 token ≈ 4 characters

# Ollama configuration
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1"


@dataclass
class LLMResponse:
    """
    Structured response from the LLM Brain.
    
    Encapsulates both the content and the fiscal metadata required
    for budget-aware agent operations.
    """
    text: str
    estimated_tokens: int
    simulated_cost: float
    model: str


class LLMBrain:
    """
    The Central Voice Box for the Budget-Aware AI Squad.
    
    This class provides a unified interface for all agents to interact with
    the local Ollama LLM. It implements cost simulation to enable the
    Accountant Agent's circuit breaker functionality.
    
    Key Principles:
        - LOCAL FIRST: Uses Ollama to avoid cloud LLM costs
        - COST AWARE: Every response includes simulated cost metadata
        - CENTRALIZED: Single point of control for all LLM interactions
    
    Example:
        >>> brain = LLMBrain()
        >>> response = brain.generate_response(
        ...     prompt="List 3 AWS S3 bucket naming best practices",
        ...     system_message="You are a cloud infrastructure expert."
        ... )
        >>> print(f"Cost: ${response.simulated_cost:.6f}")
    
    Attributes:
        model (str): The Ollama model to use (default: llama3.1)
        host (str): The Ollama server endpoint
        total_tokens_used (int): Running total of tokens consumed
        total_cost_incurred (float): Running total of simulated costs
    """
    
    def __init__(self, model: str = DEFAULT_MODEL, host: str = OLLAMA_HOST):
        """
        Initialize the LLM Brain.
        
        Args:
            model: The Ollama model identifier (default: llama3.1)
            host: The Ollama server URL (default: http://localhost:11434)
        """
        self.model = model
        self.host = host
        
        # Fiscal tracking - the ledger for our budget-aware system
        self.total_tokens_used: int = 0
        self.total_cost_incurred: float = 0.0
        
        # Configure ollama client
        self._client = ollama.Client(host=self.host)
    
    def calculate_simulated_cost(self, text: str) -> tuple[int, float]:
        """
        Estimate token count and calculate simulated cost for a text string.
        
        This is the core of our fiscal governance model. By simulating costs
        BEFORE cloud execution, we enable the Accountant Agent to make
        informed circuit breaker decisions.
        
        Token Estimation Formula:
            tokens ≈ len(text) / 4
            
        Cost Formula:
            cost = (tokens / 1000) * $0.015
        
        Args:
            text: The text to analyze (prompt or response)
            
        Returns:
            tuple: (estimated_tokens, simulated_cost_in_dollars)
            
        Example:
            >>> brain = LLMBrain()
            >>> tokens, cost = brain.calculate_simulated_cost("Hello world!")
            >>> print(f"{tokens} tokens = ${cost:.6f}")
            3 tokens = $0.000045
        """
        # Estimate tokens: ~1 token per 4 characters
        estimated_tokens = max(1, len(text) // CHARS_PER_TOKEN)
        
        # Calculate cost: $0.015 per 1k tokens
        simulated_cost = (estimated_tokens / 1000) * COST_PER_1K_TOKENS
        
        return estimated_tokens, simulated_cost
    
    def generate_response(
        self, 
        prompt: str, 
        system_message: Optional[str] = None
    ) -> LLMResponse:
        """
        Generate a response from the local Ollama LLM.
        
        This is the primary method for agent communication. Every call:
            1. Sends the prompt to Ollama (local, cost-effective)
            2. Calculates simulated token usage and cost
            3. Updates the running fiscal ledger
            4. Returns structured response with cost metadata
        
        The Accountant Agent uses this cost metadata to enforce budget
        constraints and trigger circuit breakers when thresholds are exceeded.
        
        Args:
            prompt: The user/agent prompt to send to the LLM
            system_message: Optional system context for the LLM
            
        Returns:
            LLMResponse: Structured response with text and fiscal metadata
            
        Raises:
            ConnectionError: If Ollama server is unreachable
            
        Example:
            >>> brain = LLMBrain()
            >>> response = brain.generate_response(
            ...     prompt="What is EC2?",
            ...     system_message="Be concise."
            ... )
            >>> print(response.text)
            >>> print(f"This cost: ${response.simulated_cost:.6f}")
        """
        # Build message list for Ollama
        messages = []
        
        if system_message:
            messages.append({
                "role": "system",
                "content": system_message
            })
        
        messages.append({
            "role": "user", 
            "content": prompt
        })
        
        # Calculate input cost (prompt + system message)
        input_text = (system_message or "") + prompt
        input_tokens, input_cost = self.calculate_simulated_cost(input_text)
        
        # Call Ollama (local execution - no cloud cost!)
        response = self._client.chat(
            model=self.model,
            messages=messages
        )
        
        # Extract response text
        response_text = response["message"]["content"]
        
        # Calculate output cost
        output_tokens, output_cost = self.calculate_simulated_cost(response_text)
        
        # Total cost for this interaction
        total_tokens = input_tokens + output_tokens
        total_cost = input_cost + output_cost
        
        # Update the fiscal ledger
        self.total_tokens_used += total_tokens
        self.total_cost_incurred += total_cost
        
        return LLMResponse(
            text=response_text,
            estimated_tokens=total_tokens,
            simulated_cost=total_cost,
            model=self.model
        )
    
    def get_fiscal_summary(self) -> dict:
        """
        Get the current fiscal state of this LLM Brain instance.
        
        Used by the Accountant Agent to track cumulative spending and
        determine if circuit breaker thresholds have been reached.
        
        Returns:
            dict: Fiscal summary with tokens used and costs incurred
        """
        return {
            "total_tokens_used": self.total_tokens_used,
            "total_cost_incurred": self.total_cost_incurred,
            "cost_per_1k_tokens": COST_PER_1K_TOKENS,
            "model": self.model
        }
    
    def check_connection(self) -> bool:
        """
        Verify that the Ollama server is reachable and responsive.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # List models to verify connection
            self._client.list()
            return True
        except Exception:
            return False


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

def ask_llama(prompt: str, system_message: Optional[str] = None) -> str:
    """
    Simple convenience function for quick LLM queries.
    
    This is a stateless wrapper around LLMBrain for simple use cases.
    For budget-tracked operations, use LLMBrain directly.
    
    Args:
        prompt: The question or instruction for the LLM
        system_message: Optional system context
        
    Returns:
        str: The LLM's text response
        
    Example:
        >>> from brain import ask_llama
        >>> response = ask_llama("What is S3?", "Be concise.")
        >>> print(response)
    """
    brain = LLMBrain()
    response = brain.generate_response(prompt, system_message)
    return response.text


# =============================================================================
# CONNECTION TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 LLM BRAIN - Connection Test")
    print("=" * 60)
    print(f"Target: {OLLAMA_HOST}")
    print(f"Model:  {DEFAULT_MODEL}")
    print("-" * 60)
    
    brain = LLMBrain()
    
    # Test 1: Connection check
    print("\n[TEST 1] Checking Ollama connection...")
    if brain.check_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed!")
        print("   Make sure Ollama is running: ollama serve")
        exit(1)
    
    # Test 2: Generate a response
    print("\n[TEST 2] Generating test response...")
    try:
        response = brain.generate_response(
            prompt="In one sentence, what is AWS Lambda?",
            system_message="You are a concise cloud computing expert."
        )
        print(f"✅ Response received!")
        print(f"   Text: {response.text[:100]}...")
        print(f"   Tokens: {response.estimated_tokens}")
        print(f"   Cost: ${response.simulated_cost:.6f}")
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        exit(1)
    
    # Test 3: Cost calculation
    print("\n[TEST 3] Testing cost calculation...")
    test_text = "This is a test string for token estimation."
    tokens, cost = brain.calculate_simulated_cost(test_text)
    print(f"✅ Cost calculation working!")
    print(f"   Input: '{test_text}'")
    print(f"   Estimated tokens: {tokens}")
    print(f"   Simulated cost: ${cost:.6f}")
    
    # Fiscal summary
    print("\n" + "-" * 60)
    print("📊 FISCAL SUMMARY")
    print("-" * 60)
    summary = brain.get_fiscal_summary()
    print(f"Total tokens used:    {summary['total_tokens_used']}")
    print(f"Total cost incurred:  ${summary['total_cost_incurred']:.6f}")
    print(f"Cost rate:            ${summary['cost_per_1k_tokens']}/1k tokens")
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! LLM Brain is ready for the AI Squad.")
    print("=" * 60)
