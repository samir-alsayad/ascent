from engine.benchmarking.validators.base import BaseValidator, ValidationResult
from typing import Dict, Any
import re

class VerificationValidator(BaseValidator):
    """
    Checks for the presence of a verifiable artifact/script in the mission.
    """
    @property
    def name(self) -> str:
        return "verification_presence"

    def validate(self, artifact_type: str, content: str, context: Dict[str, Any]) -> ValidationResult:
        if artifact_type != "assignment":
            return ValidationResult(self.name, True)
            
        if any(content.startswith(x) for x in ["SKIP:", "REFUSE:"]):
            return ValidationResult(self.name, True)
            
        reasons = []
        
        # Look for a verification header flexibly
        if not re.search(r"^#+\s+.*Verification", content, re.IGNORECASE | re.MULTILINE):
            reasons.append("Missing 'Verification' section header.")
            
        # For computing domains, we strongly prefer a python block or a clear script reference
        if "computing" in context.get("target_id", ""):
            if "```python" not in content and "verification.py" not in content.lower():
                reasons.append("Computing assignment missing executable verification artifacts.")
        
        if reasons:
            return ValidationResult(self.name, False, reasons)
            
        return ValidationResult(self.name, True)
