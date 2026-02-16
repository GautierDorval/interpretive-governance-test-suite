# Changelog

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
