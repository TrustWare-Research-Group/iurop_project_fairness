# simple_ses_count.py
import json
import os

# Count from the files
consistent_file = "mistralai_mixtral-8x22b-instruct-v0.1_results/cross_consistency_SES_ambig_consistent.jsonl"
mixed_file = "mistralai_mixtral-8x22b-instruct-v0.1_results/cross_consistency_SES_ambig_mixed.jsonl"

total = 0
fully_consistent = 0
question_b_biased = 0
both_flags = 0

for filepath in [consistent_file, mixed_file]:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    total += 1
                    data = json.loads(line)
                    summary = data.get('summary', {})
                    flags = summary.get('flag_counts', {})
                    
                    if summary.get('both_consistent', False):
                        fully_consistent += 1
                    if flags.get('flag_4', False):
                        question_b_biased += 1
                    if summary.get('both_consistent', False) and flags.get('flag_4', False):
                        both_flags += 1

print(f"Total pairs: {total}")
print(f"Fully consistent: {fully_consistent} ({fully_consistent/total*100:.1f}%)")
print(f"Question B biased: {question_b_biased} ({question_b_biased/total*100:.1f}%)")
print(f"Overlap (both flags): {both_flags} ({both_flags/total*100:.1f}%)")
print(f"\nUnique pairs with at least one flag: {fully_consistent + question_b_biased - both_flags}")
print(f"Expected if your parser double-counted: {fully_consistent + question_b_biased} > {total}")