# Oracle Analysis Results

## Configuration
- **Model**: openai/gpt-oss-20b
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: Religion
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-03 04:58:56

## Summary Statistics
- **Total Pairs Analyzed**: 300
- **Fully Consistent Pairs**: 92 (30.7%)
- **Inconsistent Reasoning Pairs**: 208 (69.3%)
- **Biased Interpretation Pairs**: 297 (99.0%)
- **Total Flagged Pairs**: 505 (168.3%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 105 | 35.0% |
| Reasoning A doesn't match Input B/Output B | 188 | 62.7% |
| Guessed Question doesn't resemble Question A | 260 | 86.7% |
| Guessed Question doesn't resemble Question B | 266 | 88.7% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
