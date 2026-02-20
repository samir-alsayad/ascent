"""
Curriculum loaders - Load structure from /domains and /projects.
"""

from .modules import scan_modules
from .campaigns import scan_campaigns

__all__ = ["scan_modules", "scan_campaigns"]
