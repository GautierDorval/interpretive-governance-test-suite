## End-to-end example (filled)

This folder demonstrates a complete evaluation cycle using **fictional** data.

### Files

- `corpus.example.md`  
  Canonical excerpt used as the authoritative reference for this example.

- `question-set.example.json`  
  A minimal question set spanning all test categories.

- `response-log.example.json`  
  Raw responses for two fictional models on the same questions.

- `scoring-output.example.json`  
  Per-dimension scoring outputs for each model response.

- `variance-report.example.json`  
  Variance reports showing how divergence is recorded per test_id.

### Validation

From the repo root:

```bash
python -m pip install jsonschema
python scripts/validate_repo.py
```
