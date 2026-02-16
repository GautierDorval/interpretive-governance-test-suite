## Variance protocol

Variance is a first-class signal. It must be measured and reported **per test_id**.

Averaging variance is discouraged; it hides failure modes.

## What variance is

Variance is divergence in:
- raw responses,
- inferred frames and boundaries,
- per-dimension scores,
across models, versions, runs, or contexts.

## Why variance matters

- High variance can indicate missing canonical anchors, unstable interpretation, or prompt sensitivity.
- Low variance can indicate stable grounding or consistent abstention.
- Low variance can also indicate **stable failure** (the same wrong frame repeated consistently).  
  Variance must be interpreted alongside fidelity, anti-inference, attribution, and authority dimensions.

## Variance taxonomy (recommended)

Report the dominant variance type(s):

- **Sampling variance**  
  Small differences in phrasing with materially identical claims and boundaries.

- **Structural variance**  
  Different frames, different boundary claims, or materially different inferred relationships.

- **Regime boundary variance**  
  Divergence caused by inconsistent interpretation of “should I answer at all” constraints (silence legitimacy).

## Minimum variance reporting

For each test_id, report:

- models compared (name + version)
- run identifiers
- raw responses (verbatim)
- per-dimension scores
- divergence summary (what changes and why it matters)
- risk implication (info / major / critical)

A reference format is provided:
- `datasets/variance-report-template.json`
- `schemas/variance-report.schema.json`

## Divergence significance (non-normative guidance)

Variance is considered **material** when it changes any of:

- identity attribution (who/what is being described),
- authority claims (mandate, certification, recommendation),
- scope boundaries (what is included/excluded),
- refusal vs answer decision.

When variance is material on **major** or **critical** risk-level tests, escalation is recommended (see `protocols/escalation-protocol.md`).
