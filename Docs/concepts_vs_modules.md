# Open Discussion: Concept IDs vs Module IDs

**Status:** DEFERRED (V1 uses 1:1 mapping)

## The Question
Should we separate the abstract *concept* (what the learner knows) from the *module* (the teaching package that teaches it)?

## Current State (V1)
`computing.fundamentals.variables` is simultaneously:
- The **concept** (used in `tier_3_verified`, `requires`, `produces`)
- The **module** (a folder with `module.yaml` + assignments)

## Proposed Lightweight Separation
Same IDs, but treated differently:
- The Track Agent thinks in **concepts** ("the learner needs conditionals")
- The `module.yaml` declares `produces: [conditionals]` and `requires: [variables]`
- The Resolver maps concepts → modules
- A concept never gets its own file. It exists only as metadata on modules.

## Key Insight
- A **concept** has no written form. It's a label.
- A **module** IS the written form. It's a folder with assignments.
- An **assignment** is a single exercise inside that module.

## Verdict
Deferred. The 1:1 mapping works for V1. The `requires`/`produces` fields already exist in the module schema. We can flip to concept-aware resolution later without breaking anything.
