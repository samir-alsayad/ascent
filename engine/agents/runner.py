import click
import yaml
import os
import shutil
import datetime
import subprocess
from pathlib import Path
from rich.console import Console

from engine.schemas.config import RunConfig
from engine.agents.track import TrackAgent
from engine.agents.campaign import CampaignAgent
from engine.agents.module import ModuleAgent
from engine.agents.assignment import AssignmentAgent
from engine.resolver.learner import LearnerProfile
from engine.utils.writer import ArtifactWriter

console = Console()

# Resolve absolute paths
RUNNER_DIR = Path(__file__).parent
ENGINE_DIR = RUNNER_DIR.parent
PROJECT_ROOT = ENGINE_DIR.parent

def _clean_code_fences(text):
    """Strip markdown code fences from LLM output."""
    import re
    pattern = r"```(?:\w+)?\n?(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

def _write_run_log(sandbox_dir, step_name, raw_output, rendered_context=None, rendered_instructions=None, metadata=None):
    """Append a generation step to the run log inside the sandbox."""
    log_path = Path(sandbox_dir) / "run_log.md"
    
    with open(log_path, "a") as f:
        f.write(f"\n# STEP: {step_name}\n")
        f.write(f"**Timestamp**: {datetime.datetime.now().isoformat()}  \n")
        
        if metadata:
            f.write("## Metadata\n")
            for k, v in metadata.items():
                f.write(f"- **{k.upper()}**: {v}\n")
        
        if rendered_context:
            f.write(f"\n## Context (User Data)\n")
            f.write("````markdown\n")
            f.write(rendered_context)
            f.write("\n````\n")
            
        if rendered_instructions:
            f.write(f"\n## System Prompt (Instructions)\n")
            f.write("````markdown\n")
            f.write(rendered_instructions)
            f.write("\n````\n")
        
        f.write(f"\n## Raw LLM Output\n")
        if raw_output:
            # Use 4 backticks to wrap potential triple backticks in output
            f.write("````yaml\n")
            f.write(raw_output)
            f.write("\n````\n")
        else:
            f.write("*(empty)*\n")
        f.write(f"\n---\n")

@click.group()
@click.option("--benchmark", is_flag=True, help="Run in benchmark mode (isolated sandbox)")
@click.option("--case-file", type=click.Path(exists=True), help="Path to benchmark case YAML")
@click.pass_context
def cli(ctx, benchmark, case_file):
    """Agent Orchestrator (Runner). Interacts with Agents to author curriculum."""
    ctx.ensure_object(dict)
    
    if case_file:
        benchmark = True
        
    ctx.obj['benchmark'] = benchmark
    ctx.obj['case_file'] = case_file
    
    if benchmark:
        if not case_file:
            console.print("[red]Error: --case-file required for benchmark mode.[/red]")
            exit(1)
            
        case_path = Path(case_file).resolve()
        case_data = yaml.safe_load(case_path.read_text())
        
        ctx.obj['goal'] = case_data.get('goal')
        ctx.obj['model'] = case_data.get('model')
        
        learner_state_ref = case_data.get('learner_state')
        run_name = case_data.get('run_name', 'benchmark_run')
        
        if not learner_state_ref:
            console.print("[red]Error: Case file missing 'learner_state'.[/red]")
            exit(1)
            
        # Sandbox generation
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        sandbox_dir = PROJECT_ROOT / "runs" / f"{timestamp}_{run_name}"
        
        school_sandbox = sandbox_dir / "school-content"
        learners_sandbox = sandbox_dir / "learners"
        
        school_sandbox.mkdir(parents=True, exist_ok=True)
        (school_sandbox / "domains").mkdir(exist_ok=True)
        (school_sandbox / "projects").mkdir(exist_ok=True)
        (school_sandbox / "exams").mkdir(exist_ok=True)
        
        learners_sandbox.mkdir(parents=True, exist_ok=True)
        local_user_dir = learners_sandbox / "local_user"
        local_user_dir.mkdir(exist_ok=True)
        
        # Inject mock state
        state_source_path = case_path.parent / learner_state_ref
        if not state_source_path.exists():
            state_source_path = PROJECT_ROOT / "runs" / learner_state_ref
            
        if state_source_path.exists():
            shutil.copy(state_source_path, local_user_dir / "student_state.yaml")
        else:
            console.print(f"[red]Could not locate mock state at {state_source_path}[/red]")
            exit(1)
            
        # Override environment for this runner process
        os.environ["SCHOOL_ROOT"] = str(school_sandbox)
        os.environ["STATE_ROOT"] = str(learners_sandbox)
        
        ctx.obj['school_root'] = school_sandbox
        ctx.obj['learner_state_path'] = local_user_dir / "student_state.yaml"
        console.print(f"[bold blue]Benchmark Sandbox active at:[/bold blue] {sandbox_dir}")
        
    else:
        # Production Mode
        ctx.obj['school_root'] = PROJECT_ROOT / "school-content"
        ctx.obj['learner_state_path'] = PROJECT_ROOT / "learners" / "local_user" / "student_state.yaml"
        
        # Make sure target dirs exist
        ctx.obj['school_root'].mkdir(exist_ok=True)
        (ctx.obj['school_root'] / "projects").mkdir(exist_ok=True)
        
        # Ensure env vars are set properly for underlying components
        os.environ["SCHOOL_ROOT"] = str(ctx.obj['school_root'])
        os.environ["STATE_ROOT"] = str(ctx.obj['learner_state_path'].parent.parent)

    # Initialize writer
    ctx.obj['writer'] = ArtifactWriter(str(ctx.obj['school_root']))
    
    # Load prompt version config
    prompts_config_path = PROJECT_ROOT / "benchmarks" / "prompts.yaml"
    if prompts_config_path.exists():
        ctx.obj['prompts'] = yaml.safe_load(prompts_config_path.read_text()) or {}
    else:
        ctx.obj['prompts'] = {}

@cli.command("track")
@click.option("--goal", help="Learning goal (required in production mode)")
@click.pass_context
def run_track(ctx, goal):
    """Generate a Track using the Track Agent."""
    benchmark = ctx.obj['benchmark']
    active_goal = ctx.obj.get('goal') if benchmark else goal
    model = ctx.obj.get('model') or os.getenv("OPENROUTER_MODEL", "qwen/qwen3-coder-next")
    
    if not active_goal:
        console.print("[red]Error: --goal is required.[/red]")
        exit(1)
        
    learner_state_path = ctx.obj['learner_state_path']
    if learner_state_path.exists():
        profile = LearnerProfile.load(learner_state_path)
    else:
        profile = LearnerProfile({"profile": {"description": "unknown"}})

    config = RunConfig(
        run_name="runner_track",
        model=model,
        learner_state={"knowledge": "resolved"},
        curriculum={"goal": active_goal}
    )
    
    agent = TrackAgent(config, template_path=ctx.obj['prompts'].get('track', 'track/v2_standard.md'))
    output = agent.run(active_goal, profile)
    cleaned = _clean_code_fences(output)
    
    try:
        data = yaml.safe_load(cleaned)
        tid = data.get('id') or "new_track"
        path = ctx.obj['writer'].write('track', cleaned, tid)
        if path:
            console.print(f"[green]Saved track to {path}[/green]")
    except Exception as e:
        console.print(f"[yellow]Failed to save track: {e}[/yellow]")
    console.print(output)
    
    # Write run log if in benchmark mode
    if benchmark and ctx.obj.get('school_root'):
        sandbox_dir = ctx.obj['school_root'].parent
        _write_run_log(sandbox_dir, "track", output,
            rendered_context=agent.last_context,
            rendered_instructions=agent.last_instructions,
            metadata={
                "model": model,
                "goal": active_goal,
                "case_file": ctx.obj.get('case_file', 'N/A'),
                "saved_to": str(path) if path else "FAILED"
            }
        )
        console.print(f"[dim]Run log updated at {sandbox_dir / 'run_log.md'}[/dim]")

@cli.command("campaign")
@click.option("--track-file", type=click.Path(exists=True), required=True)
@click.pass_context
def run_campaign(ctx, track_file):
    """Generate a Campaign using the Campaign Agent."""
    benchmark = ctx.obj['benchmark']
    model = ctx.obj.get('model') or os.getenv("OPENROUTER_MODEL", "qwen/qwen3-coder-next")
    
    content = Path(track_file).read_text()
    
    config = RunConfig(
        run_name="runner_campaign",
        model=model,
        learner_state={"knowledge": "resolved"},
        curriculum={"goal": ctx.obj.get("goal", "unknown")}
    )
    
    agent = CampaignAgent(config)
    output = agent.run(content)
    cleaned = _clean_code_fences(output)
    
    is_valid, err = _validate_artifact('campaign', cleaned)
    if not is_valid:
        console.print(f"[bold yellow]Validation Warning:[/bold yellow] {err}")
        
    try:
        data = yaml.safe_load(cleaned)
        cid = data.get('id')
        if cid:
            path = ctx.obj['writer'].write('campaign', cleaned, cid)
            if path:
                console.print(f"[green]Saved campaign to {path}[/green]")
    except Exception as e:
        console.print(f"[yellow]Failed to save campaign: {e}[/yellow]")
    console.print(output)

@cli.command("module")
@click.option("--campaign-file", type=click.Path(exists=True), required=True)
@click.pass_context
def run_module(ctx, campaign_file):
    """Generate a Module using the Module Agent."""
    benchmark = ctx.obj['benchmark']
    model = ctx.obj.get('model') or os.getenv("OPENROUTER_MODEL", "qwen/qwen3-coder-next")
    
    content = Path(campaign_file).read_text()
    
    config = RunConfig(
        run_name="runner_module",
        model=model,
        learner_state={"knowledge": "resolved"},
        curriculum={"goal": ctx.obj.get("goal", "unknown")}
    )
    
    agent = ModuleAgent(config)
    output = agent.run(content)
    cleaned = _clean_code_fences(output)
    
    is_valid, err = _validate_artifact('module', cleaned)
    if not is_valid:
        console.print(f"[bold yellow]Validation Warning:[/bold yellow] {err}")

    try:
        data = yaml.safe_load(cleaned)
        mid = data.get('id')
        if mid:
            path = ctx.obj['writer'].write('module', cleaned, mid)
            if path:
                console.print(f"[green]Saved module to {path}[/green]")
    except Exception as e:
        console.print(f"[yellow]Failed to save module: {e}[/yellow]")
    console.print(output)

@cli.command("assignment")
@click.option("--module-id", required=True)
@click.option("--assignment-id", required=True)
@click.option("--context", default="", help="Context/Goal for assignment")
@click.pass_context
def run_assignment(ctx, module_id, assignment_id, context):
    """Generate an Assignment using the Assignment Agent."""
    benchmark = ctx.obj['benchmark']
    model = ctx.obj.get('model') or os.getenv("OPENROUTER_MODEL", "qwen/qwen3-coder-next")
    
    # Needs CurriculumResolver to get the module target
    from engine.resolver.resolver import CurriculumResolver
    resolver = CurriculumResolver([ctx.obj['school_root']])
    module_data = resolver.get_module(module_id)
    
    if not module_data:
        console.print(f"[bold red]Error[/bold red]: Module '{module_id}' not found in `{ctx.obj['school_root']}`.")
        exit(1)
        
    config = RunConfig(
        run_name="runner_assignment",
        model=model,
        learner_state={"knowledge": "resolved"},
        curriculum={"goal": context or ctx.obj.get("goal", "unknown")}
    )
    
    agent = AssignmentAgent(config)
    output = agent.run(module_data, assignment_id, context)
    cleaned = _clean_code_fences(output)
    
    is_valid, err = _validate_artifact('assignment', cleaned)
    if not is_valid:
        console.print(f"[bold yellow]Validation Warning:[/bold yellow] {err}")
        
    try:
        path = ctx.obj['writer'].write('assignment', cleaned, assignment_id, parent_id=module_id)
        if path:
            console.print(f"[green]Saved assignment to {path}[/green]")
    except Exception as e:
        console.print(f"[yellow]Failed to save assignment: {e}[/yellow]")
    console.print(output)


def _validate_artifact(artifact_type, content, context=None):
    from engine.benchmarking.validators import StructuralValidator, VerificationValidator
    if context is None:
        context = {}
    if not content or len(content.strip()) < 10:
        return False, "Content is empty or too short."
        
    if artifact_type in ['track', 'campaign', 'module']:
        try:
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                return False, "YAML must be an object."
            if artifact_type == 'module':
                req = ['id', 'title', 'assignments', 'requires', 'produces']
            elif artifact_type == 'campaign':
                req = ['id', 'title', 'modules']
            elif artifact_type == 'track':
                req = ['id', 'title', 'campaigns']
            missing = [k for k in req if k not in data]
            if missing:
                return False, f"Missing keys: {', '.join(missing)}"
            return True, None
        except yaml.YAMLError as e:
            return False, f"Invalid YAML: {e}"
            
    elif artifact_type == 'assignment':
        validators = [StructuralValidator(), VerificationValidator()]
        failures = []
        for v in validators:
            if hasattr(v, 'name') and v.name == 'completability': continue
            res = v.validate(artifact_type, content, context)
            if not res.passed:
                failures.extend(res.reasons)
        if failures:
            return False, "; ".join(failures)
    return True, None

if __name__ == "__main__":
    cli()
