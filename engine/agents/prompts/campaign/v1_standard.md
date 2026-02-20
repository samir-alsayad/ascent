# Source Track Artifact
{{ track_content }}

# Project Objectives
1. Analyze the track's progression.
2. Identify the FIRST campaign that needs to be created.
3. Breakdown that campaign into specific Modules.

# Execution Constraints
- **Strict Referencing**: You MUST reference existing modules or propose new ones via `proposed_modules`.
- **Atomic Modules**: Ensure modules are small, focused, and represent a single learning step.
- **Competency Mapping**: Each module must clearly state what it `requires` and what it `produces`.

# Output Requirement
Produce the `campaign.yaml` artifact. Ensure valid YAML syntax and double-quoted strings.

Your output MUST strictly follow this exact structural template:
```yaml
{{ campaign_template }}
```
