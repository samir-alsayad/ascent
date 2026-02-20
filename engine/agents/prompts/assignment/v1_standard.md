# Target Assignment Scope
ID: {{ assignment_id }}
Parent Module: {{ module_data.id }}
Context: {{ context }}

# Learner Profile
{{ learner_summary }}

# Module Contract
- **Prerequisites**: {{ module_data.requires | join(', ') }}
- **Learning Objectives**: {{ module_data.produces | join(', ') }}

# Execution Strategy (The 3 Layers)
Compare the **Learner Profile** against the **Module Contract**:

1.  **Scenario A: Formalization Gap (Layer 2)**
    *   *Condition*: User lacks the *Concept* or *Algorithm*.
    *   *Action*: Teach the logic itself. Use the environment only as a whiteboard.
    *   *Focus*: Step-by-step logic, mental models, pseudo-code.

2.  **Scenario B: Translation/Fluency Gap (Layer 3)**
    *   *Condition*: User HAS the *Concept* (in Profile) but lacks the *Environment* (in Context/Fluency).
    *   *Action*: **Do NOT re-teach the concept.** Focus entirely on **Syntax Mapping**.
    *   *Prompt*: "You generally know how to do X. Here is how we say X in [Language]."

# Design Constraints
1.  **Self-Contained**: The assignment must be small and incremental.
2.  **Atomic**: Focus exactly on the identified gap.
3.  **Observable**: Verification must require execution.

# Output Format
Generate a `mission.md` file with these EXACT headers:
1. **Context** (Mission theme and background)
2. **Challenge** (The specific task the learner must perform)
3. **Requirements** (Detailed acceptance criteria)
4. **Invariants** (Constraints, tool policies)
5. **Verification** (Executable instructions or scripts)
6. **Reflection** (Three standard reflection probes)
