# Analysis Run Summary

**Timestamp:** 20251212_223258
**Model:** deepseek-reasoner (deepseek)
**Base URL:** https://api.deepseek.com
**Subset:** SES
**Context Condition:** ambig

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 1488 | - |
| Consistent Answers | 1448 | 97.3% |
| Mixed 'Can't Determine' | 40 | 2.7% |
| Both 'Can't Determine' | 1447 | 97.2% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 1488 | - |
| Fully Consistent | 128 | 8.6% |
| Inconsistent Reasoning | 974 | 65.5% |
| Biased Interpretation | 20 | 1.3% |
| Total Flagged Pairs | 994 | 66.8% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 543 | 36.5% |
| Reasoning A doesn't match Input B/Output B | 770 | 51.7% |
| Guessed Question doesn't resemble Question A | 4 | 0.3% |
| Guessed Question doesn't resemble Question B | 16 | 1.1% |
