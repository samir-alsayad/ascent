# Course Creator Agent — Final Specification (v2)

---

## I. Architecture

### Two Graphs

| Graph | Purpose | Location | Mutable? |
|---|---|---|---|
| **Knowledge Graph** | "What exists to be learned" | `/domains` | Slow, versioned |
| **Execution Graph** | "What to study now, in what order" | `/tracks` | Fast, adaptive |

> **Rule**: Execution Graph may only **compose** Modules. It never creates new canonical content.

### Hierarchy

```
Domain → Discipline → Module → Assignment       (Knowledge Graph)
Track  → Campaign  → [Module references]         (Execution Graph)
```

| Level | Analogy | Bounded? | Goal-Driven? |
|---|---|---|---|
| **Track** | Degree program | No | Yes |
| **Campaign** | Semester | Soft | Yes |
| **Module** | Textbook chapter | Hard (5-20, versioned) | No |
| **Assignment** | Lab exercise | Atomic | No |

---

## II. Agent Architecture (Compiler Model)

```
Track Agent      → "You need 3 campaigns"           (High-level program)
  Campaign Agent → "Campaign 1 needs Modules A,B,C" (Dependency resolver)
    Module Agent → "Module A: 4 assignments needed"  (Interface contract)
      Assignment Agent → mission.md + reflection.md  (Compiled instance)
```

| Agent | Input | Output | Checks `/domains` for |
|---|---|---|---|
| **Track** | `(goal, learner_state)` | Campaign list | Existing tracks |
| **Campaign** | `(sub-goal, module graph)` | Ordered module sequence | Existing modules + `produces:` |
| **Module** | `(concept, discipline)` | `module.yaml` + assignment specs | Existing modules/concepts |
| **Assignment** | `(module contract, prerequisites)` | `mission.md` + `reflection.md` + `verification.*` | Existing assignments |

**Deduplication**: The filesystem IS the deduplication index. Each agent scans `/domains` before creating anything new.

**Benchmark order**: Assignment → Module → Campaign → Track (bottom-up).

---

## III. Module Contract (`module.yaml`)

```yaml
id: computing.networking.tcp_handshake
title: "TCP 3-Way Handshake"
version: 1

requires:
  - computing.networking.ip_basics
  - computing.fundamentals.binary_representation

produces:
  - computing.networking.tcp_handshake.identify_packets
  - computing.networking.tcp_handshake.trace_sequence
  - computing.networking.tcp_handshake.predict_state

assignments:
  - a01_capture_handshake
  - a02_label_sequence
  - a03_predict_state
```

### Competency ID Format
```
<domain>.<discipline>.<concept>.<operation>
```

Controlled verbs: `identify`, `trace`, `construct`, `transform`, `predict`, `diagnose`, `formalize`, `apply`

Regex: `^[a-z]+(\.[a-z_]+){3}$`

---

## IV. Assignment Structure (3 Files)

```
a01_[name]/
├── mission.md        # Context + Task (self-contained)
├── reflection.md     # Comprehension questions (agent-generated)
└── verification.*    # Domain-appropriate proof
```

### `mission.md` Template (5 Sections)
1. **Context & Goal** — purpose, concept being mastered
2. **The Challenge** — must specify CREATE or TRANSFORM action (never "understand" or "explore")
3. **Requirements** — acceptance criteria
4. **Expected Invariants** — properties that must hold
5. **Verification** — how learner confirms success

### `reflection.md` — Agent fills `{{ Title }}` + 3 questions
Allowed question types only:

| Type | Pattern |
|---|---|
| **Reconstruction** | "Rebuild/explain the concept without looking" |
| **Perturbation** | "What breaks if X changes?" |
| **Transfer** | "Apply this to a different system" |

### `verification.*` — Domain-agnostic
- Computing: `.py`, `.sh`
- Other domains: `.md` (rubric, expected answer, checklist)

### `generation_log.yaml` — Emitted per assignment
```yaml
source_module: computing.networking.tcp_handshake
assumed_prerequisites:
  - computing.networking.ip_basics
target_competency: tcp_handshake.trace_sequence
why_atomic: "Single packet capture exercise"
```

---

## V. The Eight Invariants

| # | Invariant | Formal |
|---|---|---|
| 1 | Goal-Aligned | `Goal(Track) = G` |
| 2 | State-Aware | `Output depends on U` |
| 3 | Min Cognitive Entropy | `Complexity(n+1) ≤ f(Mastery(n))` |
| 4 | Verifiable | Each assignment → evidence |
| 5 | Transferable Structure | Builds reusable mental models |
| 6 | Preserves Agency | Learner decides |
| 7 | **Completable** | **mission.md is self-contained given prior assignments** |
| 8 | **Declared Prerequisites** | **Modules declare `requires`/`produces`; no other layer introduces deps** |

**Meta**: Never optimize engagement over actual capability gain.

---

## VI. Next Steps

1. **Draft Assignment Agent system prompt**
2. **Set up OpenRouter pipe** (simple Python script)
3. **Run 3 manual test cases**, review each output
