from typing import Dict, Any
from engine.agents.generic import GenericTemplateAgent
from engine.resolver.learner import LearnerProfile

class AssignmentAgent(GenericTemplateAgent):
    """
    Agent responsible for generating a specific Assignment instance (mission.md).
    Uses Jinja2 templates for prompt generation.
    """
    
    def __init__(self, config):
        # Hardcoded default template for now, could come from config
        super().__init__(config, "assignment/v1_standard.md")

    def run(self, module_data: Dict[str, Any], assignment_id: str, context: str) -> str:
        """
        Generate mission.md content using external template.
        """
        # Load profile to provide competence/fluency context
        profile = LearnerProfile(self.config.learner_state.model_dump())
        
        # Prepare context for Jinja2
        template_context = {
            "module_data": module_data,
            "assignment_id": assignment_id,
            "context": context,
            "learner_summary": profile.to_prompt_string()
        }
        
        # The dynamic user data: what the learner wants and who they are
        context_str = f"Assignment ID: {assignment_id}\nGoal: {context}\n\n{profile.to_prompt_string()}"
        
        instructions_str = self.render_prompt(**template_context)
        return self.call("assignment", context=context_str, instructions=instructions_str)
