"""
Configuration models for SFP Engine runs.
"""

from pathlib import Path
from typing import List, Optional, Literal, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator

class EnvironmentState(BaseModel):
    practiced: bool = Field(False, description="Has the learner used this environment?")

class LearnerState(BaseModel):
    # Legacy/Simple mode
    knowledge: Optional[Union[str, List[str]]] = Field(None, description="Description of knowledge")
    
    # Structured mode (V2) - 3 Tiers of Competence
    tier_1_claims: List[str] = Field(default_factory=list, description="Self-reported concepts the user claims to know")
    tier_2_practiced: Dict[str, Any] = Field(default_factory=dict, description="Assignments the user submitted")
    tier_3_verified: Dict[str, Any] = Field(default_factory=dict, description="Concept clusters the user passed exams for")
    
    style: Optional[str] = Field("text-based", description="Preferred learning style")
    context: Optional[str] = Field(None, description="Additional context about the learner")

class CurriculumConfig(BaseModel):
    goal: str = Field(..., description="High-level learning goal")
    domains: List[str] = Field(default_factory=list, description="List of domains strictly required")
    tool_first: bool = Field(True, description="Strictly enforce tool acquisition before subject application")
    
class OutputConfig(BaseModel):
    format: Literal["markdown", "json"] = "markdown"
    structure: Literal["school_v2"] = "school_v2"
    root_dir: Optional[str] = None  # Override default runs/ folder

class RunConfig(BaseModel):
    """Configuration for a single SFP run."""
    run_name: str = Field(..., description="Unique identifier for this run")
    model: str = Field(..., description="LLM model identifier (e.g., google/gemini-2.0-flash-001)")
    
    learner_state: LearnerState
    curriculum: CurriculumConfig
    output: OutputConfig = Field(default_factory=OutputConfig)
    
    # Optional override for template paths
    template_dir: Optional[str] = None
    prompt_dir: Optional[str] = None

    @classmethod
    def from_yaml(cls, path: Path) -> "RunConfig":
        import yaml
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        data = yaml.safe_load(path.read_text())
        
        # Support simplified "User Mode" config
        if isinstance(data.get('learner_state'), str):
            data['learner_state'] = {'knowledge': data['learner_state']}
            
        if 'goal' in data and 'curriculum' not in data:
            data['curriculum'] = {'goal': data.pop('goal')}
            
        return cls(**data)
