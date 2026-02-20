# Domain Context
This track may span multiple domains (e.g., computing, mathematics, science).
Do not constrain yourself to a single domain if the goal requires interdisciplinary knowledge.

# Execution Directives

## 1. Gap Analysis — Transformation, Not Syllabus
- Your job is to identify **what the learner cannot yet DO**, not to design a complete course.
- Ask: "What transformation is missing between what the learner already knows and what the goal requires?"
- A concept is a "Textbook Chapter" (e.g., Recursion), NOT a "Tutorial Step" (e.g., Writing a function).
- **Environment Neutrality**: Do NOT reference programming languages, tools, or execution environments in module IDs. Those are selected during assignment instantiation.
- **Gap Minimality**: Include the FEWEST modules necessary. Every module must be justified by a concrete capability the learner currently lacks. If you cannot articulate what new capability a module provides, remove it.

## 2. Learner-Aware Planning
- **CRITICAL**: If a module ID appears in the learner's **Tier 3 (Verified)** list, DO NOT include it in any campaign. That concept is already proven.
- **DOMAIN CLOSURE**: If the learner has verified mastery of a domain's required competency for this goal, treat that domain as **CLOSED**. Do NOT introduce adjacent, review, or supplementary modules in that domain unless the goal *explicitly* demands deeper theory. "Review" is an assignment-level adaptation, never a structural module.
- **REFERENCE ≠ INCLUSION**: Tracks list what must be LEARNED, not what must be USED. If a verified concept is needed during execution, assignments may reference it — but it must NOT appear as a module in the track.
- If a module ID appears in **Tier 1 (Claims)**, you MAY skip introductory coverage but should still include it if it is a critical dependency for later modules.
- If no learner data is provided, assume a complete beginner.
- **Anti-pattern**: Do NOT front-load recap campaigns. If knowledge is verified, the track starts at the first UNKNOWN capability.

## 3. Module Legitimacy Test
Before emitting ANY module ID, it must pass ALL of these checks:

1. **New Abstraction**: Does this module teach a mental model the learner does not yet possess? "Using", "applying", "extending", "handling edge cases", or "implementing" an existing concept are NEVER valid reasons to create a module. Those are assignment-level concerns.
2. **Library Independence**: Would this module exist in a universal knowledge library *before* this learner or this goal existed? If it only makes sense in the context of completing this specific task, it is not a module — it is an assignment.
3. **Non-Redundancy**: Is this module NOT a subset or trivial variant of a verified competency? (e.g., `complex_numbers` is NOT a new computing fundamental if the learner already knows algebra — it is a datatype instantiation, handled in assignments.)
4. **Necessity**: Can the goal be achieved WITHOUT this module? If yes, remove it.

## 4. Domain Taxonomy
- **Computing**: Use the 5 Disciplines (`fundamentals`, `systems`, `software_engineering`, `ai`, `applied`).
- **Other Domains**: Follow their native conceptual structure (e.g., `mathematics.algebra`). Do NOT force them into computing's taxonomy.

## 5. Module Granularity Rule
- Modules must represent **stable, reusable concepts** worth 5-20 assignments each.
- NEVER create modules for single tasks, exercises, or tool tutorials.
- If two potential modules would each have fewer than 5 assignments, **merge them** into one broader module.
- **Litmus Test**: If a module name contains a specific tool name (e.g., `python_intro`), it is WRONG (unless specifically studying that tool's internals).
  - CORRECT: `computing.fundamentals.iteration`
  - WRONG: `computing.fundamentals.python_loops`

## 6. Campaign Rules
- A campaign is a **chapter** of 2-5 related modules that share a theme.
- **Campaign IDs**: Use the format `c01_descriptive_slug` (numbered, lowercase, underscores). Example: `c01_computational_expression`.
- **Campaign Titles**: Use a clear, human-readable chapter title. Example: "Expressing Mathematics Computationally".
- Campaigns should be ordered so that each campaign's modules only depend on modules from earlier campaigns.

## 7. Module IDs
- Format: `domain.subdomain.concept` (e.g., `computing.fundamentals.iteration`).
- Track IDs MUST be **Goal-Based** (e.g., `quadratic-roots-with-python`), NOT Domain IDs.

# Output Requirement
Produce a valid YAML `track.yaml` following the standard schema below. Ensure all strings are correctly quoted. Do NOT include module definitions — only reference module IDs.

```yaml
{{ track_template }}
```
