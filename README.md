# Ascent

**A system for goal-driven learning, capability tracking, and knowledge transfer — for humans, AI, or both.**

> Ascent doesn't teach you everything. It teaches you exactly what's missing.

---

## The Problem

Learning tools today — LMS platforms, online courses, AI tutors — all share the same flaw: they start from a syllabus and work forward. They teach *everything*, regardless of what you already know.

But learning isn't about coverage. It's about **closing gaps**.

If you already understand algebra and want to compute quadratic roots in Python, you don't need a math refresher or a programming basics course. You need exactly one thing: the ability to translate symbolic reasoning into executable procedure.

No existing system computes that delta for you.

## What Ascent Does

Ascent is a **capability resolver**. Given a goal and a learner's verified state, it computes the minimal transformation required — then delivers only the learning needed to close that gap.

```
declare_intent("Compute quadratic roots in Python")
→ compute_delta(goal, learner_state)
→ resolve_modules()          # 1 module, not 12
→ generate_assignments()     # Proof obligations, not lectures
→ verify()                   # Evidence, not completion stamps
→ update_state()             # Capability now exists
```

Learning is tracked through a **3-tier evidence model**: what you claim → what you've practiced → what you've proven. Only proven capability counts.

## Who Uses Ascent

The system separates **structure** from **authorship**. Any combination works:

|  | **Human Student** | **AI Student** |
|---|---|---|
| **Human Teacher** | Traditional structured learning | AI training on structured curriculum |
| **AI Teacher** | AI-generated, human-verified learning | Fully autonomous pipeline |

Same module contracts. Same assignment format. Same evidence model. The system is **actor-agnostic**.

## Unlocking AI for Knowledge Transfer

Most "AI in education" products wrap a chatbot around a content library. That's a UX improvement, not a paradigm shift.

Ascent provides **structure** that makes AI genuinely useful for learning:

- **A concept graph with declared dependencies** — giving AI something to reason against, rather than generating from nothing
- **Atomic assignments with clear scope** — so AI output is bounded and reviewable
- **A formal learner state model** — so AI can avoid re-teaching known material
- **Module contracts with specs** — so AI generates against constraints, not open-ended prompts

Without this structure, AI generates generic courses. With it, AI can function as a **content compiler** — generating targeted learning artifacts scoped to a specific learner's gaps.

This is **intelligence transfer infrastructure**, not content delivery.
Neither the graph nor the AI output is guaranteed to be correct. But the structure makes it auditable, improvable, and far more useful than unstructured generation.

## The Three Learning Layers

The system models knowledge gaps across three layers:

| Layer | Question | Example |
|-------|----------|---------|
| **Domain Knowledge** | "Do I understand the concept?" | Understanding quadratic equations |
| **Computational Formalization** | "Can I express it as a procedure?" | Turning the formula into step-by-step logic |
| **Environment Fluency** | "Can I implement it in a specific tool?" | Writing it in Python |

Through self reporting, exams, and tracked evidence, the system can assess which layers a learner has demonstrated competence in — and focus new content on the actual gap rather than re-covering known ground.

## Key Features

**Core Engine (works without AI)**
- Gap-minimal planning — fewest modules necessary, justified by concrete missing capabilities
- 3-tier evidence model — claimed / practiced / verified
- Domain closure — verified knowledge is never re-taught
- Versioned, bounded modules — 5-20 assignments each, stable progress denominators
- Set-algebraic progress — `|Relevant ∩ Completed| / |Relevant|` at every scale

**AI Synthesis Layer (optional, replaceable)**
- Strategy planner — generates minimal learning paths from goal + learner state
- Assignment generator — creates mission, reflection, and verification files from module contracts
- Exam generator — Tier-3 "test-out" challenges for verified mastery
- Adaptive replanning — recomputes strategy when learner state changes

**Engagement & Tracking**
- XP system, streaks, mastery badges
- Skill tree visualization — concept graph as an explorable map
- Knowledge portfolio — exportable proof of demonstrated capability
- Gap inspector — instant delta analysis for any stated goal

**For Teachers & Institutions**
- Class dashboard with per-student gap visibility
- Aggregated gap heatmaps across learner cohorts
- Custom objectives with individualized path computation
- Evidence review and manual verification

## Project Structure

```
ascent/
├── engine/              # Core engine + AI synthesis layer
│   ├── agents/          # Track, Campaign, Module, Assignment agents
│   ├── prompts/         # Versioned prompt templates
│   ├── benchmarking/    # LLM client, test harness
│   ├── cli/             # Command-line interface
│   ├── resolver/        # Gap computation
│   └── schemas/         # Pydantic data models
│
├── benchmarks/          # Test cases and prompt routing config
├── school-content/      # Knowledge graph (domains, modules, assignments)
├── learners/            # Learner state files
└── Docs/                # Architecture documentation
```

## Status

🚧 **Active Development** — Core engine operational. Prompt engineering in progress. CLI, gamification layer, and teacher dashboard are partly implemented.

## Tech Stack

- **Python 3.12** — Core engine and CLI
- **OpenRouter** — Model-agnostic LLM backend (Mistral, Qwen, etc.)
- **Pydantic** — Schema validation
- **YAML** — Knowledge graph and state storage

## License

TBD

---

*`make(1)` for human skill acquisition.*
