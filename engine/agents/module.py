from pathlib import Path
from typing import Union, Dict, Any
from engine.agents.generic import GenericTemplateAgent
from engine.schemas.schema import ModuleProposal

class ModuleAgent(GenericTemplateAgent):
    """
    Agent responsible for defining a specific Module contract.
    """
    
    def __init__(self, config):
        # Default template, though we might switch dynamically
        super().__init__(config, "module/v1_legacy.md")

    def run(self, input_data: Union[str, ModuleProposal], target_id: str = None) -> str:
        """
        Generate a module.yaml content based on input (campaign content OR proposal).
        """
        from pathlib import Path
        template_path = Path(__file__).parent / "templates" / "module.yaml"
        if not template_path.exists():
            raise FileNotFoundError(f"Module template not found: {template_path}")
        module_template = template_path.read_text()
        
        if isinstance(input_data, ModuleProposal):
            self.template_path = "module/v1_from_proposal.md"
            context = {
                "proposal": input_data,
                "module_template": module_template
            }
            # The serialized proposal is the dynamic user data
            context_str = str(input_data)
        else:
            self.template_path = "module/v1_legacy.md"
            context = {
                "campaign_content": input_data,
                "module_template": module_template,
                "target_id": target_id or "NEXT_AVAILABLE"
            }
            # The raw campaign content is the dynamic user data
            context_str = input_data
            
        instructions_str = self.render_prompt(**context)
        return self.call("module", context=context_str, instructions=instructions_str)
