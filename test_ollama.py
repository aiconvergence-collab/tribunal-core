"""
TEST VARIATION: Runs Tribunal Core with REAL Ollama models.
Focuses on generating disagreement/consensus variation.
"""
import sys
sys.path.insert(0, '.')

from tribunal.engine import DeliberationEngine

# --- CONFIGURATION ---
# 1. Ensure you have pulled these models: `ollama pull llama3.2` (or mistral, etc)
#    Using the same model for all is fine, but different roles key.
MODEL = "llama3.2:latest" 

print(f"🚀 INITIALIZING REAL OLLAMA TEST (Model: {MODEL})...")
print("   (Note: This will be slower than mock mode)")

# 2. Define Agents with CONFLICTING parameters to force debate
agents = {
    'Analyst': {
        'model': MODEL, 
        'role': 'Conservative Analyst. You prefer "UNRESOLVED" unless evidence is 100% undeniable.', 
        'temperature': 0.1  # Cold/Rigid
    },
    'Skeptic': {
        'model': MODEL, 
        'role': 'Aggressive Skeptic. You actively doubt log files and look for alternative explanations.', 
        'temperature': 0.8  # Hot/Creative
    },
    'Alarmist': {
        'model': MODEL, 
        'role': 'Security Hawk. You verify "RESOLVED" immediately if any keyword matches.', 
        'temperature': 0.6 
    }
}

# 3. Initialize Engine
engine = DeliberationEngine(agents)

# CRITICAL: Disable mock mode to hit the real API
engine.mock_mode = False 

# 4. Use an AMBIGUOUS Claim (Harder to agree on)
# A clear claim like "System is down" usually gets 100% agreement.
# A vague claim forces them to rely on their bias.
claim = "The user behavior pattern in the logs is anomalous but technically authorized."
context = "User: Admin_01. Action: Bulk Export. Time: 2:00 AM (local). IP: Corporate VPN. History: User rarely exports data."

print(f"\n🔍 INVESTIGATING AMBIGUOUS CLAIM: '{claim}'")

try:
    result = engine.deliberate(claim, context=context)
    
    # 5. Report Results
    print("\n✅ DELIBERATION COMPLETE")
    print(f"   • Verdict:    {result['final_verdict']}")
    print(f"   • Confidence: {result['final_confidence']:.0%}")
    print(f"   • Duration:   {result['duration']:.1f}s")
    print("-" * 50)
    
    # Show the disagreement
    print("   • AGENT VOTES:")
    for rnd in result['rounds']:
        if not rnd: continue
        swap_label = " (ADVERSARIAL SWAP)" if rnd[0].get('swapped') else ""
        print(f"     [Round {rnd[0]['round']}{swap_label}]")
        for entry in rnd:
            swap_icon = "🔄" if entry.get('swapped') else "  "
            print(f"      {swap_icon} {entry['agent']:<10}: {entry['verdict']} (Conf: {entry['confidence']:.2f})")
            if entry.get('content'):
                print(f"         └─ {entry['content'][:70]}...")

except Exception as e:
    print(f"\n❌ TEST FAILED: {str(e)}")
    print("   (Did you run 'ollama serve' and pull the model?)")
    import traceback
    traceback.print_exc()
