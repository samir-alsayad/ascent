from pathlib import Path
from typing import Any
from jinja2 import Environment, FileSystemLoader
from engine.agents.base import BaseAgent

class GenericTemplateAgent(BaseAgent):
    """
    Agent that uses Jinja2 templates for prompts.
    """
    def __init__(self, config, template_path: str):
        super().__init__(config)
        self.template_path = template_path
        # Prompts are now stored alongside the agents in engine/agents/prompts
        base_dir = Path(__file__).parent / "prompts"
        self.env = Environment(loader=FileSystemLoader(str(base_dir)))
        
    def render_prompt(self, **context) -> str:
        template = self.env.get_template(self.template_path)
        return template.render(**context)
    
    def run(self, *args, **kwargs) -> Any:
        # subclasses must implement this or we could make a fully generic runner
        pass
