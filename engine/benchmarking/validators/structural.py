from engine.benchmarking.validators.base import BaseValidator, ValidationResult
from typing import Dict, Any
import re

class StructuralValidator(BaseValidator):
    """
    Checks for the presence of required markdown headings in missions.
    """
    @property
    def name(self) -> str:
        return "structural_consistency"

    def validate(self, artifact_type: str, content: str, context: Dict[str, Any]) -> ValidationResult:
        if artifact_type != "assignment":
            return ValidationResult(self.name, True)
            
        if any(content.startswith(x) for x in ["SKIP:", "REFUSE:"]):
            return ValidationResult(self.name, True)
            
        requested_headers = [
            "Context",
            "Challenge",
            "Requirements",
            "Invariants",
            "Verification",
            "Reflection"
        ]
        
        missing = []
        for h in requested_headers:
            # Look for '# ... Header' or '**Header**'
            pattern = rf"(^#+\s+.*{h})|(\*\*{h}\*\*)"
            if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                missing.append(h)
                
        if missing:
            return ValidationResult(self.name, False, [f"Missing headers: {', '.join(missing)}"])
            
        return ValidationResult(self.name, True)
