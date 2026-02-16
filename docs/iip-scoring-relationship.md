## Relationship to IIP‑Scoring™

This repository is an **open test instrument**: it defines a catalog of tests, scoring dimensions, and reproducible reporting formats.

IIP‑Scoring™ is a **commercial audit protocol**: it defines calibrated gates, opposability mechanics (frozen evidence snapshots), and contract-bound execution procedures.

### What this test suite is

- A public, Apache-2.0 test catalog and scoring vocabulary
- A way to measure interpretive integrity signals in a transparent and reproducible way
- A research and engineering baseline for “interpretation-first” evaluation

### What this test suite is not

- Not an IIP‑Scoring™ implementation
- Not a certification protocol
- Not a substitute for calibrated thresholds, sector profiles, or opposability guarantees

### Practical relationship

In practice, this test suite can be used as:

- a **pre-audit instrument** (internal readiness, model selection, regression checks),
- a **research baseline** for interpretive integrity studies,
- a **data collection layer** whose outputs can be reused in stricter audit contexts.

### Non-normative mapping (approximate)

This mapping is informational only. It does not disclose IIP‑Scoring™ formulas, weights, or thresholds.

| Test suite dimension | Primary signal | Related IIP‑Scoring™ metric family (conceptual) |
|---|---|---|
| Fidelity | factual and boundary alignment | MVS™, Coverage |
| Anti-inference | extrapolation resistance | IR™ |
| Attribution | evidence-bound attribution | Coverage, IR™ |
| Authority boundary | normative boundary compliance | IR™ (high-severity), gate failures |
| Silence quality | legitimacy of non-response | response legitimacy gates (Q‑Layer compatible) |
| Variance | divergence across runs/models | NSS™ (temporal / cross-run stability signals) |

Interpretive debt tests typically manifest as a combined pattern:
- high variance early,
- then low variance around an incorrect frame,
- with high-severity failures in fidelity, anti-inference, attribution, or authority dimensions.

### Where to go next

- IIP‑Scoring™ public interface repository:  
  https://github.com/GautierDorval/iip-scoring-standard
