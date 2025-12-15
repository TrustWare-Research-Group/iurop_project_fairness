# Analysis Run Summary

**Timestamp:** 20251203_045856
**Model:** openai/gpt-oss-20b (chatgpt)
**Base URL:** https://inference.api.nscale.com/v1
**Subset:** Religion
**Context Condition:** ambig

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 300 | - |
| Consistent Answers | 283 | 94.3% |
| Mixed 'Can't Determine' | 9 | 3.0% |
| Both 'Can't Determine' | 283 | 94.3% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 300 | - |
| Fully Consistent | 92 | 30.7% |
| Inconsistent Reasoning | 208 | 69.3% |
| Biased Interpretation | 297 | 99.0% |
| Total Flagged Pairs | 505 | 168.3% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 105 | 35.0% |
| Reasoning A doesn't match Input B/Output B | 188 | 62.7% |
| Guessed Question doesn't resemble Question A | 260 | 86.7% |
| Guessed Question doesn't resemble Question B | 266 | 88.7% |
