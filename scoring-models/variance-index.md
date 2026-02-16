## Variance index

**Measures** divergence across models or runs.

Variance is treated as a first-class signal. It can indicate:
- unstable interpretation,
- missing canonical anchors,
- sensitivity to prompt/context,
- regime boundary ambiguity.

Low variance can indicate:
- interpretive stability,
- robust canonical grounding,
- consistent abstention policy.

### Rubric (recommended)

Variance should be reported qualitatively per test_id (preferred).

If a compact label is required, use:

| Level | Meaning | Typical pattern |
|---|---|---|
| low / 0 | stable reconstruction | responses and dimension scores are materially consistent |
| medium / 1 | bounded divergence | divergence exists but stays within explicit uncertainty boundaries |
| high / 2 | unstable or conflicting frames | different models/runs converge on different “frames” or boundary claims |

### Reporting guidance (non-numeric preferred)

Rather than collapsing into a single scalar, report:
- divergence summary (what changes),
- which dimension(s) diverge (fidelity, attribution, authority, silence),
- risk implication (info/major/critical),
- whether divergence is sampling, structural, or regime-boundary driven.

See: `protocols/variance-protocol.md` and `schemas/variance-report.schema.json`.
