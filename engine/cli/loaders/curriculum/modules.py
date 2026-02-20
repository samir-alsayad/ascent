"""
Module loader - Scans /domains for module.yaml files.
"""

import sys
import yaml
from typing import Dict, List

from engine.config import DOMAINS_PATH, SCHOOL_ROOT


def scan_modules() -> Dict[str, List[str]]:
    """
    Scan all module.yaml files in /domains.
    Returns: {module_id: [assignment_ids]}
    
    Strict validation: exits if domains path doesn't exist.
    """
    modules = {}
    
    if not DOMAINS_PATH.exists():
        print(f"[FATAL] Domains path does not exist: {DOMAINS_PATH}")
        print(f"[HINT] Expected school root: {SCHOOL_ROOT}")
        print("[HINT] Is SCHOOL_ROOT configured correctly?")
        sys.exit(1)
    
    for module_yaml in DOMAINS_PATH.rglob("module.yaml"):
        try:
            with open(module_yaml) as f:
                manifest = yaml.safe_load(f)
            
            module_id = manifest.get("id")
            assignments = manifest.get("assignments", [])
            
            if module_id:
                # Resolve local names to full IDs
                full_ids = [f"{module_id}.{a}" for a in assignments]
                modules[module_id] = full_ids
                print(f"[OK] Loaded module: {module_id} ({len(full_ids)} assignments)")
        except Exception as e:
            print(f"[ERR] Failed to load {module_yaml}: {e}")
    
    if not modules:
        print("[WARN] No modules found. Create module.yaml files in /domains.")
    
    return modules
