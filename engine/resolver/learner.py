"""
Learner State Management.
Handles loading and querying of learner competencies.
"""

import yaml
from pathlib import Path
from typing import Set, Dict, Any, List

class LearnerProfile:
    """Represents the current state of a learner (mocks or real)."""
    
    def __init__(self, data: Dict[str, Any] = None):
        self._data = data or {}
        
        # V2: 3-Tier Competence Model
        self.tier_1_claims: List[str] = self._data.get("tier_1_claims", []) or []
        self.tier_2_practiced: Dict[str, Any] = self._data.get("tier_2_practiced", {}) or {}
        self.tier_3_verified: Dict[str, Any] = self._data.get("tier_3_verified", {}) or {}
        
        # Legacy fallback
        self.knowledge_desc = (
            self._data.get("knowledge") 
            or self._data.get("profile", {}).get("description") 
            or None
        )
        
        # Legacy: merge old competencies into tier_1
        if not self.tier_1_claims and "competencies" in self._data:
            self.tier_1_claims = self._data.get("competencies", [])

    @classmethod
    def load(cls, path: Path) -> "LearnerProfile":
        if not path.exists():
            raise FileNotFoundError(f"Learner state file not found: {path}")
        data = yaml.safe_load(path.read_text())
        return cls(data)

    def has_competency(self, competency_id: str) -> bool:
        """Check if a competency is known at ANY tier."""
        if competency_id in self.tier_3_verified:
            return True
        if competency_id in self.tier_2_practiced:
            return True
        if competency_id in self.tier_1_claims:
            return True
        return False

    def to_prompt_string(self) -> str:
        """Convert state to a prompt-friendly summary."""
        sections = []
        
        # Description
        if self.knowledge_desc:
            sections.append(f"Profile Description: {self.knowledge_desc}")
        
        # Tier 3: Verified (strongest evidence)
        if self.tier_3_verified:
            lines = ["# Tier 3 — VERIFIED Competencies (Exam-Proven Mastery):"]
            lines.append("These concepts are PROVEN. DO NOT reteach them.")
            for comp in sorted(self.tier_3_verified.keys()):
                lines.append(f"  - {comp}")
            sections.append("\n".join(lines))
            
        # Tier 2: Practiced  
        if self.tier_2_practiced:
            lines = ["# Tier 2 — PRACTICED Assignments (Completed Work):"]
            lines.append("These assignments have been submitted. The learner has exposure to these topics.")
            for comp in sorted(self.tier_2_practiced.keys()):
                lines.append(f"  - {comp}")
            sections.append("\n".join(lines))
            
        # Tier 1: Claims
        if self.tier_1_claims:
            lines = ["# Tier 1 — SELF-REPORTED Claims (Unverified):"]
            lines.append("The learner CLAIMS to know these. Trust for skipping intro material, but do not treat as proven.")
            for comp in sorted(self.tier_1_claims):
                lines.append(f"  - {comp}")
            sections.append("\n".join(lines))
        
        if not self.tier_1_claims and not self.tier_2_practiced and not self.tier_3_verified:
            sections.append("No prior knowledge reported. Treat as a complete beginner.")
            
        return "\n\n".join(sections)

