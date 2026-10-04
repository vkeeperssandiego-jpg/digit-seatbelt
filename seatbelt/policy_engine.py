"""Policy evaluation engine that applies rules to requests."""

import re
from typing import Any, Dict, List


class PolicyEngine:
    """
    Evaluates requests against a set of policy rules.
    """

    def __init__(self, policy: Dict):
        """
        Initialize the policy engine with a policy.

        Args:
            policy: A dictionary with 'rules' key containing a list of rules
        """
        self.policy = policy
        self.rules = policy.get('rules', [])

    def evaluate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a request against all rules in the policy.

        Args:
            request: Dictionary containing request data

        Returns:
            A result dictionary with evaluation outcome
        """
        triggered_rules = []
        action = "allow"  # default action
        reasons = []

        # Evaluate each rule
        for rule in self.rules:
            if self._evaluate_rule(rule, request):
                triggered_rules.append(rule['id'])
                reasons.append(rule.get('reason', 'Rule triggered'))

                # Update action based on rule severity
                rule_action = rule.get('action', 'flag')
                if rule_action == 'block':
                    action = 'block'
                elif rule_action == 'flag' and action != 'block':
                    action = 'flag'

        return {
            'flagged': action in ['flag', 'block'],
            'action': action,
            'reason': '; '.join(reasons) if reasons else 'No violations detected',
            'triggered_rules': triggered_rules
        }

    def _evaluate_rule(self, rule: Dict, request: Dict[str, Any]) -> bool:
        """
        Evaluate a single rule against a request.

        Args:
            rule: A rule dictionary
            request: A request dictionary

        Returns:
            True if the rule is triggered, False otherwise
        """
        rule_type = rule.get('type')

        if rule_type == 'keyword_match':
            return self._check_keywords(rule, request)
        elif rule_type == 'pattern_match':
            return self._check_patterns(rule, request)
        elif rule_type == 'length_check':
            return self._check_length(rule, request)
        else:
            return False

    def _check_keywords(self, rule: Dict, request: Dict[str, Any]) -> bool:
        """
        Check if request contains any keywords from the rule.
        """
        keywords = rule.get('keywords', [])
        request_text = self._extract_text(request).lower()

        for keyword in keywords:
            if keyword.lower() in request_text:
                return True
        return False

    def _check_patterns(self, rule: Dict, request: Dict[str, Any]) -> bool:
        """
        Check if request matches any regex patterns from the rule.
        """
        patterns = rule.get('patterns', [])
        request_text = self._extract_text(request)

        for pattern in patterns:
            if re.search(pattern, request_text, re.IGNORECASE):
                return True
        return False

    def _check_length(self, rule: Dict, request: Dict[str, Any]) -> bool:
        """
        Check if request text exceeds length threshold.
        """
        max_length = rule.get('max_length', float('inf'))
        request_text = self._extract_text(request)

        return len(request_text) > max_length

    def _extract_text(self, request: Dict[str, Any]) -> str:
        """
        Extract text content from a request.
        Looks for common fields like 'prompt', 'message', 'content', 'text'.
        """
        for field in ['prompt', 'message', 'content', 'text', 'input']:
            if field in request:
                value = request[field]
                if isinstance(value, str):
                    return value

        # Fallback: convert entire request to string
        return str(request).lower()
