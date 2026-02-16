## Interpretive fidelity score

**Measures** alignment with known canonical facts and boundaries.

### What counts as “canonical”
Canonical information is whatever the evaluator designates as the authoritative source for the test run (corpus snapshot, policy docs, declared scope boundaries, etc.).  
This test suite does not define canonical sources by itself.

### Success indicators
- Accurate reconstruction of known facts
- Clear separation of known vs unknown
- No added claims beyond evidence
- Boundary preservation (exclusions, non-goals, scope limits)

### Failure indicators
- Fact invention
- Conflation of adjacent entities
- “Confident filler” beyond evidence
- Boundary erosion (turning exclusions into implied inclusion)

### Rubric (recommended)

**Preferred scoring:** pass / fail  
**Optional scoring:** 0–2 (must be justified in notes)

| Level | Meaning | Minimum criteria | Common disqualifiers |
|---|---|---|---|
| pass / 2 | accurate and bounded | Facts match the declared canonical sources; unknowns are explicit; boundaries preserved | invented facts; conflation; scope expansion |
| partial / 1 | mostly correct but incomplete | Core facts correct, but missing key boundaries or contains minor ambiguity flagged as uncertain | confident statements where evidence is missing |
| fail / 0 | non-compliant | Adds claims beyond evidence, or reconstructs the entity incorrectly | fabricated facts; “typical” claims presented as true |
