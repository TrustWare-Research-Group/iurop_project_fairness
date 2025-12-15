# Oracle Analysis Results

## Configuration
- **Model**: mistralai/mixtral-8x22b-instruct-v0.1
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: Race_ethnicity
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-09 19:59:18

## Summary Statistics
- **Total Pairs Analyzed**: 1720
- **Fully Consistent Pairs**: 0 (0.0%)
- **Inconsistent Reasoning Pairs**: 0 (0.0%)
- **Biased Interpretation Pairs**: 1012 (58.8%)
- **Total Flagged Pairs**: 1012 (58.8%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 372 | 31.6% |
| Reasoning A doesn't match Input B/Output B | 233 | 13.5% |
| Did not guess Question A correctly (expected x) | 145 | 8.4% |
| Did not guess Question B correctly (expected y) | 970 | 56.4% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
