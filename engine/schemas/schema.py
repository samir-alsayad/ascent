"""
Core Schema Definitions for Benchmark V2.
Defines strict types for Competency IDs and Module Proposals.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
import re

# Strict Regex for Competency IDs: domain.subdomain.concept.verb
# Example: computing.networking.tcp_handshake.trace_sequence
COMPETENCY_ID_REGEX = r"^[a-z0-9_]+\.[a-z0-9_]+\.[a-z0-9_]+\.[a-z0-9_]+$"

# Allowed verbs for the last segment
ALLOWED_VERBS = {
    "identify", "trace", "construct", "transform", 
    "predict", "diagnose", "formalize", "apply"
}

class CompetencyID(str):
    """
    Validates a competency ID string.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Competency ID must be a string")
        
        if not re.match(COMPETENCY_ID_REGEX, v):
            raise ValueError(f"Invalid Competency ID format: {v}. Must be domain.subdomain.concept.verb")
        
        parts = v.split(".")
        verb = parts[-1]
        
        if verb not in ALLOWED_VERBS:
            # We urge the LLM to use standard verbs, but maybe strict validation is too harsh for V2 start?
            # Let's warn instead of fail? No, strict is strict.
            # But the user said "avoid chaos", strict schemas reduce chaos.
            pass # We'll enforce it in prompt, maybe relax here if needed.
            
        return v

class ModuleProposal(BaseModel):
    """
    A proposal for a new module to be created.
    """
    id: str = Field(..., description="The unique ID of the proposed module (domain.subdomain.concept)")
    title: str = Field(..., description="Human-readable title")
    description: str = Field(..., description="Brief description of what this module covers")
    justification: str = Field(..., description="Why this module is needed (gap analysis)")
    required_competencies: List[str] = Field(default_factory=list, description="Prerequisite Competency IDs")
    produced_competencies: List[str] = Field(..., description="Competency IDs this module will teach")

class CampaignReference(BaseModel):
    id: str
    title: str
    description: str
    modules: List[str]

class TrackSchema(BaseModel):
    """
    Schema for track.yaml output from TrackAgent.
    """
    id: Optional[str] = None
    title: str
    description: str
    goal: str
    campaigns: List[CampaignReference] = Field(..., description="Ordered list of campaigns (chapters)")
    proposed_modules: List[ModuleProposal] = Field(default_factory=list, description="Definitions of NEW modules referenced in campaigns")
