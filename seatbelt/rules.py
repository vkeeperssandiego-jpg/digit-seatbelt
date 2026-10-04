"""Rule definitions and helper functions for policy creation."""

from typing import Dict, List, Any


def create_keyword_rule(
    rule_id: str,
    keywords: List[str],
    action: str = "flag",
    reason: str = ""
) -> Dict[str, Any]:
    """
    Create a keyword matching rule.

    Args:
        rule_id: Unique identifier for the rule
        keywords: List of keywords to match
        action: "allow", "flag", or "block"
        reason: Explanation for the rule

    Returns:
        A rule dictionary
    """
    return {
        "id": rule_id,
        "type": "keyword_match",
        "keywords": keywords,
        "action": action,
        "reason": reason or f"Keyword match: {', '.join(keywords)}"
    }


def create_pattern_rule(
    rule_id: str,
    patterns: List[str],
    action: str = "flag",
    reason: str = ""
) -> Dict[str, Any]:
    """
    Create a regex pattern matching rule.

    Args:
        rule_id: Unique identifier for the rule
        patterns: List of regex patterns to match
        action: "allow", "flag", or "block"
        reason: Explanation for the rule

    Returns:
        A rule dictionary
    """
    return {
        "id": rule_id,
        "type": "pattern_match",
        "patterns": patterns,
        "action": action,
        "reason": reason or f"Pattern match triggered"
    }


def create_length_rule(
    rule_id: str,
    max_length: int,
    action: str = "flag",
    reason: str = ""
) -> Dict[str, Any]:
    """
    Create a length check rule.

    Args:
        rule_id: Unique identifier for the rule
        max_length: Maximum allowed text length
        action: "allow", "flag", or "block"
        reason: Explanation for the rule

    Returns:
        A rule dictionary
    """
    return {
        "id": rule_id,
        "type": "length_check",
        "max_length": max_length,
        "action": action,
        "reason": reason or f"Request exceeds {max_length} characters"
    }
