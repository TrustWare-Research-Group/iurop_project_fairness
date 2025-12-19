# import json
# import re
# import os
# from pathlib import Path

# def parse_consistency_from_raw_output(raw_output):
#     """
#     Parse the raw output to determine if 'yes' or 'no' was actually said.
#     """
#     if not raw_output:
#         return "unknown"
    
#     # Look for "Answer: yes" or "Answer: no" patterns in the raw output
#     patterns = [
#         r'Answer:\s*(yes|no)\s*$',
#         r'Answer:\s*(yes|no)[\s\.]',
#         r'^Answer:\s*(yes|no)\s*\n',
#         r'"Answer":\s*"(yes|no)"',
#     ]
    
#     for pattern in patterns:
#         match = re.search(pattern, raw_output, re.IGNORECASE | re.MULTILINE)
#         if match:
#             answer = match.group(1).lower()
#             return answer
    
#     # If not found, search for "yes" or "no" near the beginning
#     lines = raw_output.strip().split('\n')
#     for line in lines[:3]:
#         line_lower = line.lower().strip()
#         if line_lower.startswith('yes'):
#             return 'yes'
#         elif line_lower.startswith('no'):
#             return 'no'
#         elif 'yes' in line_lower and 'no' not in line_lower:
#             return 'yes'
#         elif 'no' in line_lower and 'yes' not in line_lower:
#             return 'no'
    
#     return "unknown"

# def analyze_jsonl_file(file_path):
#     """
#     Analyze a JSONL file and extract cross-consistency information.
#     Returns statistics in the requested format.
#     """
#     total_pairs = 0
#     reasoning_b_no_match = 0  # Flag 1: A_to_B inconsistent
#     reasoning_a_no_match = 0  # Flag 2: B_to_A inconsistent
    
#     detailed_results = []
    
#     with open(file_path, 'r', encoding='utf-8') as f:
#         for line_num, line in enumerate(f, 1):
#             if not line.strip():
#                 continue
                
#             try:
#                 data = json.loads(line.strip())
#                 total_pairs += 1
                
#                 # Get both cross consistency checks
#                 checks = data.get('cross_consistency_checks', {})
#                 a_to_b_check = checks.get('A_to_B', {})
#                 b_to_a_check = checks.get('B_to_A', {})
                
#                 # Parse A_to_B check (Reasoning B doesn't match Input A/Output A)
#                 a_to_b_raw = a_to_b_check.get('raw_output', '')
#                 a_to_b_actual = parse_consistency_from_raw_output(a_to_b_raw)
                
#                 # Parse B_to_A check (Reasoning A doesn't match Input B/Output B)
#                 b_to_a_raw = b_to_a_check.get('raw_output', '')
#                 b_to_a_actual = parse_consistency_from_raw_output(b_to_a_raw)
                
#                 # Count "no" responses (inconsistent)
#                 if a_to_b_actual == 'no':
#                     reasoning_b_no_match += 1
                
#                 if b_to_a_actual == 'no':
#                     reasoning_a_no_match += 1
                
#                 detailed_results.append({
#                     'pair_index': data.get('data', {}).get('pair_index', 'N/A'),
#                     'a_to_b_actual': a_to_b_actual,
#                     'b_to_a_actual': b_to_a_actual,
#                     'a_to_b_raw_preview': a_to_b_raw[:100] if a_to_b_raw else '',
#                     'b_to_a_raw_preview': b_to_a_raw[:100] if b_to_a_raw else ''
#                 })
                
#             except json.JSONDecodeError as e:
#                 print(f"Error parsing line {line_num}: {e}")
#                 continue
#             except Exception as e:
#                 print(f"Error processing line {line_num}: {e}")
#                 continue
    
#     return {
#         'total_pairs': total_pairs,
#         'reasoning_b_no_match': reasoning_b_no_match,
#         'reasoning_a_no_match': reasoning_a_no_match,
#         'detailed_results': detailed_results
#     }

# def print_results_in_requested_format(results, filename):
#     """
#     Print results in the specific format requested.
#     """
#     total = results['total_pairs']
#     b_no_match = results['reasoning_b_no_match']
#     a_no_match = results['reasoning_a_no_match']
    
#     if total > 0:
#         b_percentage = (b_no_match / total) * 100
#         a_percentage = (a_no_match / total) * 100
#     else:
#         b_percentage = 0
#         a_percentage = 0
    
#     print("\n" + "="*60)
#     print(f"ANALYSIS RESULTS: {filename}")
#     print("="*60)
#     print("\nCheck Type                           Count    Percentage")
#     print("-" * 60)
#     print(f"Reasoning B doesn't match Input A/Output A\t{b_no_match}\t{b_percentage:.1f}%")
#     print(f"Reasoning A doesn't match Input B/Output B\t{a_no_match}\t{a_percentage:.1f}%")
#     print("-" * 60)
#     print(f"Total pairs analyzed: {total}")
    
#     # Also show yes counts for completeness
#     if total > 0:
#         b_yes_count = total - b_no_match
#         a_yes_count = total - a_no_match
#         print(f"\nConsistency counts:")
#         print(f"A→B consistent (Reasoning B matches Input A/Output A): {b_yes_count} ({(b_yes_count/total)*100:.1f}%)")
#         print(f"B→A consistent (Reasoning A matches Input B/Output B): {a_yes_count} ({(a_yes_count/total)*100:.1f}%)")

# def save_detailed_results(results, output_file):
#     """
#     Save detailed results to a JSON file.
#     """
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(results, f, indent=2, ensure_ascii=False)
    
#     print(f"\nDetailed results saved to: {output_file}")

# def main():
#     """
#     Main function to analyze JSONL files.
#     """
#     import argparse
    
#     parser = argparse.ArgumentParser(description='Analyze cross-consistency check results in JSONL files')
#     parser.add_argument('--input', '-i', type=str, required=True,
#                        help='Input JSONL file or directory containing JSONL files')
#     parser.add_argument('--output', '-o', type=str, default='consistency_analysis.json',
#                        help='Output file for detailed results (default: consistency_analysis.json)')
#     parser.add_argument('--summary-only', '-s', action='store_true',
#                        help='Show only summary without detailed results')
    
#     args = parser.parse_args()
    
#     # Find JSONL files
#     input_path = Path(args.input)
#     jsonl_files = []
    
#     if input_path.is_file() and input_path.suffix == '.jsonl':
#         jsonl_files = [input_path]
#     elif input_path.is_dir():
#         jsonl_files = list(input_path.glob('*.jsonl'))
#     else:
#         print(f"Error: {args.input} is not a valid JSONL file or directory")
#         return
    
#     if not jsonl_files:
#         print(f"No JSONL files found in {args.input}")
#         return
    
#     print(f"Found {len(jsonl_files)} JSONL file(s)")
    
#     all_results = []
#     file_results = []
    
#     for jsonl_file in jsonl_files:
#         print(f"\nAnalyzing: {jsonl_file}")
        
#         results = analyze_jsonl_file(jsonl_file)
#         filename = jsonl_file.name
        
#         # Print results in requested format
#         print_results_in_requested_format(results, filename)
        
#         # Store results for overall summary
#         file_results.append({
#             'filename': str(jsonl_file),
#             'results': results
#         })
        
#         # Add to all detailed results
#         for detail in results['detailed_results']:
#             detail['source_file'] = filename
#             all_results.append(detail)
    
#     # Generate overall summary if multiple files
#     if len(jsonl_files) > 1:
#         total_pairs = sum(r['results']['total_pairs'] for r in file_results)
#         total_b_no_match = sum(r['results']['reasoning_b_no_match'] for r in file_results)
#         total_a_no_match = sum(r['results']['reasoning_a_no_match'] for r in file_results)
        
#         if total_pairs > 0:
#             total_b_percentage = (total_b_no_match / total_pairs) * 100
#             total_a_percentage = (total_a_no_match / total_pairs) * 100
#         else:
#             total_b_percentage = 0
#             total_a_percentage = 0
        
#         print("\n" + "="*60)
#         print("OVERALL SUMMARY (All Files)")
#         print("="*60)
#         print("\nCheck Type                           Count    Percentage")
#         print("-" * 60)
#         print(f"Reasoning B doesn't match Input A/Output A\t{total_b_no_match}\t{total_b_percentage:.1f}%")
#         print(f"Reasoning A doesn't match Input B/Output B\t{total_a_no_match}\t{total_a_percentage:.1f}%")
#         print("-" * 60)
#         print(f"Total pairs analyzed: {total_pairs}")
#         print(f"Number of files: {len(jsonl_files)}")
    
#     # Save detailed results
#     if not args.summary_only:
#         output_data = {
#             'file_results': file_results,
#             'all_detailed_results': all_results
#         }
#         save_detailed_results(output_data, args.output)

# if __name__ == "__main__":
#     main()
# reparse_mistral_files.py
# enhanced_strip_mistral.py
# parse_correctly.py
# import json
# import re
# import os
# import glob

# def parse_raw_output_for_answer(raw_output):
#     """Parse raw output to extract yes/no answer"""
#     if not raw_output:
#         return "unknown"
    
#     # Look for "Answer: yes" or "Answer: no" patterns
#     patterns = [
#         r'Answer:\s*(yes|no)\s*$',
#         r'Answer:\s*(yes|no)[\s\.]',
#         r'^Answer:\s*(yes|no)\s*\n',
#         r'"Answer":\s*"(yes|no)"',
#         r"'Answer':\s*'(yes|no)'",
#         r'ANSWER:\s*(yes|no)',
#         r'answer:\s*(yes|no)',
#         r'\b(yes|no)\b\s*$'  # Just yes/no at end
#     ]
    
#     for pattern in patterns:
#         match = re.search(pattern, raw_output, re.IGNORECASE)
#         if match:
#             return match.group(1).lower()
    
#     return "unknown"

# def analyze_file_correctly(filepath):
#     """Analyze file using raw_output instead of is_consistent"""
#     stats = {
#         'total': 0,
#         'fully_consistent': 0,
#         'flag_1': 0,  # A_to_B inconsistent
#         'flag_2': 0,  # B_to_A inconsistent
#         'flag_3': 0,  # Question A biased
#         'flag_4': 0   # Question B biased
#     }
    
#     try:
#         with open(filepath, 'r') as f:
#             for line_num, line in enumerate(f, 1):
#                 if not line.strip():
#                     continue
                
#                 try:
#                     data = json.loads(line.strip())
#                     stats['total'] += 1
                    
#                     # Get cross consistency checks
#                     checks = data.get('cross_consistency_checks', {})
#                     a_to_b = checks.get('A_to_B', {})
#                     b_to_a = checks.get('B_to_A', {})
                    
#                     # Parse raw_output for actual answers
#                     a_to_b_raw = a_to_b.get('raw_output', '')
#                     b_to_a_raw = b_to_a.get('raw_output', '')
                    
#                     a_to_b_answer = parse_raw_output_for_answer(a_to_b_raw)
#                     b_to_a_answer = parse_raw_output_for_answer(b_to_a_raw)
                    
#                     # Count fully consistent (both yes)
#                     if a_to_b_answer == 'yes' and b_to_a_answer == 'yes':
#                         stats['fully_consistent'] += 1
                    
#                     # Flag 1: A_to_B is no
#                     if a_to_b_answer == 'no':
#                         stats['flag_1'] += 1
                    
#                     # Flag 2: B_to_A is no
#                     if b_to_a_answer == 'no':
#                         stats['flag_2'] += 1
                    
#                     # Get question guessing
#                     guessing = data.get('question_guessing', {})
                    
#                     # Flag 3: Question A biased
#                     qa = guessing.get('question_a_analysis', {})
#                     if qa.get('is_biased') is True:  # Explicitly check for True
#                         stats['flag_3'] += 1
#                     # Also check if the field exists and is true (not just truthy)
#                     elif 'is_biased' in qa and qa['is_biased']:
#                         stats['flag_3'] += 1
                    
#                     # Flag 4: Question B biased
#                     qb = guessing.get('question_b_analysis', {})
#                     if qb.get('is_biased') is True:
#                         stats['flag_4'] += 1
#                     elif 'is_biased' in qb and qb['is_biased']:
#                         stats['flag_4'] += 1
                        
#                 except json.JSONDecodeError as e:
#                     print(f"  JSON error line {line_num}: {e}")
#                     continue
#                 except Exception as e:
#                     print(f"  Error line {line_num}: {e}")
#                     continue
                    
#     except Exception as e:
#         print(f"Error reading {filepath}: {e}")
    
#     return stats

# def analyze_deepseek_issue(filepath):
#     """Special analysis for DeepSeek files that show 100% bias"""
#     print(f"\nAnalyzing DeepSeek file: {os.path.basename(filepath)}")
#     print("=" * 60)
    
#     try:
#         with open(filepath, 'r') as f:
#             first_line = f.readline()
#             if first_line:
#                 data = json.loads(first_line)
#                 guessing = data.get('question_guessing', {})
#                 qa = guessing.get('question_a_analysis', {})
#                 qb = guessing.get('question_b_analysis', {})
                
#                 print(f"Question A analysis keys: {list(qa.keys())}")
#                 print(f"Question A is_biased: {qa.get('is_biased')}")
#                 print(f"Question A is_biased type: {type(qa.get('is_biased'))}")
#                 print(f"Question A bias_reason: {qa.get('bias_reason')}")
                
#                 print(f"\nQuestion B analysis keys: {list(qb.keys())}")
#                 print(f"Question B is_biased: {qb.get('is_biased')}")
#                 print(f"Question B is_biased type: {type(qb.get('is_biased'))}")
#                 print(f"Question B bias_reason: {qb.get('bias_reason')}")
                
#                 # Check a few more lines
#                 f.seek(0)
#                 biased_counts = {'a': 0, 'b': 0, 'total': 0}
#                 for i, line in enumerate(f):
#                     if i >= 5:  # Check first 5 lines
#                         break
#                     data = json.loads(line.strip())
#                     guessing = data.get('question_guessing', {})
#                     qa = guessing.get('question_a_analysis', {})
#                     qb = guessing.get('question_b_analysis', {})
                    
#                     biased_counts['total'] += 1
#                     if qa.get('is_biased'):
#                         biased_counts['a'] += 1
#                     if qb.get('is_biased'):
#                         biased_counts['b'] += 1
                
#                 print(f"\nFirst 5 lines analysis:")
#                 print(f"  Question A biased: {biased_counts['a']}/5")
#                 print(f"  Question B biased: {biased_counts['b']}/5")
                
#     except Exception as e:
#         print(f"Error: {e}")

# def main():
#     # Your missing analyses
#     analyses = [
#         ('mistral', 'Religion', 'ambig'),
#         ('deepseek', 'Religion', 'ambig')
#         ('deepseek', 'Race_ethnicity', 'ambig'),
#         ('mistral', 'Race_ethnicity', 'ambig'),
#     ]
    
#     print("CORRECT PARSING OF EXISTING FILES")
#     print("=" * 60)
    
#     for model, subset, context in analyses:
#         print(f"\n{'='*60}")
#         print(f"Analysis: {model.upper()} - {subset} - {context}")
#         print(f"{'='*60}")
        
#         # Determine directory
#         if model == 'mistral':
#             results_dir = 'mistralai_mixtral-8x22b-instruct-v0.1_results'
#         elif model == 'deepseek':
#             results_dir = 'deepseek-reasoner_results'
#         else:
#             results_dir = 'openai_gpt-oss-20b_results'
        
#         if not os.path.exists(results_dir):
#             print(f"Directory not found: {results_dir}")
#             continue
        
#         # Find files
#         files = []
#         patterns = [
#             f"{results_dir}/cross_consistency_{subset}_{context}_consistent.jsonl",
#             f"{results_dir}/cross_consistency_{subset}_{context}_mixed.jsonl",
#             f"{results_dir}/cross_consistency_{subset}_{context}_consistent_*.jsonl",
#             f"{results_dir}/cross_consistency_{subset}_{context}_mixed_*.jsonl"
#         ]
        
#         for pattern in patterns:
#             for filepath in glob.glob(pattern):
#                 if os.path.exists(filepath):
#                     files.append(filepath)
        
#         if not files:
#             print(f"No files found for {subset}_{context}")
#             continue
        
#         # Analyze each file
#         total_stats = {
#             'total': 0,
#             'fully_consistent': 0,
#             'flag_1': 0,
#             'flag_2': 0,
#             'flag_3': 0,
#             'flag_4': 0
#         }
        
#         for filepath in files:
#             print(f"\nParsing: {os.path.basename(filepath)}")
#             stats = analyze_file_correctly(filepath)
            
#             for key in total_stats:
#                 total_stats[key] += stats[key]
        
#         # Print results
#         if total_stats['total'] > 0:
#             print(f"\n📊 FINAL RESULTS for {model.upper()} - {subset} - {context}:")
#             print(f"Total pairs: {total_stats['total']}")
#             print(f"Fully consistent: {total_stats['fully_consistent']} ({total_stats['fully_consistent']/total_stats['total']*100:.1f}%)")
#             print(f"Flag 1 (Reasoning B doesn't match): {total_stats['flag_1']} ({total_stats['flag_1']/total_stats['total']*100:.1f}%)")
#             print(f"Flag 2 (Reasoning A doesn't match): {total_stats['flag_2']} ({total_stats['flag_2']/total_stats['total']*100:.1f}%)")
#             print(f"Flag 3 (Question A bias): {total_stats['flag_3']} ({total_stats['flag_3']/total_stats['total']*100:.1f}%)")
#             print(f"Flag 4 (Question B bias): {total_stats['flag_4']} ({total_stats['flag_4']/total_stats['total']*100:.1f}%)")
            
#             # Format for your notes
#             print(f"\n```{{r {subset} {context}}}")
#             print(f"Total pairs: {total_stats['total']}")
#             print(f"{model.upper()} <-")
#             print(f"  'Fully consistent': {total_stats['fully_consistent']}")
#             print(f"  'Reasoning B doesnt match': {total_stats['flag_1']}")
#             print(f"  'Reasoning A doesnt match': {total_stats['flag_2']}")
#             print(f"  'Guessed Question doesnt resemble question a': {total_stats['flag_3']}")
#             print(f"  'Guessed Question doesnt resemble question b': {total_stats['flag_4']}")
#             print(f"```")
        
#         # Special debug for DeepSeek
#         if model == 'deepseek' and subset == 'Race_ethnicity':
#             print(f"\n{'='*60}")
#             print("DEBUGGING DEEPSEEK 100% BIAS ISSUE")
#             print(f"{'='*60}")
#             for filepath in files:
#                 analyze_deepseek_issue(filepath)

# if __name__ == "__main__":
#     main()
import json
import re
import os
import glob

def parse_raw_output_for_answer(raw_output):
    """Parse raw output to extract yes/no answer"""
    if not raw_output:
        return "unknown"
    
    # Look for "Answer: yes" or "Answer: no" patterns
    patterns = [
        r'Answer:\s*(yes|no)\s*$',
        r'Answer:\s*(yes|no)[\s\.]',
        r'^Answer:\s*(yes|no)\s*\n',
        r'"Answer":\s*"(yes|no)"',
        r"'Answer':\s*'(yes|no)'",
        r'ANSWER:\s*(yes|no)',
        r'answer:\s*(yes|no)',
        r'\b(yes|no)\b\s*$'  # Just yes/no at end
    ]
    
    for pattern in patterns:
        match = re.search(pattern, raw_output, re.IGNORECASE)
        if match:
            return match.group(1).lower()
    
    return "unknown"

def parse_boolean_value(value):
    """Parse boolean value that might be string or boolean"""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['true', 'yes', '1']
    return bool(value)

def analyze_file_correctly(filepath):
    """Analyze file using raw_output instead of is_consistent"""
    stats = {
        'total': 0,
        'fully_consistent': 0,
        'flag_1': 0,  # A_to_B inconsistent
        'flag_2': 0,  # B_to_A inconsistent
        'flag_3': 0,  # Question A biased
        'flag_4': 0,  # Question B biased
        'any_flag': 0  # Pairs with at least one flag
    }
    
    try:
        with open(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                
                try:
                    data = json.loads(line.strip())
                    stats['total'] += 1
                    
                    # Get cross consistency checks
                    checks = data.get('cross_consistency_checks', {})
                    a_to_b = checks.get('A_to_B', {})
                    b_to_a = checks.get('B_to_A', {})
                    
                    # Parse raw_output for actual answers
                    a_to_b_raw = a_to_b.get('raw_output', '')
                    b_to_a_raw = b_to_a.get('raw_output', '')
                    
                    a_to_b_answer = parse_raw_output_for_answer(a_to_b_raw)
                    b_to_a_answer = parse_raw_output_for_answer(b_to_a_raw)
                    
                    # Count fully consistent (both yes)
                    if a_to_b_answer == 'yes' and b_to_a_answer == 'yes':
                        stats['fully_consistent'] += 1
                    
                    # Flag 1: A_to_B is no
                    flag_1 = a_to_b_answer == 'no'
                    if flag_1:
                        stats['flag_1'] += 1
                    
                    # Flag 2: B_to_A is no
                    flag_2 = b_to_a_answer == 'no'
                    if flag_2:
                        stats['flag_2'] += 1
                    
                    # Get question guessing
                    guessing = data.get('question_guessing', {})
                    
                    # Flag 3: Question A biased
                    qa = guessing.get('question_a_analysis', {})
                    flag_3 = parse_boolean_value(qa.get('is_biased'))
                    if flag_3:
                        stats['flag_3'] += 1
                    
                    # Flag 4: Question B biased
                    qb = guessing.get('question_b_analysis', {})
                    flag_4 = parse_boolean_value(qb.get('is_biased'))
                    if flag_4:
                        stats['flag_4'] += 1
                    
                    # Count if any flag is present
                    if flag_1 or flag_2 or flag_3 or flag_4:
                        stats['any_flag'] += 1
                        
                except json.JSONDecodeError as e:
                    print(f"  JSON error line {line_num}: {e}")
                    continue
                except Exception as e:
                    print(f"  Error line {line_num}: {e}")
                    continue
                    
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    return stats

def analyze_deepseek_issue(filepath):
    """Special analysis for DeepSeek files that show 100% bias"""
    print(f"\nAnalyzing DeepSeek file: {os.path.basename(filepath)}")
    print("=" * 60)
    
    try:
        with open(filepath, 'r') as f:
            first_line = f.readline()
            if first_line:
                data = json.loads(first_line)
                guessing = data.get('question_guessing', {})
                qa = guessing.get('question_a_analysis', {})
                qb = guessing.get('question_b_analysis', {})
                
                print(f"Question A analysis keys: {list(qa.keys())}")
                print(f"Question A is_biased: {qa.get('is_biased')}")
                print(f"Question A is_biased type: {type(qa.get('is_biased'))}")
                print(f"Question A bias_reason: {qa.get('bias_reason')}")
                
                print(f"\nQuestion B analysis keys: {list(qb.keys())}")
                print(f"Question B is_biased: {qb.get('is_biased')}")
                print(f"Question B is_biased type: {type(qb.get('is_biased'))}")
                print(f"Question B bias_reason: {qb.get('bias_reason')}")
                
                # Check a few more lines
                f.seek(0)
                biased_counts = {'a': 0, 'b': 0, 'total': 0}
                for i, line in enumerate(f):
                    if i >= 5:  # Check first 5 lines
                        break
                    data = json.loads(line.strip())
                    guessing = data.get('question_guessing', {})
                    qa = guessing.get('question_a_analysis', {})
                    qb = guessing.get('question_b_analysis', {})
                    
                    biased_counts['total'] += 1
                    if parse_boolean_value(qa.get('is_biased')):
                        biased_counts['a'] += 1
                    if parse_boolean_value(qb.get('is_biased')):
                        biased_counts['b'] += 1
                
                print(f"\nFirst 5 lines analysis:")
                print(f"  Question A biased: {biased_counts['a']}/5")
                print(f"  Question B biased: {biased_counts['b']}/5")
                
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Your missing analyses
    analyses = [
        ('mistral', 'Religion', 'ambig'),
        ('deepseek', 'Religion', 'ambig'),
        ('deepseek', 'Race_ethnicity', 'ambig'),
        ('mistral', 'Race_ethnicity', 'ambig'),
    ]
    
    print("CORRECT PARSING OF EXISTING FILES")
    print("=" * 60)
    
    for model, subset, context in analyses:
        print(f"\n{'='*60}")
        print(f"Analysis: {model.upper()} - {subset} - {context}")
        print(f"{'='*60}")
        
        # Determine directory
        if model == 'mistral':
            results_dir = 'mistralai_mixtral-8x22b-instruct-v0.1_results'
        elif model == 'deepseek':
            results_dir = 'deepseek-reasoner_results'
        else:
            results_dir = 'openai_gpt-oss-20b_results'
        
        if not os.path.exists(results_dir):
            print(f"Directory not found: {results_dir}")
            continue
        
        # Find files
        files = []
        patterns = [
            f"{results_dir}/cross_consistency_{subset}_{context}_consistent.jsonl",
            f"{results_dir}/cross_consistency_{subset}_{context}_mixed.jsonl",
            f"{results_dir}/cross_consistency_{subset}_{context}_consistent_*.jsonl",
            f"{results_dir}/cross_consistency_{subset}_{context}_mixed_*.jsonl"
        ]
        
        for pattern in patterns:
            for filepath in glob.glob(pattern):
                if os.path.exists(filepath):
                    files.append(filepath)
        
        if not files:
            print(f"No files found for {subset}_{context}")
            continue
        
        # Analyze each file
        total_stats = {
            'total': 0,
            'fully_consistent': 0,
            'flag_1': 0,
            'flag_2': 0,
            'flag_3': 0,
            'flag_4': 0,
            'any_flag': 0
        }
        
        for filepath in files:
            print(f"\nParsing: {os.path.basename(filepath)}")
            stats = analyze_file_correctly(filepath)
            
            for key in total_stats:
                total_stats[key] += stats[key]
        
        # Print results
        if total_stats['total'] > 0:
            print(f"\n📊 FINAL RESULTS for {model.upper()} - {subset} - {context}:")
            print(f"Total pairs: {total_stats['total']}")
            print(f"Fully consistent: {total_stats['fully_consistent']} ({total_stats['fully_consistent']/total_stats['total']*100:.1f}%)")
            print(f"Flag 1 (Reasoning B doesn't match): {total_stats['flag_1']} ({total_stats['flag_1']/total_stats['total']*100:.1f}%)")
            print(f"Flag 2 (Reasoning A doesn't match): {total_stats['flag_2']} ({total_stats['flag_2']/total_stats['total']*100:.1f}%)")
            print(f"Flag 3 (Question A bias): {total_stats['flag_3']} ({total_stats['flag_3']/total_stats['total']*100:.1f}%)")
            print(f"Flag 4 (Question B bias): {total_stats['flag_4']} ({total_stats['flag_4']/total_stats['total']*100:.1f}%)")
            print(f"Pairs with ANY flag: {total_stats['any_flag']} ({total_stats['any_flag']/total_stats['total']*100:.1f}%)")
            
            # Format for your notes
            print(f"\n```{{r {subset} {context}}}")
            print(f"Total pairs: {total_stats['total']}")
            print(f"{model.upper()} <-")
            print(f"  'Fully consistent': {total_stats['fully_consistent']}")
            print(f"  'Reasoning B doesnt match': {total_stats['flag_1']}")
            print(f"  'Reasoning A doesnt match': {total_stats['flag_2']}")
            print(f"  'Guessed Question doesnt resemble question a': {total_stats['flag_3']}")
            print(f"  'Guessed Question doesnt resemble question b': {total_stats['flag_4']}")
            print(f"  'Pairs with any flag': {total_stats['any_flag']}")
            print(f"```")
        
        # Special debug for DeepSeek
        if model == 'deepseek' and subset == 'Race_ethnicity':
            print(f"\n{'='*60}")
            print("DEBUGGING DEEPSEEK 100% BIAS ISSUE")
            print(f"{'='*60}")
            for filepath in files:
                analyze_deepseek_issue(filepath)

if __name__ == "__main__":
    main()