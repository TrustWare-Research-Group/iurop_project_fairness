# Oracle Analysis Results

## Configuration
- **Model**: deepseek-reasoner
- **Base URL**: https://api.deepseek.com
- **Subset**: Religion
- **Context Condition**: ambig
- **Analysis Timestamp**: 2025-12-02 20:40:41

## Summary Statistics
- **Total Pairs Analyzed**: 300
- **Fully Consistent Pairs**: 21 (7.0%)
- **Inconsistent Reasoning Pairs**: 236 (78.7%)
- **Biased Interpretation Pairs**: 175 (58.3%)
- **Total Flagged Pairs**: 206 (68.7%)

## Flag Breakdown
| Flag Type | Count | Percentage |
|-----------|-------|------------|
| Reasoning B doesn't match Input A/Output A | 161 | 53.7% |
| Reasoning A doesn't match Input B/Output B | 192 | 64.0% |
| Guessed Question doesn't resemble Question A | 103 | 34.3% |
| Guessed Question doesn't resemble Question B | 115 | 38.3% |

## Files Generated
- Cross-consistency results: `cross_consistency_*.jsonl`
- Flagged pairs: `flagged_pairs_*.md`
- This summary: `BIAS_ANALYSIS.md`
