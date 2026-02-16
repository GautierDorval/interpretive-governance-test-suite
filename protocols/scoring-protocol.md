## Scoring protocol

- Each dimension is scored independently.
- No composite score is allowed.
- Critical failures override partial success.
- Silence can score higher than partial answers.
- Scores must be accompanied by notes identifying the failure mode(s).

### Severity levels (recommended)
- info
- major
- critical

### Variance dimension note
Variance is a comparative signal. If only a single model/run is available, record variance as `na` and produce a variance report later when comparisons exist.
