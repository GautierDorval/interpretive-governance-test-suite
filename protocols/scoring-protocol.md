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

### Claim status note
A change of claim status (proposal, observation, capability or author's statement presented with a stronger status) is scored with the existing dimensions, not as a separate score. See [claim status preservation](../docs/claim-status-preservation.md).
