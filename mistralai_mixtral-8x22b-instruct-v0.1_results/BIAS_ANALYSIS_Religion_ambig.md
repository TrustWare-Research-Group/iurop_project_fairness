# Oracle Analysis Results

## Configuration
- **Model**: mistralai/mixtral-8x22b-instruct-v0.1
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: Religion
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-03 02:15:25

## Summary Statistics
- **Total Pairs Analyzed**: 300
- **Fully Consistent Pairs**: 0 (0.0%)
- **Inconsistent Reasoning Pairs**: 0 (0.0%)
- **Biased Interpretation Pairs**: 253 (84.3%)
- **Total Flagged Pairs**: 253 (84.3%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 0 | 0.0% |
| Reasoning A doesn't match Input B/Output B | 0 | 0.0% |
| Guessed Question doesn't resemble Question A | 233 | 77.7% |
| Guessed Question doesn't resemble Question B | 230 | 76.7% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
