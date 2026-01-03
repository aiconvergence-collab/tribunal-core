"""
TRIBUNAL CORE ENGINE
--------------------
The Blind-Execution Deliberation Logic.
"""
import time
import json
import requests
from typing import List, Dict, Any
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

def classify_harm_type(claim: str) -> str:
    claim_lower = claim.lower()
    if any(w in claim_lower for w in ['attack', 'overflow', 'exploit', 'breach']):
        return 'security'
    return 'general'

def get_threshold(harm_type: str) -> float:
    return {'security': 0.85, 'general': 0.75}.get(harm_type, 0.80)

class DeliberationEngine:
    def __init__(self, agent_configs: Dict, config: Dict = None):
        self.agents = agent_configs
        self.config = config or {}
        self.mock_mode = False

    def deliberate(self, claim: str, context: str = "") -> Dict:
        start_time = time.time()
        
        harm_type = classify_harm_type(claim)
        threshold = get_threshold(harm_type)
        
        rounds = []
        
        # --- ROUND 1: BLIND ---
        round1 = self._run_round(claim, context, 1, [], harm_type, threshold)
        rounds.append(round1)
        
        # --- ROUND 2: DEBATE ---
        round2 = self._run_round(claim, context, 2, round1, harm_type, threshold)
        rounds.append(round2)
        
        # --- ROUND 3: ADVERSARIAL SWAP ---
        round3 = self._run_swap_round(claim, context, round2, harm_type, threshold)
        rounds.append(round3)
        
        # --- SYNTHESIS ---
        final_verdict = self._synthesize_verdict(rounds[-1])
        
        return {
            "claim": claim,
            "final_verdict": final_verdict['verdict'],
            "final_confidence": final_verdict['confidence'],
            "rounds": rounds,
            "duration": time.time() - start_time
        }

    def _run_round(self, claim: str, context: str, round_num: int, prev_round: List[Dict], harm: str, thresh: float) -> List[Dict]:
        results = []
        snapshot = self._format_prev_round(prev_round) if prev_round else None

        for name, config in self.agents.items():
            prompt = self._build_prompt(claim, name, config['role'], context, snapshot, harm, thresh)
            response = self._call_model(config['model'], prompt, config.get('temperature', 0.5))
            
            results.append({
                'round': round_num,
                'agent': name,
                'verdict': response.get('verdict', 'UNRESOLVED'),
                'confidence': response.get('confidence', 0.5),
                'content': response.get('statement', ''),
                'swapped': False
            })
        return results

    def _run_swap_round(self, claim: str, context: str, prev_round: List[Dict], harm: str, thresh: float) -> List[Dict]:
        results = []
        snapshot = self._format_prev_round(prev_round)
        
        for name, config in self.agents.items():
            swapped_role = f"Devil's Advocate. Argue AGAINST {config['role']}"
            prompt = self._build_prompt(claim, name, swapped_role, context, snapshot, harm, thresh, swap=True)
            response = self._call_model(config['model'], prompt, 0.7)
            
            results.append({
                'round': 3,
                'agent': name,
                'swapped': True,
                'verdict': response.get('verdict', 'UNRESOLVED'),
                'confidence': response.get('confidence', 0.5),
                'content': response.get('statement', '')
            })
        return results

    def _build_prompt(self, claim: str, agent: str, role: str, context: str, prev: str, harm: str, thresh: float, swap: bool = False) -> str:
        prompt = f"""You are {agent}. Role: {role}.
CLAIM: "{claim}"
HARM TYPE: {harm} (Threshold: {thresh})
CONTEXT: {context[:1000]}
"""
        if prev:
            prompt += f"\nPEER POSITIONS:\n{prev}"
        if swap:
            prompt += "\n⚠️ ADVERSARIAL MODE: Argue AGAINST your usual bias."
        
        prompt += '\nRespond JSON: {"verdict": "RESOLVED/UNRESOLVED", "confidence": 0.XX, "statement": "..."}'
        return prompt

    def _format_prev_round(self, prev_entries: List[Dict]) -> str:
        return "\n".join([f"- {e['agent']}: {e['verdict']}" for e in prev_entries])

    def _call_model(self, model: str, prompt: str, temperature: float) -> Dict:
        if self.mock_mode:
            import random
            # Simulate realistic agent variation
            verdicts = ["RESOLVED", "RESOLVED", "UNRESOLVED"]  # Slight bias toward resolved
            v = random.choice(verdicts)
            c = random.uniform(0.45, 0.92)
            statements = [
                "Evidence supports the claim based on log patterns.",
                "Insufficient data to confirm with certainty.",
                "Attack signature matches known buffer overflow patterns.",
                "Timestamp anomaly requires further investigation.",
                "Log entry consistent with malicious activity."
            ]
            return {"verdict": v, "confidence": round(c, 2), "statement": random.choice(statements)}

        try:
            response = requests.post(OLLAMA_URL, json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": temperature}
            }, timeout=30)
            
            if response.status_code != 200:
                return {"verdict": "ERROR", "statement": f"Ollama Error: {response.text}"}
                
            raw = response.json().get("response", "{}")
            return json.loads(raw)
        except Exception as e:
            return {"verdict": "ERROR", "statement": f"Connection Failed: {str(e)}"}

    def _synthesize_verdict(self, results: List[Dict]) -> Dict:
        votes = [r['verdict'] for r in results]
        if not votes:
            return {"verdict": "UNRESOLVED", "confidence": 0.0}
        
        final_verdict = max(set(votes), key=votes.count)
        conf = votes.count(final_verdict) / len(votes)
        return {"verdict": final_verdict, "confidence": conf}
