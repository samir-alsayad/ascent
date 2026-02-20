from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class Case(BaseModel):
    """
    Represents a single benchmark test case.
    """
    case_id: str
    domain_root: str = Field(..., description="Path to the frozen /domains snapshot")
    goal: Optional[str] = Field(None, description="Goal for Track/Campaign agents")
    learner_profile: Dict[str, Any] = Field(..., description="Ledger-like competency set")
    target: str = Field(..., description="assignment | module | campaign | track")
    target_id: str = Field(..., description="e.g., computing.numpy.arrays_creation_v1")
    model: str = Field("qwen/qwen3-coder-next", description="OpenRouter model name")
    seed: Optional[int] = 42
    temperature: float = 0.0
    max_tokens: int = 4000
    expected_failure: bool = False
