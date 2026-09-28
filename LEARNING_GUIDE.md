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

1. **Why check sample-ratio mismatch first?** An unexpected allocation imbalance can indicate an assignment or instrumentation problem. A statistically significant conversion result is not trustworthy if the experiment itself is compromised.

2. **What is the unit of randomization here?** One row per unique user. Duplicate user records violate the intended unit and are rejected before calculating the comparison.

3. **Why report an interval as well as a p-value?** The interval communicates the plausible effect magnitude under the model. A p-value alone does not show practical importance or the cost-benefit tradeoff.

4. **How do absolute and relative lift differ?** Absolute lift is the difference in conversion rates, in percentage points. Relative lift divides that difference by the control rate and can look large when the baseline is small.

5. **What assumptions limit the analysis?** The normal approximations need adequate counts, and the planning formula assumes a fixed two-arm comparison. Sparse outcomes, repeated peeking and multiple testing require additional methods.

## Independent exercise

Add Fisher's exact test for sparse outcomes and compare it with the normal approximation.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Built a 4,000-user synthetic A/B analysis workflow with sample-ratio checks, conversion intervals, lift estimates and power planning; verified nine analytical/API checks.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
