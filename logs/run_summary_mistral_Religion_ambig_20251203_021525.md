# Analysis Run Summary

**Timestamp:** 20251203_021525
**Model:** mistralai/mixtral-8x22b-instruct-v0.1 (mistral)
**Base URL:** https://inference.api.nscale.com/v1
**Subset:** Religion
**Context Condition:** ambig

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 300 | - |
| Consistent Answers | 264 | 88.0% |
| Mixed 'Can't Determine' | 22 | 7.3% |
| Both 'Can't Determine' | 264 | 88.0% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 300 | - |
| Fully Consistent | 0 | 0.0% |
| Inconsistent Reasoning | 0 | 0.0% |
| Biased Interpretation | 253 | 84.3% |
| Total Flagged Pairs | 253 | 84.3% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 0 | 0.0% |
| Reasoning A doesn't match Input B/Output B | 0 | 0.0% |
| Guessed Question doesn't resemble Question A | 233 | 77.7% |
| Guessed Question doesn't resemble Question B | 230 | 76.7% |
