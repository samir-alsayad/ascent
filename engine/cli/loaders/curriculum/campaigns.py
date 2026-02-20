"""
Campaign loader - Scans /projects for campaign.yaml files.
"""

import sys
import yaml
from typing import Dict, List

from engine.config import PROJECTS_PATH, SCHOOL_ROOT


from .modules import scan_modules

def scan_campaigns() -> Dict[str, List[str]]:
    """
    Scan all campaign.yaml files in /projects.
    Returns: {campaign_id: [assignment_ids]}
    
    Strict validation: exits if projects path doesn't exist.
    """
    campaigns = {}
    
    if not PROJECTS_PATH.exists():
        print(f"[WARN] Projects path does not exist: {PROJECTS_PATH}")
        print(f"[HINT] Expected school root: {SCHOOL_ROOT}")
        print("[HINT] Create /projects directory or check SCHOOL_ROOT.")
        return campaigns
        
    modules_map = scan_modules()

    for campaign_yaml in PROJECTS_PATH.rglob("campaign.yaml"):
        try:
            with open(campaign_yaml) as f:
                manifest = yaml.safe_load(f)
            
            campaign_id = manifest.get("id")
            assignments = manifest.get("assignments", [])
            module_refs = manifest.get("modules", [])
            
            for m_ref in module_refs:
                # Handle both string ID and dict object
                if isinstance(m_ref, dict):
                    mid = m_ref.get("id")
                else:
                    mid = m_ref
                
                if mid in modules_map:
                    assignments.extend(modules_map[mid])
                else:
                    print(f"[WARN] Campaign {campaign_id} references missing module: {mid}")
            
            if campaign_id:
                campaigns[campaign_id] = assignments
                print(f"[OK] Loaded campaign: {campaign_id} ({len(assignments)} assignments)")
        except Exception as e:
            print(f"[ERR] Failed to load {campaign_yaml}: {e}")
    
    if not campaigns:
        print("[WARN] No campaigns found. Create campaign.yaml files in /projects.")
    
    return campaigns
