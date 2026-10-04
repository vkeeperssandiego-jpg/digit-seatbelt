"""Core safety middleware for request interception and evaluation."""

import json
from typing import Any, Dict, Optional
from .policy_engine import PolicyEngine


class SafetyMiddleware:
    """
    Main middleware class that intercepts requests and evaluates them
    against a safety policy.
    """

    def __init__(self, policy_file: Optional[str] = None, policy_dict: Optional[Dict] = None):
        """
        Initialize the middleware with a policy.

        Args:
            policy_file: Path to a JSON policy file
            policy_dict: A dictionary containing policy rules
        """
        if policy_file:
            with open(policy_file, 'r') as f:
                self.policy = json.load(f)
        elif policy_dict:
            self.policy = policy_dict
        else:
            self.policy = {"rules": []}

        self.engine = PolicyEngine(self.policy)
        self.request_history = []

    def evaluate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a request against the safety policy.

        Args:
            request: A dictionary containing request data (e.g., {"prompt": "..."})

        Returns:
            A result dictionary with:
            - flagged: bool - whether the request was flagged
            - action: str - "allow", "flag", or "block"
            - reason: str - explanation for the action
            - triggered_rules: list - which rules were triggered
        """
        result = self.engine.evaluate(request)

        # Store in history for audit trail
        self.request_history.append({
            "request": request,
            "result": result
        })

        return result

    def get_history(self) -> list:
        """
        Retrieve the request evaluation history.

        Returns:
            List of evaluated requests with their results
        """
        return self.request_history

    def clear_history(self):
        """
        Clear the request history.
        """
        self.request_history = []

    def update_policy(self, policy_dict: Dict):
        """
        Update the policy at runtime.

        Args:
            policy_dict: New policy dictionary
        """
        self.policy = policy_dict
        self.engine = PolicyEngine(self.policy)
