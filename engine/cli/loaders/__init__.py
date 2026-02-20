"""
Loaders package - All I/O operations.

Subpackages:
  - curriculum: modules, campaigns (from /domains, /tracks)
  - state: ledger (from /learner_state)
"""

from .curriculum import scan_modules, scan_campaigns
from .state import load_ledger

__all__ = ["scan_modules", "scan_campaigns", "load_ledger"]
