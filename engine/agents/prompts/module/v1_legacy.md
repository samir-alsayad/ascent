# Source Campaign Artifact
{{ campaign_content }}

# Project Objectives
1. Review the campaign's module list.
2. Select the implementation target: **{{ target_id }}**.
3. Implement the full contract for this module.

# Execution Directives
- **Ontology Only**: Define the **Concept**, not the **Tool**. The ID must be tool-agnostic.
    -   **Litmus Test**: If a module name contains a specific tool name (e.g., `python_intro`), it is WRONG.
    -   CORRECT: `computing.fundamentals.iteration`
    -   WRONG: `computing.fundamentals.python_loops`
- **Taxonomy**: Use strict disciplines for computing: `computing.fundamentals`, `computing.systems`, etc.
- **Assignment Count**: STRICTLY 5-20 assignments.
- **Template Schema**: Follow the template EXACTLY.

# Output Template
{{ module_template }}
