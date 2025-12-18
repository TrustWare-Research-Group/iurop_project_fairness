# Oracle Analysis esults

## Configuration
- **Model**: deepseek-reasoner
- **Base URL**: https://api.deepseek.com
- **Subset**: Sexual_orientation
- **Context Condition**: disambig
- **Analysis Timestamp**: 2025-12-17 20:57:48

## Summary Statistics
- **Total Pairs Analyzed**: 216
- **Fully Consistent Pairs**: 55 (25.5%)
- **Inconsistent Reasoning Pairs**: 137 (63.4%)
- **Biased Interpretation Pairs**: 5 (2.3%)
- **Total Flagged Pairs**: 142 (65.7%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 113 | 52.3% |
| Reasoning A doesn't match Input B/Output B | 87 | 40.3% |
| Did not guess Question A correctly (expected x) | 2 | 0.9% |
| Did not guess Question B correctly (expected y) | 4 | 1.9% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
