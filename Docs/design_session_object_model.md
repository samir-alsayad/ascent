# Architectural Design Session — Object Model & Naming

> Distilled from design conversation on 2026-02-20.

---

## Key Insight: Two Layers, Not One

The system is **two tightly coupled but independent layers**:

| Layer | Purpose | AI-Dependent? |
|---|---|---|
| **Pedagogical State** (Layer 1) | Records learning reality — concepts, evidence, objectives | No |
| **Synthesis Engine** (Layer 2) | Generates materials — prompts, agents, benchmark harness | Yes (replaceable) |

**Invariant**: If Layer 2 is deleted, nothing about the learner's progress is lost.

---

## The Six Core Objects

The system requires exactly **six objects**. Everything else (tracks, campaigns, programs, semesters) is a view, not ontology.

### Stored Objects

| # | Object | Answers | Mutable? |
|---|---|---|---|
| 1 | **Concept** | "What is true?" | Rarely |
| 2 | **Module** | "How can this be taught reliably?" | Versioned |
| 3 | **Assignment** | "What must the learner do to prove capability?" | Often |
| 4 | **Evidence** (Learner State) | "What has happened?" | Constantly |
| 5 | **Objective** (Intent Anchor) | "Why are we learning this?" | Per-request |

### Computed (Not Stored)

| # | Object | Answers |
|---|---|---|
| 6 | **Resolver** | "What should happen next?" — `next(P, L) = min { u ∈ P | u ∉ L ∧ deps(u) ⊆ L }` |

---

## Object Relationships

```
Concepts are referenced by → {Modules, Assignments}
Modules are selected by    → Learning Strategies (ephemeral)
Strategies serve           → Objectives
Evidence evaluates against → Assignments
```

Concepts are a **shared coordinate system**, not a superclass. No inheritance — only binding.

---

## Critical Separations

### Concept vs Module vs Assignment

| Layer | Exists Without School? | Contains Text? | Learner-Specific? |
|---|---|---|---|
| Concept | Yes | Minimal (ontological statement) | No |
| Module | No | Some (pedagogical envelope) | No |
| Assignment | No | Yes (proof obligation) | No |
| Evidence | No | Little | Yes |

### Track vs Campaign (Collapsed)

Old terms like Track/Campaign/Program are **not separate object types**. They are all:

> Ordered subsets of Modules chosen to satisfy an Objective.

The difference between "semester" and "degree" is just length. No new invariant is introduced.

---

## The Containment Hierarchy (Corrected)

```
Objective (declares intent)
  └── Learning Strategy (ephemeral, ordered modules)
        └── Module (from /domains, stable)
              └── Assignment (instantiated proof task)
```

**Tracks do NOT contain Modules.** If Track exists at all, it is a goal container. Only Campaigns/Strategies touch Modules.

---

## Just-In-Time Learning Model

This is **not a curriculum system**. It is an **objective-driven resolver**.

```
declare_intent()
→ compute_delta()        # Required − Verified = Missing
→ map_to_concepts()      # Library lookup
→ instantiate_proofs()   # Create assignments
→ verify()               # Collect evidence
→ update_state()         # Commit capability
→ stop                   # Idle until next intent
```

No background progression. No "keep learning." No timeline.

**Capability sets are computed, not stored.** The system derives the minimal knowledge slice at runtime.

---

## The Three Learning Layers (Axiom)

| Layer | Definition | Gap Means |
|---|---|---|
| **L1 — Domain Knowledge** | "I understand division" | Teach the concept |
| **L2 — Computational Formalization** | "I can make division a step-by-step procedure" | Teach the algorithm (the *bridge*) |
| **L3 — Environment Fluency** | "I can encode that procedure in Python" | Teach the syntax |

---

## Filesystem Reflection

```
/school-core/            ← Layer 1 (authoritative)
    domains/             # Concepts + Modules
    learners/            # Evidence
    objectives/          # Intent anchors

/synthesis-engine/       ← Layer 2 (replaceable)
    prompts/
    agents/
    benchmarks/
    runs/
```

Work projects (repos, tools) live **outside** the school — they *attach* to learning strategies but never contain curriculum.

---

## Naming Decision (Open)

"School of First Principles" communicates **institution**, but the system is a **capability resolver**. Name should reflect computation, not education. Decision deferred.
