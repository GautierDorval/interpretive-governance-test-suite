# Changelog

## Unreleased

- Added a closed, immutable reference envelope for the exact Interpretive
  Governance standard snapshot used by this instrument.
- Added optional local Git verification of the pinned standard remote, commit,
  tree, release status, canonical manifest digest, and byte length.
- Added positive and negative schema self-tests for reference-envelope closure.
- Clarified that suite results are bounded evidence, not certification,
  endorsement, approval, or a general conformance verdict.
- Added CI workflow (`.github/workflows/ci-validate.yml`) with push + PR triggers.
- Added `.gitignore`.
- Added pinned `scripts/requirements.txt` (`jsonschema==4.23.0`).
- Extended `validate_repo.py` to validate JSON syntax for all JSON/JSON-LD files (schemas, terms).

---

## [1.1.1] — 2026-02-16 — Adoption hardening + reproducibility upgrades

### Added
- End-to-end filled example (question set → raw responses → scoring → variance report)
- JSON Schemas for dataset artifacts (`schemas/`)
- Minimal CI for JSON syntax + schema validation + repo integrity checks
- Machine-readable term registry (`terms/`) for test categories and scoring dimensions
- Documentation clarifying relationship to IIP-Scoring™ (`docs/iip-scoring-relationship.md`)

### Changed
- Canonical references now point to normative/doctrinal sources (manifest + doctrine repos), with websites treated as observational surfaces
- Scoring models upgraded with explicit rubrics to reduce evaluator variance
- Variance protocol expanded with reporting format and interpretation guidance

## [1.1.0] — Prior release
- See GitHub release notes for details.

## [1.0.0] — 2026-02-09 — Initial normative release

### Added
- Full interpretive governance test catalog
- Identity, doctrine, relationship, authority, offer, and silence tests
- Attribution integrity test catalog and scoring model
- Scoring models for fidelity, anti-inference, authority boundaries, and silence quality
- Evaluation protocols (test execution, scoring, escalation, variance)
- Dataset templates for question sets, response logs, and scoring outputs
- Governance principles, scope boundaries, and definitions
