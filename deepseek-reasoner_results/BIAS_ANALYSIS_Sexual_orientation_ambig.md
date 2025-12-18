# Oracle Analysis esults

## Configuration
- **Model**: deepseek-reasoner
- **Base URL**: https://api.deepseek.com
- **Subset**: Sexual_orientation
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-17 18:06:39

## Summary Statistics
- **Total Pairs Analyzed**: 216
- **Fully Consistent Pairs**: 84 (38.9%)
- **Inconsistent Reasoning Pairs**: 127 (58.8%)
- **Biased Interpretation Pairs**: 15 (6.9%)
- **Total Flagged Pairs**: 142 (65.7%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 81 | 37.5% |
| Reasoning A doesn't match Input B/Output B | 93 | 43.1% |
| Did not guess Question A correctly (expected x) | 6 | 2.8% |
| Did not guess Question B correctly (expected y) | 11 | 5.1% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
