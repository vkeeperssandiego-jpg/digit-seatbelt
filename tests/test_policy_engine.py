"""Unit tests for the PolicyEngine class."""

import unittest
from seatbelt.policy_engine import PolicyEngine


class TestPolicyEngine(unittest.TestCase):
    """Test cases for PolicyEngine."""

    def setUp(self):
        """Set up test fixtures."""
        self.policy = {
            "rules": [
                {
                    "id": "keyword_rule",
                    "type": "keyword_match",
                    "keywords": ["apple", "orange"],
                    "action": "flag",
                    "reason": "Fruit keyword detected"
                },
                {
                    "id": "pattern_rule",
                    "type": "pattern_match",
                    "patterns": [r"\d{3}-\d{4}"],
                    "action": "block",
                    "reason": "Phone number detected"
                },
                {
                    "id": "length_rule",
                    "type": "length_check",
                    "max_length": 50,
                    "action": "flag",
                    "reason": "Request too long"
                }
            ]
        }
        self.engine = PolicyEngine(self.policy)

    def test_engine_initialization(self):
        """Test engine initializes correctly."""
        self.assertEqual(len(self.engine.rules), 3)

    def test_keyword_matching(self):
        """Test keyword matching rule."""
        request = {"prompt": "I like apple pie"}
        result = self.engine.evaluate(request)

        self.assertTrue(result['flagged'])
        self.assertIn('keyword_rule', result['triggered_rules'])

    def test_pattern_matching(self):
        """Test pattern matching rule."""
        request = {"prompt": "Call me at 555-1234"}
        result = self.engine.evaluate(request)

        self.assertTrue(result['flagged'])
        self.assertIn('pattern_rule', result['triggered_rules'])
        self.assertEqual(result['action'], 'block')

    def test_length_checking(self):
        """Test length check rule."""
        long_text = "a" * 100
        request = {"prompt": long_text}
        result = self.engine.evaluate(request)

        self.assertTrue(result['flagged'])
        self.assertIn('length_rule', result['triggered_rules'])

    def test_case_insensitive_matching(self):
        """Test that keyword matching is case-insensitive."""
        request = {"prompt": "I like APPLE juice"}
        result = self.engine.evaluate(request)

        self.assertTrue(result['flagged'])
        self.assertIn('keyword_rule', result['triggered_rules'])

    def test_no_rules_triggered(self):
        """Test request that triggers no rules."""
        request = {"prompt": "Hello, how are you?"}
        result = self.engine.evaluate(request)

        self.assertFalse(result['flagged'])
        self.assertEqual(result['action'], 'allow')
        self.assertEqual(len(result['triggered_rules']), 0)

    def test_multiple_rules_triggered(self):
        """Test request that triggers multiple rules."""
        request = {"prompt": "I have an apple and my number is 555-1234"}
        result = self.engine.evaluate(request)

        self.assertTrue(result['flagged'])
        self.assertEqual(result['action'], 'block')  # block takes precedence
        self.assertEqual(len(result['triggered_rules']), 2)

    def test_extract_text_from_message_field(self):
        """Test text extraction from different fields."""
        request = {"message": "test apple content"}
        result = self.engine.evaluate(request)

        self.assertTrue(result['flagged'])
        self.assertIn('keyword_rule', result['triggered_rules'])


if __name__ == '__main__':
    unittest.main()
