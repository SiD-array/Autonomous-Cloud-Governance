"""
accountant_agent.py - The Budget Governance Authority

=============================================================================
ACCOUNTANT AGENT: THE FINOPS ENFORCER
=============================================================================

This agent maintains the "Shared Financial State" for the decentralized
multi-agent mesh. Before any worker agent invokes an LLM, it must request
funds from this centralized authority.

Responsibilities:
    1. Maintain the Global Budget and Daily Limits
    2. Track cumulative spend across all agents
    3. Approve or deny fund requests based on available budget
    4. Provide financial telemetry

=============================================================================
"""

import threading
from dataclasses import dataclass
from typing import Dict, Optional


class BudgetExceededException(Exception):
    """
    Raised when an agent requests funds that would exceed the daily limit.
    This is the core "Circuit Breaker" mechanism of the system.
    """
    pass


@dataclass
class FinancialLedger:
    global_budget: float
    daily_limit: float
    current_spend: float
    agent_spends: Dict[str, float]


class AccountantAgent:
    """
    The Centralized Financial Authority for the AI Squad.
    
    In a fully distributed mesh, this would be a synchronized state store
    (e.g., Redis). For Phase 3, it is a thread-safe singleton-like object
    managed by the orchestrator.
    """
    
    def __init__(self, global_budget: float = 10.00, daily_limit: float = 2.00):
        """
        Initialize the Accountant Agent.
        
        Args:
            global_budget: The total project budget.
            daily_limit: The maximum allowable spend per day.
        """
        self.global_budget = global_budget
        self.daily_limit = daily_limit
        self.current_spend = 0.0
        
        # Track spend per agent for deeper tracing (variance accuracy goal)
        self.agent_spends: Dict[str, float] = {}
        
        # Thread lock to prevent race conditions during concurrent mesh requests
        self._lock = threading.Lock()
        
    def request_funds(self, agent_name: str, estimated_cost: float) -> bool:
        """
        The preemptive circuit breaker. Evaluates if the task can proceed.
        
        Args:
            agent_name: Identifier of the requesting worker agent.
            estimated_cost: Predicted Cost-to-Complete (CtC) from the Guard.
            
        Returns:
            bool: True if funds are approved.
            
        Raises:
            BudgetExceededException: If the request breaches the daily limit.
        """
        with self._lock:
            projected_spend = self.current_spend + estimated_cost
            
            if projected_spend > self.daily_limit:
                shortfall = projected_spend - self.daily_limit
                raise BudgetExceededException(
                    f"CIRCUIT BREAKER: {agent_name} requested ${estimated_cost:.6f}. "
                    f"This exceeds the daily limit by ${shortfall:.6f}. "
                    f"(Current: ${self.current_spend:.6f} / Limit: ${self.daily_limit:.6f})"
                )
                
            # Approve and allocate funds
            self.current_spend += estimated_cost
            
            if agent_name not in self.agent_spends:
                self.agent_spends[agent_name] = 0.0
            self.agent_spends[agent_name] += estimated_cost
            
            print(f"[ACCOUNTANT] Approved ${estimated_cost:.6f} for {agent_name}. Remaining: ${(self.daily_limit - self.current_spend):.6f}")
            return True

    def get_ledger(self) -> FinancialLedger:
        """Return the current financial state."""
        with self._lock:
            return FinancialLedger(
                global_budget=self.global_budget,
                daily_limit=self.daily_limit,
                current_spend=self.current_spend,
                agent_spends=dict(self.agent_spends)
            )
