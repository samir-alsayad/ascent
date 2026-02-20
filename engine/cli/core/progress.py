"""
Progress computation - Pure set algebra, no I/O.

The fundamental formula:
    progress = |Relevant ∩ Completed| / |Relevant|
"""

from typing import Set


def compute_progress(relevant: Set[str], completed: Set[str]) -> float:
    """
    Compute progress as intersection ratio.
    
    Args:
        relevant: Set of assignment IDs in scope
        completed: Set of completed assignment IDs
    
    Returns:
        Progress as float between 0.0 and 1.0
    """
    if not relevant:
        return 0.0
    
    intersection = relevant & completed
    return len(intersection) / len(relevant)


def format_progress(progress: float) -> str:
    """Format progress as percentage string."""
    return f"{progress * 100:.1f}%"
