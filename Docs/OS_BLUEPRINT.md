# Implementation Plan: The School of First Principles
## Architectural Vision: The Learning Operating System

The School is designed as a system that cleanly separates **Knowledge** (Taxonomy) from **Execution** (Projects). It functions like a package manager for learning.

---

## 1. The Separation of Concerns

### A. The Knowledge Graph (`/domains`)
*   **Purpose**: Static Curriculum. Answers "What exists to be learned?"
*   **Structure**: Stable, taxonomic, domain-driven.
*   **Invariants**: Domains do NOT care about projects. They are libraries of atomic learning atoms.

### B. The Execution Graph (`/projects`)
*   **Purpose**: Work Execution. Answers "What am I building?" and "What is required?"
*   **Structure**: Dynamic, goal-driven.
*   **Mechanism**: Projects define **Campaigns**, which are curated playlists of atomic assignments from the Knowledge Graph.

### C. The State Layer (`/learner_state`)
*   **Purpose**: Progress Tracking.
*   **Mechanism**: Tracks progress by **Assignment ID**.
*   **Metrics** (computed by CLI, NOT stored yet):
    *   **Assignment**: Binary/Weighted completion.
    *   **Module**: `completed / total` (total from `/domains`, not ledger).
    *   **Project**: Aggregation of linked tasks.

> **Fundamental Invariant**:
> The ledger **never describes the curriculum**. It only describes the learner's interaction with it.
> *   All **structure** comes from `/domains`.
> *   All **relevance** comes from `/projects`.
> *   All **completion** comes from `/learner_state`.
> *   The CLI **reconciles** them.

---

## 1.1 Canonical Assignment IDs

Format: `domain.discipline.module.assignment`

Example:
```
computing.fundamentals.algorithms_v1.a01_big_o
```

This ID is:
*   **Globally Unique**: No two assignments share an ID.
*   **Hierarchically Derived**: Reflects taxonomy position.
*   **Stable**: Never changes once published.
*   **Filesystem-Derived**: Folder names map deterministically to IDs.

**Invariant**: The filesystem IS the canonical namespace.
```
/domains/computing/fundamentals/algorithms_v1/a01_big_o
→ computing.fundamentals.algorithms_v1.a01_big_o
```
No hidden indirection. This prevents tooling bugs.

**Naming Convention** (frozen):
*   Lowercase only
*   Underscores allowed (no spaces, no hyphens)
*   Version suffix like `_v1`
*   Example: `a01_big_o`, `algorithms_v1`

---

## 1.2 Module Manifest (`module.yaml`)

Every module MUST declare:

```yaml
# A. Identity
id: computing.fundamentals.algorithms_v1
title: "Algorithms v1"
description: "Core algorithmic thinking."

# B. Assignment Order (Modules own sequencing)
assignments:
  - a01_big_o
  - a02_sorting
  - a03_recursion
```

The manifest is the **source of truth** for:
*   Module completion denominator.
*   Recommended learning order.

**Invariant**: Assignment names in `module.yaml` are **local names**, not full IDs.
The CLI resolves them as: `module_id + "." + local_name`.
This keeps modules self-contained and ensures renaming a module updates its namespace cleanly.

---

## 1.3 The Ledger Model (`ledger.yaml`)

The Ledger tracks learner state.

```yaml
completed:
  computing.fundamentals.algorithms_v1.a01_big_o:
    verified_at: "2026-02-06T10:30:00"
    score: 0.9

in_progress:
  - computing.systems.networking_v1.a03
```

*   **Key**: Canonical Assignment ID.
*   **Value**: Metadata object (supports future fields like `notes`, `verifier`, `source`).

**`in_progress`** (optional):
*   Non-authoritative UI state (convenience cache).
*   **Never** used in progress math.
*   **Never** relied upon for correctness.
*   May be stale, duplicated, or absent without breaking the system.

---

## 1.4 The Three Layers of Learning (Axiom)

We distinguish three stacked layers of capability. The system must identify which layer is being extended.

### Layer 1: Domain Knowledge (Concepts)
*   **Definition**: "I understand the concept of Division."
*   **Storage**: `competencies` (e.g., `math.arithmetic.division`).
*   **Nature**: Abstract, Declarative.

### Layer 2: Computational Formalization (Algorithms)
*   **Definition**: "I can make Division explicit as a step-by-step procedure."
*   **Storage**: `competencies` (e.g., `computing.fundamentals.algorithmic_formalization`).
*   **Nature**: Procedural, Logic-based. *The bridge between Math and Code.*

### Layer 3: Environment Fluency (Expression)
*   **Definition**: "I can encode that procedure in Python syntax."
*   **Storage**: `environment_fluency` (e.g., `python: practiced`).
*   **Nature**: Syntax, Tooling, Idiom.

> **Gap Analysis Rule**:
> *   **Layer 1 Gap**: Teach the Concept (Math).
> *   **Layer 2 Gap**: Teach the Algorithm (Step Decomposition). *Crucial for "Math in Python" tasks.*
> *   **Layer 3 Gap**: Teach the Syntax (Translation).

---

## 1.5 The Language Litmus Test (Instrument vs Specimen)

Is the language the **Tool** or the **Topic**?

### A. Language as Instrument (99% of cases)
*   **Goal**: Use Python to learn Iteration.
*   **Module**: `computing.fundamentals.iteration` (Concept).
*   **Assignment**: "Write a loop in Python."
*   **Rule**: **NEVER** put the language name in the Module ID.

### B.- **Language as Instrument vs Specimen**:
    -   Modules must NEVER be named after a tool (e.g. `python_basics`) unless the *subject of study* is the tool itself (e.g. `language_implementations.python`).
    -   Modules are *Realized* in an environment (instrument), but *Defined* by a concept.

    > **Litmus Test**: If we switched languages tomorrow, would this module still make sense?
> *   **Yes** → It is a Concept (Instrument).
> *   **No** → It is Implementation Detail (Tool).


### 4. The Three Tiers of Competence
We distinguish between what a learner *claims*, what they have *practiced*, and what they have *verified*.

1.  **Tier 1: Self-Reported** (Claimed)
    -   Unverified user input. Used to skip "introductory" material, but not trusted for advanced prerequisites.
2.  **Tier 2: Practiced** (Ledger)
    -   Evidence of completed assignments. Shows exposure and effort.
3.  **Tier 3: Verified** (Exam)
    -   Proof of understanding via "Test Out" challenges or Capstone projects.

**The Passive Resolution (Philosophy)**
The OS is a strictly passive tracker and agent runner. It is not "smart" and it does not make pedagogical decisions. If a user relies on a Tier 1 claim to skip to advanced modules, the OS simply updates its internal graph. If the user then struggles to complete the advanced assignments, the OS does absolutely nothing. It does not wake up to suggest an exam, nor does it proactively "fail" the user. 
It is a dashboard. It is up to the *user* to recognize they are stuck, inspect their own knowledge gaps, and manually trigger `scholar generate exam` or `scholar generate campaign` to patch their own Tier 1 claims into Tier 3 verifications. The OS provides the tools, but the user is the only one driving.

---

## 2. The Taxonomy: Computing (The 5 Disciplines)

We define **Computing** as the Domain, supported by 5 Pillars (Disciplines). These represent "Modes of Thinking".

| Discipline | Focus | Examples |
| :--- | :--- | :--- |
| **1. Fundamentals** | Laws & Primitives | Algorithms, Data Structures, Math, Computation Models |
| **2. Systems** | The Substrate | OS, Networking, Distributed Systems, Low-level Perf |
| **3. Software Engineering** | Construction Process | Architecture, Testing, Tooling, Design Patterns |
| **4. AI** | Adaptive Intelligence | Machine Learning, Statistics, Optimization |
| **5. Applied Computing** | Domain Expression | UX, Graphics, Databases, Gameplay, Data Visualization |

**Cross-Cutting Substrates** (e.g., programming languages):
*   Languages are NOT a discipline.
*   They are tools that manifest in every discipline.
*   Module categorization is by **cognitive objective**, not by tool.
*   Example: `python_algorithms_v1` → fundamentals, `python_testing_v1` → software_engineering.

**Rule of Thumb**:
*   *Discipline*: Answers "How does computation work?" (e.g., Systems).
*   *Practice*: Answers "What problem are we solving?" (e.g., Data Science). Practices emerge in Projects, not Domains.
*   *Tools*: Answers "What tool am I using?/What Environment am I in?" (e.g., Pen and Paper and Calculator, Python). Tools 

---

## 3. The Module Philosophy

*   **Bounded**: A module is a unit of **Closure**. It must be finishable.
*   **Sized**: 5-20 Assignments.
*   **Versioned**: Modules do NOT grow infinitely. When scope expands, we fork (e.g., `algorithms_v1`, `algorithms_v2`).
*   **Impact**: This ensures stable progress denominators. "80% complete" remains true forever.

---

## 4. Workflows

### The Definition Flow
1.  **Define Assignment**: Create atomic assignments at:
    ```
    /domains/[domain]/[discipline]/[module]/[assignment]/
      mission.md
      reflection.md
    ```
2.  **Define Project**: Create `project.yaml` in `/projects/[project_name]/`.
3.  **Define Campaign**: Create `campaign.yaml` in `/projects/[project_name]/campaigns/[campaign_name]/`, linking to Domain Assignment IDs.

### The Learning Flow (CLI)
1.  `scholar start [project]` -> Loads Campaign.
2.  `scholar status` -> Checks Ledger for Assignment IDs.
3.  `scholar submit` -> Verifies Atomic Assignment.

---

## 5. Next Steps (Immediate)
1.  **Refactor Directory Structure**: Verify `/domains/computing` reflects the 5 Disciplines.
2.  **Schema Definition**: Formalize `module.yaml` and `campaign.yaml`.
3.  **Scholar CLI**: Implement the "Resolver" logic.

---

## 6. The Progress Computation Model

All progress reduces to **set intersection**:

```
progress = |Relevant ∩ Completed| / |Relevant|
```

Where:
*   `Relevant` = assignments defined by a module/campaign/project/domain.
*   `Completed` = assignments in the ledger.

This applies uniformly to:
*   Module progress
*   Discipline progress
*   Domain progress
*   Campaign progress
*   Project progress
*   Total progress

**The CLI is a resolver performing set algebra over curriculum graphs.**

**Invariant (v1)**: All assignments have **equal weight** (1 unit each).
Weighted assignments may be introduced in future versions, but v1 keeps the math simple.

---

## 7. The Sparse Ledger Philosophy

The ledger is **sparse**, not dense.

*   **Sparse**: Only completed assignments are stored.
*   **Silence means incomplete**: If an assignment is not in the ledger, it is not done.

This ensures:
*   No migration when new assignments are added.
*   Ledger scales indefinitely.
*   No coupled state between curriculum and progress.

> Think of the ledger as a **set**, not a database.
> `Completed ⊆ AllAssignments`

---

## 8. Campaign Semantics

Campaigns are **ordered sequences** of assignment references.

```yaml
id: school.cli_bootstrap
assignments:
  - computing.fundamentals.cli_v1.a01   # First
  - computing.fundamentals.cli_v1.a02   # Second
  - computing.systems.io_v1.a01         # Third
```

*   The CLI respects this order for recommendations.
*   Future: may support DAG-based unlocking.

**Invariant**: Campaigns may referencde the same assignment **only once**.
Duplicates create ambiguous progress reporting.

---

## 9. Validation Rules

**Strict validation** is enforced:
*   If a campaign references an assignment that does not exist in `/domains`, the CLI **errors**.
*   This keeps the system honest and catches broken references early.

---

## 10. Governing Principles (Locked)

| Principle | Meaning |
| :--- | :--- |
| Knowledge expands by branching, not swelling | Add new modules; don't inflate old ones. |
| Modules are bounded milestones | 5-20 assignments, versioned. |
| Progress is stable under growth | Denominators never change retroactively. |
| Assignments are atomic units of truth | Everything connects through assignment IDs. |
| Mutable learner state is isolated | Only the ledger is personal/mutable. |
| Aggregates are computed, never stored | Progress is derived, not persisted. |
| Curriculum and execution are orthogonal | Domains ≠ Projects. They never couple. |

## 11. The AI Authoring Layer (Orchestrator vs Engine)

A critical distinction exists between the deterministic mathematical OS and the non-deterministic LLM generators.

### A. The Core Engine (The "Dumb" CLI)
*   **Location:** `engine/cli/`
*   **Role:** The deterministic query tool.
*   **Behavior:** Reads from `/school-content` and `/learners`. Computes progress using set algebra.
*   **Invariant:** The Core Engine **never** calls an LLM. It does not write content. It only reports on what already exists on the filesystem.

### B. The Agent Orchestrator (The "Smart" Runner)
*   **Location:** `engine/agents/runner.py`
*   **Role:** The AI manager that ties the Dumb Engine and the Smart Agents together.
*   **Behavior:** Authors new curriculum by communicating with LLMs (Track, Campaign, Module, Assignment agents) and saves the output to the filesystem.
*   **Dual-Mode Execution:**
    *   **Production:** `scholar generate track` → writes directly to canonical `/school-content`.
    *   **Benchmarking:** `runner.py --benchmark --case case_b.yaml` → creates an isolated Sandbox in `/runs/`, copies a faked `student_state.yaml`, and executes the generation cycle without contaminating the real school.

---

## 12. Defense in Depth (The Auxiliary Modules)

Because the Orchestrator relies on probabilistic LLMs, it uses strict auxiliary modules to enforce the Laws of Physics of the OS.

### A. Schemas (`engine/schemas/`)
*   **Purpose:** The Data Rulebook.
*   **Mechanism:** Uses `pydantic` to enforce strict mathematical shapes (types, lists, required keys) on all YAML config files (e.g., `RunConfig`, `LearnerState`).
*   **Failure Prevented:** Bad data types (e.g., LLM writing `level: three`) crashing the Python OS math logic.

### B. Validators (`engine/benchmarking/validators/`)
*   **Purpose:** The Markdown Graders.
*   **Mechanism:** Programmatically parses newly generated LLM text to assure it matches the expected formatting (e.g., enforcing the presence of a `# Mission` header).
*   **Failure Prevented:** Bad markdown rendering breaking the student's terminal UI. Enables the Orchestrator to reject bad output and trigger a retry loop with the LLM.

### C. The Resolver (`engine/resolver/`)
*   **Purpose:** The Curriculum Indexer & Linker.
*   **Mechanism:** Scans the entirety of `/school-content` to build a graph dictionary. Validates that every `requires` dependency points to a real, existing module.
*   **Failure Prevented:** The LLM hallucinating a dependency module that traps a student in an unfinishable curriculum tree.

---

## 13. Exams vs Modules (Tier 2 vs Tier 3 Evidence)

While mechanically similar (both have a prompt, constraints, and an expected output), the rules of engagement and the resulting metadata differ radically.

### A. Modules (Practice)
*   **Location:** `/school-content/domains/`
*   **Experience:** Incremental scaffolding. Hints allowed. Multiple submissions allowed.
*   **Metadata:** Generates **Level 2 (Practiced)** evidence for specific assignment IDs.

### B. Exams (Verification)
*   **Location:** `/school-content/exams/` (Kept entirely separate to avoid muddying the module progression math).
*   **Experience:** Strict "Test-Out" Philosophy. Zero hints. Binary pass/fail. Cooldown periods on failure.
*   **Metadata:** Generates **Level 3 (Verified)** evidence for an *entire conceptual cluster*, allowing the resolver to automatically skip all Level 2 assignments for that topic.
