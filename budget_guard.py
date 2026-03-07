"""
budget_guard.py - The Interceptor Middleware

=============================================================================
BUDGET GUARD: THE CIRCUIT BREAKER PROXY
=============================================================================

This module provides the `BudgetGuardInterceptor`, which wraps around the
standard `LLMBrain`. It acts as a proxy, intercepting LLM requests *before*
they execute to predict costs and request approval from the Accountant Agent.

This design implements the Dependency Injection strategy, allowing future
expansion (like dynamic model routing) without rewriting worker agent logic.

=============================================================================
"""

import os
import sys

# Add project root to path to resolve local module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import math
from typing import Optional
from brain import LLMBrain, LLMResponse, CHARS_PER_TOKEN, COST_PER_1K_TOKENS
from accountant_agent import AccountantAgent, BudgetExceededException


class BudgetGuardInterceptor:
    """
    Proxy wrapper for LLMBrain that enforces budgetary constraints.
    
    This interceptor perfectly matches the generic `LLMBrain` API. When an
    agent calls `generate_response()`, the Guard intercepts it, computes the
    mock Cost-to-Complete (CtC), and requests clearance from the Accountant.
    """
    
    def __init__(self, target_brain: LLMBrain, accountant: AccountantAgent, agent_name: str):
        """
        Initialize the Budget Guard.
        
        Args:
            target_brain: The actual LLMBrain instance to delegate work to upon approval.
            accountant: Reference to the global AccountantAgent.
            agent_name: The name of the agent this guard is attached to (for tracing).
        """
        self._brain = target_brain
        self._accountant = accountant
        self.agent_name = agent_name

    def _mock_predict_ctc(self, prompt: str, system_message: Optional[str] = None) -> float:
        """
        Phase 3 Mock: Predict the Cost-to-Complete (CtC).
        
        In Phase 4, this will be replaced by a regression model.
        For now, we heuristically guess that the output will be roughly
        2x the length of the input, and calculate cost using LLMBrain constants.
        """
        input_text = (system_message or "") + prompt
        
        # Heuristic: Output is often larger than the input prompt for these tasks.
        # Let's assume output is 2x the input size to be conservative.
        estimated_total_chars = len(input_text) * 3 
        
        estimated_tokens = max(1, estimated_total_chars // CHARS_PER_TOKEN)
        estimated_cost = (estimated_tokens / 1000) * COST_PER_1K_TOKENS
        
        return estimated_cost

    def generate_response(self, prompt: str, system_message: Optional[str] = None) -> LLMResponse:
        """
        Intercept the generation request and run the FinOps circuit breaker.
        
        Args:
            prompt: The user/agent prompt to send to the LLM
            system_message: Optional system context for the LLM
            
        Returns:
            LLMResponse: Structured response with text and fiscal metadata
            
        Raises:
            BudgetExceededException: If the Accountant denies the funds.
        """
        print(f"[{self.agent_name.upper()} GUARD] Intercepting request...")
        
        # 1. Predict the cost (Mock CtC)
        estimated_cost = self._mock_predict_ctc(prompt, system_message)
        print(f"[{self.agent_name.upper()} GUARD] Predicted CtC: ${estimated_cost:.6f}")
        
        # 2. Request funds from Accountant (will raise exception if denied)
        self._accountant.request_funds(self.agent_name, estimated_cost)
        
        # 3. If approved, delegate to the actual brain
        print(f"[{self.agent_name.upper()} GUARD] Funds approved. Executing task...")
        return self._brain.generate_response(prompt, system_message)
        
    def calculate_simulated_cost(self, text: str) -> tuple[int, float]:
        """Pass-through to underlying brain."""
        return self._brain.calculate_simulated_cost(text)
        
    def get_fiscal_summary(self) -> dict:
        """Pass-through to underlying brain."""
        return self._brain.get_fiscal_summary()

    @property
    def total_cost_incurred(self) -> float:
        """Property pass-through for Researcher/Writer specific logging."""
        return self._brain.total_cost_incurred
