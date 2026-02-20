# Project Objective
Goal: {{ goal }}

# Learner Profile
{{ learner_summary }}

# Domain Context
This track may span multiple domains (e.g., computing, mathematics, science).
Do not constrain yourself to a single domain if the goal requires interdisciplinary knowledge.

# Execution Directives
- **Gap Identification**: Determine the **Conceptual Capabilities** required to reach the goal.
    -   **Concept Definition**: A concept is a "Textbook Chapter" (e.g., Recursion), not a "Tutorial Step" (e.g., Writing a function).
    -   **Environment Neutrality**: Do NOT reference programming languages, tools, or execution environments. Those are selected during assignment instantiation, not planning.
    -   It is allowed to propose new conceptual modules when required by the goal; these must still follow ontology and granularity rules.

- **Domain Taxonomy**:
    -   **Computing**: Use the 5 Disciplines (`fundamentals`, `systems`, `software_engineering`, `ai`, `applied`).
    -   **Other Domains**: Follow their native conceptual structure (e.g. `mathematics.calculus`). Do NOT force them into computing's taxonomy.

- **Module Granularity Rule**:
    -   Proposed modules must represent **stable, reusable concepts**.
    -   NEVER create modules for single tasks, exercises, or tool tutorials.
    -   **Litmus Test**: If a module name contains a specific tool name (e.g., `python_intro`), it is WRONG (unless specifically studying that tool's internals).
    -   CORRECT: `computing.fundamentals.iteration`
    -   WRONG: `computing.fundamentals.python_loops`

- **Strict Referencing**: IF A MODULE IS MISSING, do not invent content inline. Add it to the `proposed_modules` list.
- **Track ID**: MUST be **Goal-Based** (e.g., `data-science-bootcamp`), NOT a Domain ID.
- **Module IDs**: Define referenced IDs as `domain.subdomain.concept` (e.g., `computing.fundamentals.iteration`).

# Output Requirement
Produce a valid YAML `track.yaml` following the standard schema below. Ensure all strings are correctly quoted.

```yaml
{{ track_template }}
```
