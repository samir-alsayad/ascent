# Benchmark Test Cases — Math with Python

## Test Case 1: Absolute Beginner

**Module contract:**
```yaml
id: mathematics.arithmetic.basic_operations_v1
requires: []
produces:
  - mathematics.arithmetic.basic_operations.construct_expression
```

**Assignment ID:** `a01_first_calculations`

**Prompt to agent:**
> You are generating assignment `a01_first_calculations` for module `mathematics.arithmetic.basic_operations_v1`.
>
> The learner has NO prior knowledge. This is their first assignment ever.
>
> Target competency: `mathematics.arithmetic.basic_operations.construct_expression`
>
> The learner must be able to complete this with zero prior experience in programming or mathematics beyond knowing what numbers are.

**What to check:**
- [ ] Does it start from absolute zero?
- [ ] Is the challenge a CREATE action (not "learn" or "understand")?
- [ ] Can someone with zero experience actually complete this?
- [ ] Is verification concrete and executable?
- [ ] Are reflection questions Reconstruction/Perturbation/Transfer?

---

## Test Case 2: Building on Prior Knowledge

**Module contract:**
```yaml
id: mathematics.arithmetic.order_of_operations_v1
requires:
  - mathematics.arithmetic.basic_operations.construct_expression
  - programming.python.variables.construct_assignment
produces:
  - mathematics.arithmetic.order_of_operations.predict_result
  - mathematics.arithmetic.order_of_operations.construct_parenthesized
```

**Assignment ID:** `a01_operator_precedence`

**Prompt to agent:**
> You are generating assignment `a01_operator_precedence` for module `mathematics.arithmetic.order_of_operations_v1`.
>
> The learner already knows:
> - How to write basic arithmetic expressions in Python (+, -, *, /)
> - How to assign values to variables
>
> Target competency: `mathematics.arithmetic.order_of_operations.predict_result`
>
> Do NOT re-teach arithmetic or variables. Build on them.

**What to check:**
- [ ] Does it assume (not re-teach) basic arithmetic and variables?
- [ ] Is the step up in complexity reasonable?
- [ ] Does it avoid jumping to advanced concepts?
- [ ] Is mission.md self-contained given the stated prerequisites?

---

## Test Case 3: Stress Test — Vague Goal

**Module contract:**
```yaml
id: mathematics.algebra.equations_v1
requires:
  - mathematics.arithmetic.basic_operations.construct_expression
  - mathematics.arithmetic.order_of_operations.predict_result
  - programming.python.variables.construct_assignment
produces:
  - mathematics.algebra.equations.construct_linear_solver
```

**Assignment ID:** `a01_solve_for_x`

**Prompt to agent:**
> You are generating assignment `a01_solve_for_x` for module `mathematics.algebra.equations_v1`.
>
> The learner knows: basic arithmetic, order of operations, Python variables.
> The learner does NOT know: algebra, sympy, or any math libraries.
>
> Target competency: `mathematics.algebra.equations.construct_linear_solver`
>
> The learner must solve a linear equation using only basic Python. No imports allowed.

**What to check:**
- [ ] Does it bridge cleanly from arithmetic to algebra?
- [ ] Does it avoid importing sympy or any libraries?
- [ ] Is the scope truly atomic (one equation type, not a general solver)?
- [ ] Would the mission.md be completable without Googling?
