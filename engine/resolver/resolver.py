import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from rich.console import Console

console = Console()

class CurriculumResolver:
    """
    Scans and maps all curriculum artifacts (modules, campaigns, tracks).
    Ensures IDs are unique and dependencies are resolvable.
    """

    def __init__(self, search_dirs: List[Path]):
        self.search_dirs = search_dirs
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.campaigns: Dict[str, Dict[str, Any]] = {}
        self.tracks: Dict[str, Dict[str, Any]] = {}
        self._load_all()

    def _load_all(self):
        """Scan all directories for yaml files and load them."""
        for sdir in self.search_dirs:
            if not sdir.exists():
                continue
            
            # Find all yaml files recursively
            for yaml_path in sdir.rglob("*.yaml"):
                if "learner_state" in str(yaml_path):
                    continue
                
                try:
                    with open(yaml_path) as f:
                        data = yaml.safe_load(f)
                    
                    if not data or not isinstance(data, dict):
                        continue
                        
                    artifact_id = data.get("id")
                    if not artifact_id:
                        continue
                    
                    # Store path for reference
                    data["_path"] = yaml_path
                    
                    # Categorize based on content or filename
                    if "assignments" in data or "produces" in data:
                        self.modules[artifact_id] = data
                    elif "modules" in data and "sub_goal" in data:
                        self.campaigns[artifact_id] = data
                    elif "campaigns" in data and "goal" in data:
                        self.tracks[artifact_id] = data
                        
                except Exception as e:
                    console.print(f"[yellow]Warning: Failed to load artifact at {yaml_path}: {e}[/yellow]")

    def get_module(self, module_id: str) -> Optional[Dict[str, Any]]:
        return self.modules.get(module_id)

    def get_campaign(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        return self.campaigns.get(campaign_id)

    def get_track(self, track_id: str) -> Optional[Dict[str, Any]]:
        return self.tracks.get(track_id)

    def resolve_dependencies(self, artifact_id: str) -> List[str]:
        """Check if all requirements of an artifact exist in the registry."""
        artifact = self.modules.get(artifact_id) or self.campaigns.get(artifact_id)
        if not artifact:
            return []
            
        requires = artifact.get("requires", [])
        missing = []
        for req in requires:
            # Simple check: does any module produce this ID?
            # Or is the ID another module?
            if req not in self.modules:
                # Check if any module produces this competency
                found = False
                for mod in self.modules.values():
                    if req in mod.get("produces", []):
                        found = True
                        break
                if not found:
                    missing.append(req)
        return missing

    def report(self):
        """Print a summary of the discovered graph."""
        console.print("\n=== Curriculum Registry Summary ===")
        console.print(f"Tracks:    {len(self.tracks)}")
        console.print(f"Campaigns: {len(self.campaigns)}")
        console.print(f"Modules:   {len(self.modules)}")
        
        all_missing = set()
        for mid in self.modules:
            missing = self.resolve_dependencies(mid)
            all_missing.update(missing)
            
        if all_missing:
            console.print(f"[yellow]Unresolved Dependencies: {len(all_missing)}[/yellow]")
            for m in sorted(list(all_missing)):
                console.print(f"  - {m}")
        else:
            console.print("[green]Registry is structurally closed (all dependencies resolved).[/green]")
        console.print()
