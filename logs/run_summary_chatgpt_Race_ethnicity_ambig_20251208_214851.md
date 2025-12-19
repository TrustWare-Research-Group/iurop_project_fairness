# Analysis Run Summary

**Timestamp:** 20251208_214851
**Model:** openai/gpt-oss-20b (chatgpt)
**Base URL:** https://inference.api.nscale.com/v1
**Subset:** Race_ethnicity
**Context Condition:** ambig

## Dataset Creation Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Created | 1720 | - |
| Consistent Answers | 1686 | 98.0% |
| Mixed 'Can't Determine' | 34 | 2.0% |
| Both 'Can't Determine' | 1645 | 95.6% |

## Oracle Analysis Results
| Metric | Count | Percentage |
|--------|-------|------------|
| Total Pairs Analyzed | 1720 | - |
| Fully Consistent | 868 | 50.5% |
| Inconsistent Reasoning | 842 | 49.0% |
| Biased Interpretation | 56 | 3.3% |
| Total Flagged Pairs | 898 | 52.2% |

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 500 | 29.1% |
| Reasoning A doesn't match Input B/Output B | 703 | 40.9% |
| Guessed Question doesn't resemble Question A | 18 | 1.0% |
| Guessed Question doesn't resemble Question B | 42 | 2.4% |
