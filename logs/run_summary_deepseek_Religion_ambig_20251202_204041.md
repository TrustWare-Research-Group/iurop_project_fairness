# Analysis Run Summary

**Timestamp:** 20251202_204041
**Model:** deepseek-reasoner (deepseek)
**Base URL:** https://api.deepseek.com
**Subset:** Religion
**Context Condition:** ambig

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 300 | - |
| Consistent Answers | 286 | 95.3% |
| Mixed 'Can't Determine' | 13 | 4.3% |
| Both 'Can't Determine' | 286 | 95.3% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 300 | - |
| Fully Consistent | 21 | 7.0% |
| Inconsistent Reasoning | 236 | 78.7% |
| Biased Interpretation | 175 | 58.3% |
| Total Flagged Pairs | 411 | 137.0% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 161 | 53.7% |
| Reasoning A doesn't match Input B/Output B | 192 | 64.0% |
| Guessed Question doesn't resemble Question A | 103 | 34.3% |
| Guessed Question doesn't resemble Question B | 115 | 38.3% |
