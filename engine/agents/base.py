"""
Base Agent class for SFP Engine.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any

from openai import OpenAI
from engine.benchmarking.client import init_client, call_agent, PROMPTS_DIR
from engine.schemas.config import RunConfig

from datetime import datetime
import yaml

class BaseAgent(ABC):
    def __init__(self, config: RunConfig):
        self.config = config
        self.client = init_client()
        self.model = config.model
        self.last_metadata = {}
        self.last_prompt = ""
        self.last_context = ""
        self.last_instructions = ""
    
    def call(self, agent_name: str, context: str, instructions: str) -> str:
        """Call the LLM with the correct role separation.

        Args:
            agent_name:   Used for logging.
            context:      Dynamic per-request data (goal, learner profile) → user role.
            instructions: Static agent directives and output schema → system role.
        """
        self.last_context = context
        self.last_instructions = instructions
        # Keep last_prompt for backwards-compat logging (context + instructions combined)
        self.last_prompt = f"{instructions}\n\n{context}"

        output, usage = call_agent(self.client, agent_name, instructions, context, self.model)
        self.last_metadata = {
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "model": self.model,
            "usage": usage,
            "input_preview": context[:200] + "..."
        }
        return output

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """Execute the agent's main logic."""
        pass
    
    def save_step(self, run_dir: Path, step_name: str, prompt: str, output: str):
        """Save prompt, output, and generation log."""
        (run_dir / f"{step_name}_prompt.md").write_text(prompt)
        (run_dir / f"{step_name}_output.md").write_text(output)
        
        # Save generation log
        log_path = run_dir / f"{step_name}_generation_log.yaml"
        with open(log_path, "w") as f:
            yaml.dump(self.last_metadata, f)


