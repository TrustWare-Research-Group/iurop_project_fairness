# Oracle Analysis Results

## Configuration
- **Model**: openai/gpt-oss-20b
- **Base URL**: https://inference.api.nscale.com/v1
- **Subset**: Race_ethnicity
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-08 21:48:51

## Summary Statistics
- **Total Pairs Analyzed**: 1720
- **Fully Consistent Pairs**: 868 (50.5%)
- **Inconsistent Reasoning Pairs**: 842 (49.0%)
- **Biased Interpretation Pairs**: 56 (3.3%)
- **Total Flagged Pairs**: 898 (52.2%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 500 | 29.1% |
| Reasoning A doesn't match Input B/Output B | 703 | 40.9% |
| Did not guess Question A correctly (expected x) | 18 | 1.0% |
| Did not guess Question B correctly (expected y) | 42 | 2.4% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
