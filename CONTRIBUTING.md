# Contributing to TRIBUNAL Core

We welcome contributions to the agent library and consensus logic. To maintain the integrity of the deliberation protocol, all contributions must adhere to the following standards:

### 1. Agent Design
New agents must have a defined `role` and a specific `temperature` setting. 
- **Conservative Agents:** Temperature < 0.2
- **Creative/Adversarial Agents:** Temperature > 0.7

### 2. Protocol Integrity
The 3-Round Deliberation sequence (Blind -> Debate -> Swap) is the core of this project. Any changes to the `DeliberationEngine` must preserve the **Static Snapshot** requirement to prevent cascading model bias.

### 3. Testing
Before submitting a Pull Request, ensure your changes pass:
- `python test_core.py` (Mock logic check)
- `python test_ollama.py` (Inference check)

### 4. Licensing
By contributing, you agree that your contributions will be licensed under the project's MIT License.