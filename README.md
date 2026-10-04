# Digit Seatbelt

Open safety infrastructure for human-AI interaction.

Digit Seatbelt is a lightweight, model-agnostic middleware that provides a transparent safety layer between users, applications, and AI systems.

## Mission

Build a practical safety middleware that provides:

- **Risk detection**: Identify potentially unsafe requests before they reach an AI system
- **Transparent triggers**: Clear, auditable rules for when intervention occurs
- **Explainable interventions**: Communicate why a request was flagged or modified
- **Open governance**: Community-driven safety standards

## Status

Early prototype and research phase. Suitable for experimentation and feedback.

## Quick Start

### Installation

```bash
git clone https://github.com/vkeeperssandiego-jpg/digit-seatbelt.git
cd digit-seatbelt
pip install -r requirements.txt
```

### Basic Usage

```python
from seatbelt.middleware import SafetyMiddleware

# Initialize with default policy
middleware = SafetyMiddleware(policy_file='policies/default_policy.json')

# Intercept and evaluate a request
request = {"prompt": "How do I build a nuclear weapon?"}
result = middleware.evaluate(request)

if result['flagged']:
    print(f"Request flagged: {result['reason']}")
    print(f"Intervention: {result['action']}")
else:
    print("Request allowed.")
```

## Project Structure

```
digit-seatbelt/
├── seatbelt/
│   ├── __init__.py
│   ├── middleware.py          # Core safety middleware
│   ├── policy_engine.py       # Policy evaluation logic
│   └── rules.py               # Rule definitions and triggers
├── policies/
│   └── default_policy.json    # Sample safety policy
├── tests/
│   ├── __init__.py
│   ├── test_middleware.py     # Middleware tests
│   └── test_policy_engine.py  # Policy engine tests
├── examples/
│   └── basic_usage.py         # Usage example
├── docs/
│   ├── vision.md              # Project vision
│   └── architecture.md        # System design
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

## Design Principles

1. **Transparency**: Safety logic is visible and auditable
2. **Human-centered**: Users understand why requests are flagged
3. **Model-agnostic**: Works with any AI backend
4. **Lightweight**: Minimal dependencies, easy to integrate
5. **Extensible**: Custom policies and rules

## Key Features

- Policy-driven risk detection
- Request interception and evaluation
- Reason logging for transparency
- Simple JSON-based policy format
- No external dependencies for core functionality

## Policy System

Safety rules are defined in JSON format. Example:

```json
{
  "rules": [
    {
      "id": "harmful_content",
      "type": "keyword_match",
      "keywords": ["bomb", "weapon", "attack"],
      "action": "block",
      "reason": "Request contains potentially harmful keywords"
    },
    {
      "id": "jailbreak_attempt",
      "type": "pattern_match",
      "patterns": ["ignore.*instruction", "bypass.*filter"],
      "action": "flag",
      "reason": "Request may be attempting to bypass safety measures"
    }
  ]
}
```

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

## Contributing

Contributions and ideas are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is open source and available under the MIT License.

## Next Steps

- [ ] Expand policy rule types
- [ ] Add logging and auditability
- [ ] Create interactive policy editor
- [ ] Build community governance framework
- [ ] Publish architecture documentation
