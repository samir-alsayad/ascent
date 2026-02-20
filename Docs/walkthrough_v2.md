# V2 Learning OS: Repository Architecture & Orchestration

We have successfully completed the fundamental restructure of the Learning OS. The project is now organized into a "Hub" model that cleanly separates code, content, user state, and test inputs.

## 🏗️ The New Architecture

```
school/
├── engine/            # Core Python Package
│   ├── cli/           # CLI Commands & Logic
│   ├── agents/        # LLM Agents (Track, Campaign, Module, Assignment)
│   │   ├── prompts/   # Versioned .md prompt templates
│   │   └── templates/ # Structural YAML schemas
│   └── schemas/       # Pydantic models (Config, LearnerState)
├── school-content/    # The Curriculum (Git-managed)
│   └── projects/      # Tracks & Campaigns
├── learners/          # Production Learner State
│   └── local_user/    # Your 3-tier student_state.yaml
├── benchmarks/        # Testing & Verification
│   ├── cases/         # Benchmark definitions (goal + profile)
│   ├── profiles/      # Mock learner archetypes (e.g. math_expert)
│   └── prompts.yaml   # Global prompt version control
└── runs/              # Isolated execution sandboxes (gitignored)
```

## 🚀 Orchestration & Benchmarking

The new `engine.agents.runner` (The Orchestrator) allows you to simulate the entire learning pipeline in isolated sandboxes.

### Running a Benchmark
Execute a benchmark case in an isolated environment:
```bash
python3 -m engine.agents.runner --benchmark --case-file benchmarks/cases/case_b_quadratic_with_exam.yaml track
```

### 📋 Rich Audit Logs
Every benchmark run now generates a `run_log.md` in its sandbox folder. This log provides a full trace of:
- **Metadata**: Model used, goal, case file, and output path.
- **Context**: Exactly what Goal and Learner Profile were sent to the LLM.
- **System Prompt**: The specific version of the instructions used.
- **Raw Output**: The full response from the LLM for inspection.

### 🎛️ Dynamic Prompt Control
You no longer need to touch Python code to test new prompts. Use `benchmarks/prompts.yaml` to point the system to different template versions globally.

## 💎 Key Features Implemented
- **3-Tier Competence Model**: Enforced distinction between self-reported (T1), practiced (T2), and verified (T3) knowledge.
- **Learner-Aware Planning**: Agents now respect Tier 3 verified knowledge and skip material the learner already knows.
- **Project Isolation**: Benchmarks run in unique `runs/` folders, protecting your production `school-content` and `learners` data.
- **Clean Naming**: Campaigns now follow the `c01_slug` convention automatically.
