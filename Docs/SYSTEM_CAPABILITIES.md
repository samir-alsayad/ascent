# System Capabilities — Complete Feature Map

> Everything the system does, organized by layer and audience.

---

## 1. Core Engine (Layer 1 — Deterministic, AI-Free)

The truth system. Works with paper and a calculator. No models required.

### Concept Graph
- Universal knowledge ontology with explicit dependencies (`requires` / `produces`).
- Domain-neutral: computing, mathematics, physics, etc. coexist.
- Stable, versioned, learner-agnostic.

### Learner State Ledger
- **Tier 1 — Claimed**: Unverified self-report. Used to skip introductions, not trusted for prerequisites.
- **Tier 2 — Practiced**: Assignment completed. Evidence of effort and exposure.
- **Tier 3 — Verified**: Exam-proven mastery. Binary pass/fail, no hints, cooldown on failure.

### Gap Resolver
- `Required Concepts − Verified Concepts = Missing Transformation (Δ)`
- Computes the **minimal** set of learning needed for any stated objective.
- Pure set algebra — no heuristics, no intelligence.

### Progress Computation
- Uniform formula: `progress = |Relevant ∩ Completed| / |Relevant|`
- Works at every scale: assignment, module, domain, objective.
- Denominators are stable (modules are versioned and bounded).

### Objective Declarations
- "I want to do X" → becomes the system's driver.
- The system is **reactive**: no forward motion without a declared intent.
- Objectives may reference real-world projects, repos, or tools.

---

## 2. AI Synthesis Layer (Layer 2 — Replaceable Generator)

Uses LLMs to accelerate authoring. Everything it produces can be written by a human instead.

### Strategy Planner (Track Agent)
- Given goal + learner state → generates a minimal learning path.
- Respects domain closure, gap minimality, bridge module rules.
- Produces ordered module sequences, not curricula.

### Assignment Generator
- Creates `mission.md` + `reflection.md` + `verification.*` from module contracts.
- Assignments are proof obligations, not lessons.
- Each must be self-contained given prior assignments in the sequence.

### Exam Generator
- Creates Tier-3 verification challenges to "test out" of topics.
- Zero hints. Binary pass/fail. Cooldown periods on failure.
- Proves entire conceptual clusters, allowing the resolver to skip all T2 assignments for that topic.

### Campaign Recompiler
- When learner state changes (new evidence, new objective), recomputes the strategy.
- Old strategy is abandoned, new one derived from current delta.
- Adaptive replanning without manual intervention.

### Module Author
- Defines new module contracts (`requires`, `produces`, assignment specs) when the knowledge graph has gaps.
- Ensures modules pass the legitimacy test (new abstraction, library-independent, non-redundant, necessary).

---

## 3. Gamification & Engagement Layer

### XP System
- Points per assignment completion.
- Weighted by tier: T2 practice < T3 verified mastery.
- Scaled by module difficulty (assignment count, dependency depth).

### Streaks & Consistency
- Daily/weekly engagement tracking.
- Rewards sustained practice, not cramming.

### Mastery Badges
- Earned when an entire module or domain reaches T3 (verified).
- Visual proof of deep competence, not just exposure.

### Skill Tree Visualization
- The concept graph rendered as an explorable map.
- Lit nodes = verified. Dim nodes = practiced. Dark nodes = unknown.
- Interactive: click a node to see its assignments, dependencies, and evidence.

### Leaderboards (Optional)
- Compare progress across learners within a shared concept graph.
- Useful for classrooms, cohorts, or friendly competition.

### Challenge Mode
- "Test out" exams framed as high-stakes encounters.
- High risk, high XP, cooldown on failure.
- Proves mastery and unlocks downstream modules instantly.

---

## 4. Teacher / Institutional Features

### Class Dashboard
- Teacher sees all learners' state across a shared concept graph.
- Per-student drilldown into gaps, progress, and evidence.

### Gap Heatmap
- Aggregated view across a class: "80% of students are missing `iteration`."
- Surfaces systemic teaching gaps, not just individual ones.

### Custom Objectives
- Teacher declares "By Friday, students must prove X."
- System computes individualized paths per student based on their current state.

### Content Authoring
- Teacher writes assignments into `/domains` manually — same format as AI-generated.
- No AI needed. The structure is the interface.

### Exam Gating
- Teacher locks progression behind T3 verification for specific concepts.
- Ensures demonstrated mastery before advancing, not just time-on-task.

### Evidence Review
- Teacher can inspect and approve learner submissions for T3 upgrade.
- Human-in-the-loop verification when automated grading isn't sufficient.

---

## 5. Self-Directed Learner Features

### Knowledge Portfolio
- Complete record of what you've proven, when, and how.
- Exportable as transcript, portfolio, or credential proof.

### Gap Inspector
- "Show me what I don't know for goal X" → instant delta analysis.
- Renders the missing transformation, not a generic course recommendation.

### Multi-Objective Juggling
- Pursue multiple objectives simultaneously.
- Shared modules deduplicate: if two goals need `iteration`, it's learned once.

### Environment Fluency Tracking
- Separate from concept mastery.
- "I know iteration, but only practiced it in Python" — tracks per-environment evidence.

### Learning Journal
- Auto-generated from `reflection.md` answers across completed assignments.
- Your reasoning process over time, not just completion stamps.

### Transfer Detection
- "You proved `iteration` in Python — want to verify it in Rust too?"
- Identifies opportunities to broaden environmental fluency for known concepts.

---

## 6. Structural Safeguards

### Dependency Validation
- When a module is authored, the system verifies all `requires` actually exist in the concept graph.
- Prevents impossible curriculum (learner trapped by hallucinated prerequisites).

### Concept Drift Detection
- If a learner fails T3 on something they previously passed T2 on, the system flags degradation.
- Passive dashboard signal — the system never acts without being asked.

### Multi-Environment Proofs
- Same concept, different environments.
- "You can do recursion in Python. Can you do it on paper? In Haskell?"
- Builds genuine transfer, not tool-locked familiarity.

### Curriculum Versioning
- Modules are versioned (`v1`, `v2`).
- Old completions remain valid forever. New learners get latest version.
- Progress denominators never change retroactively.

### Collaborative Knowledge Building
- Multiple learners/teachers contribute to `/domains`.
- Concept graph grows organically — like a wiki, but structurally enforced.

### "Why Am I Stuck?" Diagnostics
- Resolver identifies which unmet dependency is blocking progress.
- Not a recommendation — just set algebra surfacing the specific blocker.

---

## 7. The Three Learning Layers (Axiom)

Every learning gap falls into exactly one of these:

| Layer | Question | Gap Means |
|---|---|---|
| **L1 — Domain Knowledge** | "Do I understand the concept?" | Teach the concept (math, physics, etc.) |
| **L2 — Computational Formalization** | "Can I make it a step-by-step procedure?" | Teach the algorithm — the *bridge* |
| **L3 — Environment Fluency** | "Can I express it in a specific tool?" | Teach the syntax (Python, pen-and-paper, etc.) |

The system must identify which layer is being extended before generating any content.

---

## 8. System Identity

### What It Is
- A **capability resolver** that tracks what you know, computes what you're missing, and generates exactly the learning you need.
- Teachers see gaps. Students prove mastery. Nothing is taught that doesn't need to be.
- AI accelerates authoring but is not the product.

### What It Is Not
- Not a course platform.
- Not an AI tutor or chatbot.
- Not a recommendation engine.
- Not an LMS.

### Core Metaphor
> `make(1)` for human skill acquisition.
> Concepts are source code. Learner state is compiled artifacts. Objectives are requested binaries. The planner is a dependency resolver.
