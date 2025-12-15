# Analysis Run Summary

**Timestamp:** 20251206_153902
**Model:** deepseek-reasoner (deepseek)
**Base URL:** https://api.deepseek.com
**Subset:** Race_ethnicity
**Context Condition:** ambig

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 1720 | - |
| Consistent Answers | 1664 | 96.7% |
| Mixed 'Can't Determine' | 56 | 3.3% |
| Both 'Can't Determine' | 1626 | 94.5% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 1720 | - |
| Fully Consistent | 278 | 16.2% |
| Inconsistent Reasoning | 912 | 53.0% |
| Biased Interpretation | 1720 | 100.0% |
| Total Flagged Pairs | 2632 | 153.0% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 542 | 31.5% |
| Reasoning A doesn't match Input B/Output B | 694 | 40.3% |
| Guessed Question doesn't resemble Question A | 1720 | 100.0% |
| Guessed Question doesn't resemble Question B | 1720 | 100.0% |
