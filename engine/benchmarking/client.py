"""
Shared utilities for the SFP benchmark engine.
"""

import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

# ── Paths ───────────────────────────────────────────────────────────────────

# We assume this file is in engine.benchmarking.client.py
# So parent is core, parent.parent is engine, parent.parent.parent is root
CORE_DIR = Path(__file__).parent
PKG_DIR = CORE_DIR.parent
ROOT_DIR = PKG_DIR.parent
SPEC_DIR = PKG_DIR / "agents" / "prompts" # Prompts inside package for now? Or keep external?
# Let's keep prompts in the package for self-containment, or config driven.
# For now, let's look for prompts in engine/spec for compatibility or move them.
# BETTER: Move prompts to engine/agents/prompts
PROMPTS_DIR = PKG_DIR / "agents" / "prompts"

RUNS_DIR = ROOT_DIR / "runs"
CURRICULUM_DIR = ROOT_DIR / "curriculum"


# ── LLM Client ─────────────────────────────────────────────────────────────

def init_client(env_path: Optional[Path] = None) -> OpenAI:
    """Initialize OpenRouter client."""
    # Try loading .env from root or engine/
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv(ROOT_DIR / "engine" / ".env") # Backwards compat
        load_dotenv(ROOT_DIR / ".env")
        
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        # Fallback to engine/key.txt for that one specific setup if needed
        key_path = ROOT_DIR / "engine" / "key.txt"
        if key_path.exists():
             api_key = key_path.read_text().strip()
    
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY in .env")
        sys.exit(1)
        
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


def get_model(override: Optional[str] = None) -> str:
    """Get the model name. CLI override > env var > default."""
    if override:
        return override
    return os.getenv("OPENROUTER_MODEL", "qwen/qwen3-coder-next")


def call_agent(client: OpenAI, agent_name: str, system_prompt: str, user_prompt: str, model: str) -> tuple[str, dict]:
    """Call an agent and return (content, usage).
    
    Args:
        system_prompt: The agent's instruction set (directives, schema, rules).
        user_prompt:   The dynamic per-request data (goal, learner context).
    """
    print(f"\n{'='*60}")
    print(f"  {agent_name.upper()} AGENT")
    print(f"  Model: {model}")
    print(f"{'='*60}")
    print(f"  Context: {user_prompt[:120]}{'...' if len(user_prompt) > 120 else ''}")
    print()

    if os.getenv("MOCK_LLM"):
        print("  [MOCK] Bypassing OpenAI Call. Returning dummy artifact.")
        return f"```yaml\nid: mock_{agent_name}\ntitle: Mock title\n```", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.0, # Fixed for benchmark stability
        max_tokens=4096,
    )

    result = response.choices[0].message.content
    usage = response.usage
    usage_dict = {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens
    }
    print(f"  Tokens: {usage.prompt_tokens} in / {usage.completion_tokens} out")
    print(f"  Done.\n")
    return result, usage_dict

