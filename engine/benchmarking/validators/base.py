from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple, Optional

class ValidationResult:
    def __init__(self, name: str, passed: bool, reasons: Optional[List[str]] = None):
        self.name = name
        self.passed = passed
        self.reasons = reasons or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "reasons": self.reasons
        }

class BaseValidator(ABC):
    """
    Base class for all benchmark validators.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def validate(self, artifact_type: str, content: str, context: Dict[str, Any]) -> ValidationResult:
        """
        Validates the generated artifact.
        
        Args:
            artifact_type: 'assignment', 'module', etc.
            content: The generated string.
            context: dict containing case info, parent spec, etc.
        """
        pass
