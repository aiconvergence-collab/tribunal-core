# TRIBUNAL Core

**Multi-Agent Blind Deliberation Engine**

A lightweight, pluggable consensus engine for AI-powered document analysis and claim verification.

## Features

- **3-Round Blind Deliberation Protocol**
  - Round 1: Independent analysis (no peer influence)
  - Round 2: Debate (agents see Round 1 snapshot)
  - Round 3: Adversarial Swap (agents argue opposite positions)

- **Pluggable LLM Backend** - Works with any model (Ollama, GPT, Claude, etc.)
- **Mock Mode** - Test logic without LLM calls
- **Zero Dependencies** - Just `requests` for HTTP calls

## Quick Start

```bash
# Install
pip install -e .

# Test (mock mode - instant)
python test_core.py

# Test (real Ollama - requires ollama running)
python test_ollama.py
```

## Test Scripts

| Script | Mode | Purpose |
|--------|------|---------|
| `test_core.py` | Mock | Verify logic runs (instant, no LLM) |
| `test_ollama.py` | Real | Test with Ollama models (requires setup) |

## Usage

```python
from tribunal.engine import DeliberationEngine

# Define agents
agents = {
    'Skeptic': {'model': 'llama3', 'role': 'Critical Skeptic', 'temperature': 0.7},
    'Analyst': {'model': 'llama3', 'role': 'Evidence Analyst', 'temperature': 0.1},
}

# Initialize
engine = DeliberationEngine(agents)

# Run deliberation
result = engine.deliberate(
    claim="The contract was breached on March 15th.",
    context="Contract clause 4.2 states..."
)

print(result['final_verdict'])  # RESOLVED or UNRESOLVED
print(result['final_confidence'])  # 0.0 - 1.0
```

## Using with Ollama

1. Install Ollama: https://ollama.ai
2. Start server: `ollama serve`
3. Pull a model: `ollama pull llama3.2`
4. Run test: `python test_ollama.py`

## Agent Design Tips

For realistic disagreement, use **conflicting roles**:

```python
agents = {
    'Analyst': {
        'model': 'llama3.2', 
        'role': 'Conservative. Prefer UNRESOLVED unless evidence is 100% undeniable.', 
        'temperature': 0.1  # Cold/Rigid
    },
    'Skeptic': {
        'model': 'llama3.2', 
        'role': 'Aggressive Skeptic. Doubt everything, find alternative explanations.', 
        'temperature': 0.8  # Hot/Creative
    },
    'Hawk': {
        'model': 'llama3.2', 
        'role': 'Security Hawk. Flag RESOLVED immediately on any keyword match.', 
        'temperature': 0.6 
    }
}
```



Contact: @MROCELOT1976 X.COM
FOR THE ENTERPRISE VERSION WITH MORE SOPHISTICATED MULTI AGENT DEBATE ANTI-HALLUCINATION FEATURES

COPYRIGHT 2026

MIT
