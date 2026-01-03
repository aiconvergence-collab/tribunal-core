"""
TEST CORE: Verifies the Blind Deliberation Loop runs correctly.
"""
import sys
sys.path.insert(0, '.')

from tribunal.engine import DeliberationEngine

USE_MOCK = True
MODEL_NAME = "llama3.2:latest"

print(f"🚀 INITIALIZING TRIBUNAL CORE (Mode: {'MOCK' if USE_MOCK else 'REAL OLLAMA'})...")

# 1. Define Agents
agents = {
    'Skeptic': {'model': MODEL_NAME, 'role': 'Critical Skeptic', 'temperature': 0.7},
    'Analyst': {'model': MODEL_NAME, 'role': 'Evidence Analyst', 'temperature': 0.1},
    'Judge':   {'model': MODEL_NAME, 'role': 'Procedural Judge', 'temperature': 0.1}
}

# 2. Initialize Engine
engine = DeliberationEngine(agents)
engine.mock_mode = USE_MOCK

# 3. Run Investigation
claim = "The server log indicates a buffer overflow attack at 03:00 AM."
print(f"\n🔍 INVESTIGATING CLAIM: '{claim}'")

try:
    result = engine.deliberate(claim, context="Log entry: ERROR 0x8932 BUFFER OVERFLOW")
    
    print("\n✅ DELIBERATION COMPLETED SUCCESSFULLY")
    print(f"   • Duration: {result['duration']:.2f}s")
    print(f"   • Verdict:  {result['final_verdict']}")
    print(f"   • Confidence: {result['final_confidence']:.0%}")
    print(f"   • Rounds Run: {len(result['rounds'])}")
    
    # Show each round
    for i, rnd in enumerate(result['rounds'], 1):
        swap_label = " (ADVERSARIAL SWAP)" if i == 3 else ""
        print(f"\n   ═══ Round {i}{swap_label} ═══")
        for entry in rnd:
            swap_icon = "🔄" if entry.get('swapped') else "  "
            print(f"   {swap_icon} {entry['agent']}: {entry['verdict']} ({entry['confidence']:.0%})")
            print(f"      └─ {entry['content'][:60]}...")

except Exception as e:
    print(f"\n❌ TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
