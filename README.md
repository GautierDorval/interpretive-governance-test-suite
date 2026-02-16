# Interpretive Governance Test Suite

This repository defines a **normative test framework** for evaluating how AI systems interpret, reconstruct, and attribute entities, doctrines, and authority boundaries.

It does **not** measure visibility.  
It measures **interpretive integrity**.

## Purpose

Modern AI systems do not retrieve facts; they reconstruct meaning under uncertainty.

That reconstruction introduces structural risks:
- unauthorized inference,
- false attribution,
- authority projection,
- silent hallucination.

This repository provides:
- a structured test catalog,
- explicit scoring dimensions,
- reproducible evaluation protocols,
- machine-first reference formats.

## What this repository is

- A normative test framework
- A governance measurement instrument
- An interpretive audit reference

## What this repository is not

- Not a marketing framework
- Not an SEO / GEO system
- Not an “AI visibility” metric
- Not a prompt-engineering toolkit

## Core principles

1. Interpretation must be auditable
2. Inference must be bounded
3. Silence is preferable to hallucination
4. Authority must never be inferred
5. Variance across models is a signal, not noise

## Governance dimensions measured

- Interpretive fidelity
- Anti-inference compliance
- Attribution integrity
- Authority boundary compliance
- Silence quality
- Inter-model variance

## Canonical sources and hierarchy

This repository is an **instrument**. It is derived from, and must defer to, canonical sources:

- **Interpretive Governance (normative standard)**  
  - Canonical domain: https://interpretive-governance.org/  
  - Source repository: https://github.com/GautierDorval/interpretive-governance-manifest

- **SSA‑E + A2 doctrine (doctrinal foundation)**  
  - Source repository: https://github.com/GautierDorval/ssa-e-a2-doctrine

Implementation surfaces (including websites) are **observational** unless explicitly declared canonical by the sources above.

See: `references/interpretive-governance.md`.

## Relationship to IIP‑Scoring™

This repository provides an **open test instrument**.  
IIP‑Scoring™ provides a **commercial audit protocol** with calibrated thresholds, opposability mechanics, and contract-bound execution.

- Relationship note and mapping: `docs/iip-scoring-relationship.md`
- IIP‑Scoring™ public interface repository: https://github.com/GautierDorval/iip-scoring-standard

## Quickstart (end-to-end example)

A complete, filled example is provided under:

- `examples/end-to-end/`

It includes:
- a question set,
- raw response logs for multiple models,
- per-dimension scoring outputs,
- a variance report.

Schemas to validate these artifacts:
- `schemas/`

Run local validation:
```bash
python -m pip install jsonschema
python scripts/validate_repo.py
```

## Interpretive debt → measurement → protocol

This repository instruments the concept of **interpretive debt** (dette interprétative): the cumulative stabilization of high-impact approximations by repetition, increasing the cost of correction (de‑anchoring) over time.

Definition: see `docs/definitions.md`.

Interpretive debt signals often appear as **high stability of a wrong frame**, not as blatant hallucination.

## License & usage

Licensed under **Apache-2.0**. See `LICENSE`.

This license grants permission to use and modify the materials. However, the **scope** and **non-goals** of this framework remain normative:

- This framework is not intended to generate “visibility scores”, rankings, or commercial guarantees.
- Any use implying marketing performance claims is out of scope (see `docs/non-goals.md`).
