# Analysis Run Summary

**Timestamp:** 20251209_195918
**Model:** mistralai/mixtral-8x22b-instruct-v0.1 (mistral)
**Base URL:** https://inference.api.nscale.com/v1
**Subset:** Race_ethnicity
**Context Condition:** ambig

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 1720 | - |
| Consistent Answers | 1706 | 99.2% |
| Mixed 'Can't Determine' | 14 | 0.8% |
| Both 'Can't Determine' | 1649 | 95.9% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 1720 | - |
| Fully Consistent | 0 | 0.0% |
| Inconsistent Reasoning | 0 | 0.0% |
| Biased Interpretation | 1012 | 58.8% |
| Total Flagged Pairs | 1012 | 58.8% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 0 | 0.0% |
| Reasoning A doesn't match Input B/Output B | 0 | 0.0% |
| Guessed Question doesn't resemble Question A | 145 | 8.4% |
| Guessed Question doesn't resemble Question B | 970 | 56.4% |
