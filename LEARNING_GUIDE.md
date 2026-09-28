# Experiment Lens — learning guide

## What it does

Audit and interpret an A/B experiment. The intended user is product analysts. Browser controls → validated Flask API → project analysis/workflow → results and export.

## Run and demonstrate

Follow the README installation block, then: Inspect the synthetic experiment, then change expected treatment allocation to trigger an SRM warning. Compare the effect interval with zero and inspect the planning sample size for a chosen minimum effect.

## Important files

- `app.py` — local HTTP interface and request/error handling.
- `core.py` — project-specific logic.
- `tests/` — regression and correctness checks.
- `reports/` — recorded outputs and verification evidence.

## Three engineering decisions

1. Validate unique randomized user IDs and binary outcomes before computing effects.
2. Report absolute/relative lift, rate intervals, a fixed-horizon test and sample-ratio mismatch separately.
3. Expose allocation and planning assumptions; keep statistical evidence distinct from a shipping decision.

## Five interview questions

1. **What problem does this project solve, and what is its unit of work?** Explain audit and interpret an a/b experiment, identify product analysts as the audience, and trace one concrete example through the files above. Use the demonstration output rather than hypothetical impact.
2. **Why did you choose the first design decision?** Validate unique randomized user IDs and binary outcomes before computing effects. Show the corresponding implementation and a test that would fail if that property were removed.
3. **How do you protect correctness when inputs or execution change?** Report absolute/relative lift, rate intervals, a fixed-horizon test and sample-ratio mismatch separately. Explain the relevant invalid-input or edge-case test and distinguish a checked property from an untested assumption.
4. **How do you make results inspectable and reproducible?** Expose allocation and planning assumptions; keep statistical evidence distinct from a shipping decision. Point to actual outputs and recorded commands. Explain why a successful example is weaker evidence than a tested boundary or independently reconciled total.
5. **What would you improve before real deployment or real-data use?** Synthetic fixed-window experiment. Normal approximations can fail for sparse events. No sequential peeking correction, multiple testing adjustment, interference analysis or guardrail metric. Sample-size calculation is an equal-group planning approximation. Choose one limitation, describe the missing evidence, and propose a measurable acceptance check rather than promising production readiness.

## Independent exercise

Add Fisher's exact test for sparse outcomes and compare it with the normal approximation.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented and validated audit and interpret an a/b experiment using scipy · Flask, with srm checks and documented correctness checks and limitations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
