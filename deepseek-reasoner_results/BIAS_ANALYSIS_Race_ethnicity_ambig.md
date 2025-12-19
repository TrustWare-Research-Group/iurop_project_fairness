# Oracle Analysis Results

## Configuration
- **Model**: deepseek-reasoner
- **Base URL**: https://api.deepseek.com
- **Subset**: Race_ethnicity
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-06 15:39:02

## Summary Statistics
- **Total Pairs Analyzed**: 1720
- **Fully Consistent Pairs**: 278 (16.2%)
- **Inconsistent Reasoning Pairs**: 912 (53.0%)
- **Biased Interpretation Pairs**: 1720 (100.0%)
- **Total Flagged Pairs**: 2632 (153.0%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 542 | 31.5% |
| Reasoning A doesn't match Input B/Output B | 694 | 40.3% |
| Did not guess Question A correctly (expected 1) | 1720 | 100.0% |
| Did not guess Question B correctly (expected 2) | 1720 | 100.0% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
