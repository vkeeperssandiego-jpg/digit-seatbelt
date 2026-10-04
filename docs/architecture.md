# Digit Seatbelt Architecture

## Overview

Digit Seatbelt is a lightweight, modular safety middleware designed to intercept and evaluate requests against a configurable policy before they reach an AI system.

## Core Components

### 1. SafetyMiddleware

The main entry point for the system. Responsible for:
- Loading and managing policies
- Intercepting requests
- Coordinating evaluation
- Maintaining audit history

**Key Methods:**
- `evaluate(request)` - Evaluate a request against the policy
- `get_history()` - Retrieve evaluation history
- `update_policy(policy_dict)` - Update policy at runtime

### 2. PolicyEngine

Core evaluation logic. Responsible for:
- Parsing policy rules
- Evaluating each rule against a request
- Aggregating results
- Determining final action (allow, flag, block)

**Rule Types:**
- `keyword_match` - Search for specific keywords
- `pattern_match` - Match regex patterns
- `length_check` - Enforce text length limits

### 3. Rules Module

Helper functions for creating policy rules programmatically:
- `create_keyword_rule()` - Create keyword matching rules
- `create_pattern_rule()` - Create pattern matching rules
- `create_length_rule()` - Create length check rules

## Policy Format

Policies are defined in JSON:

```json
{
  "rules": [
    {
      "id": "unique_rule_id",
      "type": "keyword_match|pattern_match|length_check",
      "action": "allow|flag|block",
      "reason": "Human-readable explanation",
      // type-specific fields
    }
  ]
}
```

## Request Evaluation Flow

```
Request
   |
   v
SafetyMiddleware.evaluate()
   |
   v
PolicyEngine.evaluate()
   |
   +-> For each rule:
   |    |
   |    v
   |    _evaluate_rule()
   |    |
   |    +-> Type-specific check
   |    |    (keywords, patterns, length)
   |    |
   |    v
   |    Triggered? -> Collect reason, update action
   |
   v
Aggregate results
   |
   v
Return result:
{
  "flagged": bool,
  "action": "allow|flag|block",
  "reason": "explanation",
  "triggered_rules": [list of rule ids]
}
   |
   v
Store in history
```

## Action Precedence

When multiple rules are triggered:
1. `block` takes highest precedence
2. `flag` takes next precedence
3. `allow` is the default

## Integration Points

### As a library

```python
from seatbelt.middleware import SafetyMiddleware

middleware = SafetyMiddleware(policy_file='policy.json')
result = middleware.evaluate({"prompt": "user input"})
```

### As an API wrapper

The middleware can be wrapped around API calls to intercept requests before they reach an AI service.

### Custom policies

Extend the `PolicyEngine` to support new rule types by adding new evaluation methods.

## Design Considerations

### Transparency

- All rules are human-readable JSON
- Each rule includes a `reason` field
- Audit history is maintained for all requests

### Performance

- Minimal dependencies (core uses only stdlib)
- Fast rule evaluation
- Rules are evaluated in order

### Extensibility

- New rule types can be added via `_evaluate_rule()` method
- Policies can be updated at runtime
- Custom request fields are supported

### Safety

- Evaluation is deterministic
- All interventions are logged
- No external API calls by default
