"""
Ledger loader - Loads learner progress from student_state.yaml.
"""

import yaml
from typing import Set

from engine.config import get_learner_state_path


def load_ledger(learner_id: str = "local_user") -> Set[str]:
    """
    Load completed assignment IDs from student_state.yaml.
    Returns: set of completed assignment IDs (those in level >= 2).
    
    Creates learner's state directory if it doesn't exist.
    """
    state_path = get_learner_state_path(learner_id)
    
    if not state_path.exists():
        print(f"[WARN] State file does not exist: {state_path}")
        print("[INFO] Creating empty learner_state directory...")
        state_path.parent.mkdir(parents=True, exist_ok=True)
        return set()
    
    try:
        with open(state_path) as f:
            state = yaml.safe_load(f) or {}
        
        # New 4-tier model: progress is based on 'evidence' section
        evidence = state.get("evidence", {})
        completed = set(evidence.keys())
        
        print(f"[OK] Loaded student_state: {len(completed)} practiced assignments")
        return completed
    except Exception as e:
        print(f"[ERR] Failed to load student state: {e}")
        return set()
