# iurop_project_fairness

Pipeline
- loads the model and dataset with ambigious questions
- Creates a pair (prompt A and prompt B):
-- Make sure that the multiple choice are structured the same for both for fact checking as in answer 1. is the same for prompt A and B, answer 2. is the same for prompt A and B and so also answer 3.
-- Change the prompt format so that the RLM responds with the answer as in X. Y (with X being the number and Y the answer corresponding to that number)
- Save the results in a json file for that model:
-- Save the id of the questions
-- The created id of the pair
-- The questions (not the prompt given)
-- The reasoning of the model
-- The answer



## Methodology

### Cross-Consistency Check
We analyze whether the reasoning appropriately accounts for and remains consistent with:
1. The input context and question
2. The output answer

We check consistency in both directions (A→B and B→A) to detect logical inconsistencies.

### Bias Detection via Question Guessing
We use an "oracle" model to reconstruct the original question based on:
- Context
- Model's reasoning
- Final answer

If the guessed question differs substantially from the original question, we flag it as potential bias. This indicates the model may be answering a different question than intended.

## Flag Categories

### 1. Inconsistent Reasoning
Pairs where the reasoning doesn't logically align with the input context/question or output answer.

### 2. Biased Interpretation  
Pairs where the model appears to be answering a different question than intended, suggesting biased interpretation of the context.

## Files Generated

For each dataset, two files are generated:
- `cross_consistency_*.jsonl`: Detailed results in JSONL format
- `flagged_pairs_*.md`: Markdown report of flagged pairs with analysis

## Interpretation

- **High inconsistent rates** may indicate reasoning flaws in the model
- **High bias rates** may indicate the model is making unwarranted assumptions or stereotypes
- **Combined flags** suggest serious issues with model understanding
"""