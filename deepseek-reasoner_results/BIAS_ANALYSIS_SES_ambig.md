# Oracle Analysis Results

## Configuration
- **Model**: deepseek-reasoner
- **Base URL**: https://api.deepseek.com
- **Subset**: SES
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-12 22:32:58

## Summary Statistics
- **Total Pairs Analyzed**: 1488
- **Fully Consistent Pairs**: 128 (8.6%)
- **Inconsistent Reasoning Pairs**: 974 (65.5%)
- **Biased Interpretation Pairs**: 20 (1.3%)
- **Total Flagged Pairs**: 994 (66.8%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 543 | 36.5% |
| Reasoning A doesn't match Input B/Output B | 770 | 51.7% |
| Did not guess Question A correctly (expected x) | 4 | 0.3% |
| Did not guess Question B correctly (expected y) | 16 | 1.1% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
