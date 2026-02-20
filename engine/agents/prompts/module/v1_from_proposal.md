# Module Proposal (Strict Mode)
Title: {{ proposal.title }}
ID: {{ proposal.id }}
Description: {{ proposal.description }}
Justification: {{ proposal.justification }}

# Requirements
- **Prerequisites**: {{ proposal.required_competencies }}
- **Produced**: {{ proposal.produced_competencies }}

# Execution Directives
- **Ontology Only**: Define the **Concept**, not the **Tool**. The ID must be tool-agnostic.
    -   **Litmus Test**: If a module name contains a specific tool name (e.g., `python_intro`), it is WRONG (unless specifically studying that tool's internals).
    -   CORRECT: `computing.fundamentals.iteration`
    -   WRONG: `computing.fundamentals.python_loops`
- **Context Awareness**: Check `requires`. If the user has conceptual mastery, the *Assignments* (generated later) will focus on syntax. The *Module* stays the same.
- **Taxonomy**:
    -   **Computing**: Use the 5 Disciplines (`fundamentals`, `systems`, `software_engineering`, `ai`, `applied`).
    -   **Other Domains**: Follow their native conceptual structure.
    1. `computing.fundamentals`
    2. `computing.systems`
    3. `computing.software_engineering`
    4. `computing.ai`
    5. `computing.applied`
- **Assignment Count**: STRICTLY 5-20 assignments.
- **Template**: Use the provided template EXACTLY.

# Output Template
{{ module_template }}
