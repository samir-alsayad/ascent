from engine.agents.generic import GenericTemplateAgent
from engine.resolver.learner import LearnerProfile

class TrackAgent(GenericTemplateAgent):
    """
    Agent responsible for high-level curriculum planning (Tracks).
    """
    
    def __init__(self, config, template_path="track/v2_standard.md"):
        super().__init__(config, template_path)

    def run(self, goal: str, learner_profile: LearnerProfile) -> str:
        """
        Generate a track.yaml content based on the goal and learner state.
        """
        from pathlib import Path
        
        template_path = Path(__file__).parent / "templates" / "track.yaml"
        if not template_path.exists():
            raise FileNotFoundError(f"Track template not found: {template_path}")
            
        track_template = template_path.read_text()
        
        # Render Context (user role: dynamic per-request data)
        context_templ = self.env.get_template("shared/context.md")
        context_str = context_templ.render(
            goal=goal,
            learner_summary=learner_profile.to_prompt_string()
        )
        
        # Render Instructions (system role: static agent directives + schema)
        instructions_str = self.render_prompt(
            track_template=track_template
        )
        
        return self.call("track", context=context_str, instructions=instructions_str)
