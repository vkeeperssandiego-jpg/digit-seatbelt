"""Unit tests for the SafetyMiddleware class."""

import unittest
from seatbelt.middleware import SafetyMiddleware


class TestSafetyMiddleware(unittest.TestCase):
    """Test cases for SafetyMiddleware."""

    def setUp(self):
        """Set up test fixtures."""
        self.policy = {
            "rules": [
                {
                    "id": "test_block",
                    "type": "keyword_match",
                    "keywords": ["dangerous"],
                    "action": "block",
                    "reason": "Dangerous keyword detected"
                },
                {
                    "id": "test_flag",
                    "type": "keyword_match",
                    "keywords": ["caution"],
                    "action": "flag",
                    "reason": "Caution keyword detected"
                }
            ]
        }
        self.middleware = SafetyMiddleware(policy_dict=self.policy)

    def test_middleware_initialization(self):
        """Test middleware initializes correctly."""
        self.assertIsNotNone(self.middleware.engine)
        self.assertEqual(len(self.middleware.rules), 2)

    def test_allow_safe_request(self):
        """Test that safe requests are allowed."""
        request = {"prompt": "What is 2 + 2?"}
        result = self.middleware.evaluate(request)

        self.assertFalse(result['flagged'])
        self.assertEqual(result['action'], 'allow')

    def test_flag_request(self):
        """Test that flagged requests are properly marked."""
        request = {"prompt": "Please caution me about this"}
        result = self.middleware.evaluate(request)

        self.assertTrue(result['flagged'])
        self.assertEqual(result['action'], 'flag')
        self.assertIn('test_flag', result['triggered_rules'])

    def test_block_request(self):
        """Test that blocked requests are properly blocked."""
        request = {"prompt": "This is dangerous content"}
        result = self.middleware.evaluate(request)

        self.assertTrue(result['flagged'])
        self.assertEqual(result['action'], 'block')
        self.assertIn('test_block', result['triggered_rules'])

    def test_request_history(self):
        """Test that request history is maintained."""
        request1 = {"prompt": "Safe request"}
        request2 = {"prompt": "dangerous content"}

        self.middleware.evaluate(request1)
        self.middleware.evaluate(request2)

        history = self.middleware.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['request'], request1)
        self.assertEqual(history[1]['request'], request2)

    def test_clear_history(self):
        """Test that history can be cleared."""
        self.middleware.evaluate({"prompt": "test"})
        self.assertEqual(len(self.middleware.get_history()), 1)

        self.middleware.clear_history()
        self.assertEqual(len(self.middleware.get_history()), 0)

    def test_update_policy(self):
        """Test that policy can be updated at runtime."""
        new_policy = {
            "rules": [
                {
                    "id": "new_rule",
                    "type": "keyword_match",
                    "keywords": ["new"],
                    "action": "flag",
                    "reason": "New rule"
                }
            ]
        }

        self.middleware.update_policy(new_policy)
        self.assertEqual(len(self.middleware.rules), 1)

        result = self.middleware.evaluate({"prompt": "new content"})
        self.assertTrue(result['flagged'])


if __name__ == '__main__':
    unittest.main()
