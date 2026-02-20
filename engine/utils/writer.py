from pathlib import Path
import yaml
import os

class ArtifactWriter:
    def __init__(self, root_dir: str):
        self.root = Path(root_dir)
        
    def write(self, artifact_type: str, content: str, artifact_id: str = None, parent_id: str = None):
        """
        Write generation artifact to the correct path in the School structure.
        
        Args:
            artifact_type: 'track', 'campaign', 'module', 'assignment'
            content: The string content (YAML or Markdown)
            artifact_id: The ID of the artifact (optional if parseable from content)
            parent_id: Required for assignments (the module ID)
        """
        
        # Try to parse ID from content if not provided (for YAML artifacts)
        if not artifact_id and artifact_type in ['track', 'campaign', 'module']:
            try:
                data = yaml.safe_load(content)
                artifact_id = data.get('id')
            except:
                pass
        
        if not artifact_id and artifact_type != 'track': # Track might not have ID in yaml
             raise ValueError(f"Artifact ID required for {artifact_type}")

        if artifact_type == 'track':
            # Tracks live in projects/ (Execution Layer)
            # ID: quadratic-roots-calculator -> projects/quadratic-roots-calculator/track.yaml
            if not artifact_id: artifact_id = "unknown_track"
            rel_path = artifact_id.replace('.', '/')
            path = self.root / "projects" / rel_path / "track.yaml"
            
        elif artifact_type == 'campaign':
            # Campaigns live in projects/ (Execution Layer)
            # ID: applied-linear-algebra.with-python -> projects/applied-linear-algebra/with-python/campaign.yaml
            rel_path = artifact_id.replace('.', '/')
            path = self.root / "projects" / rel_path / "campaign.yaml"
            
        elif artifact_type == 'module':
            # ID: computing.python.basics -> domains/computing/python/basics/module.yaml
            rel_path = artifact_id.replace('.', '/')
            path = self.root / "domains" / rel_path / "module.yaml"
            
        elif artifact_type == 'assignment':
            # ID: a01_intro
            # Parent: computing.python.basics
            if not parent_id:
                raise ValueError("Parent Module ID required for assignment")
            mod_path = parent_id.replace('.', '/')
            path = self.root / "domains" / mod_path / "assignments" / artifact_id / "mission.md"
            
        else:
            raise ValueError(f"Unknown artifact type: {artifact_type}")
            
        # Ensure directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        path.write_text(content)
        print(f"[Writer] Saved {artifact_type} ({artifact_id}) to {path}")
        return path
