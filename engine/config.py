"""
Configuration - All paths and constants.
"""

from pathlib import Path
import os

# The Engine Root (where this code lives)
ENGINE_ROOT = Path(__file__).parent

# The School Root (Immutable Curriculum)
# Default to ../school-content
school_env = os.getenv("SCHOOL_ROOT")
SCHOOL_ROOT = Path(school_env) if school_env else ENGINE_ROOT.parent / "school-content"

# The State Root (Mutable Learner Data)
# Default to ../learners
state_env = os.getenv("STATE_ROOT")
STATE_ROOT = Path(state_env) if state_env else ENGINE_ROOT.parent / "learners"

# Curriculum Paths
DOMAINS_PATH = SCHOOL_ROOT / "domains"
PROJECTS_PATH = SCHOOL_ROOT / "projects"

# Helper to get a specific learner's state file
def get_learner_state_path(learner_id: str = "local_user") -> Path:
    return STATE_ROOT / learner_id / "student_state.yaml"

