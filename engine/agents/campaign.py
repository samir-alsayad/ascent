from engine.agents.generic import GenericTemplateAgent

class CampaignAgent(GenericTemplateAgent):
    """
    Agent responsible for breaking down a Track into ordered Modules (Campaigns).
    """
    
    def __init__(self, config):
        super().__init__(config, "campaign/v1_standard.md")

    def run(self, track_content: str) -> str:
        """
        Generate a campaign.yaml content based on the track definition.
        """
        from pathlib import Path
        
        template_path = Path(__file__).parent / "templates" / "campaign.yaml"
        if not template_path.exists():
            raise FileNotFoundError(f"Campaign template not found: {template_path}")
            
        campaign_template = template_path.read_text()
        
        instructions_str = self.render_prompt(
            track_content=track_content,
            campaign_template=campaign_template
        )
        # The raw track content is the dynamic user data; instructions are the agent directives
        return self.call("campaign", context=track_content, instructions=instructions_str)
