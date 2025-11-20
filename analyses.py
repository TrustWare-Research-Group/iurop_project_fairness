import json
import pandas as pd
from collections import Counter, defaultdict
import re
import os
from datetime import datetime
import glob

def load_jsonl(file_path):
    """Load JSONL file and return list of records."""
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line.strip()))
    return records

def parse_actual_prompt_content(prompt):
    """Extract the actual context, question, and choices from the prompt (not the example)."""
    
    # Split by the separator to get the actual content after the example
    parts = prompt.split('---')
    if len(parts) > 1:
        actual_content = parts[-1].strip()
    else:
        actual_content = prompt
    
    # Extract context, question, and choices from the actual content
    context_match = re.search(r'### Context:\s*(.*?)(?=### Question:|$)', actual_content, re.DOTALL)
    question_match = re.search(r'### Question:\s*(.*?)(?=### Choices:|$)', actual_content, re.DOTALL)
    choices_match = re.search(r'### Choices:\s*(.*?)(?=### Your answer:|$)', actual_content, re.DOTALL)
    
    context = context_match.group(1).strip() if context_match else "Not found"
    question = question_match.group(1).strip() if question_match else "Not found"
    choices_text = choices_match.group(1).strip() if choices_match else "Not found"
    
    # Parse the choices into a dictionary
    choices_dict = {}
    if choices_text:
        # Split by lines and extract choice number and text
        choice_lines = [line.strip() for line in choices_text.split('\n') if line.strip()]
        for line in choice_lines:
            # Match patterns like "1. The guy", "2. Cannot answer", etc.
            match = re.match(r'(\d+)\.\s*(.+)', line)
            if match:
                choice_num = match.group(1)
                choice_text = match.group(2)
                choices_dict[choice_num] = choice_text
    
    return {
        'context': context,
        'question': question,
        'choices': choices_dict,
        'choices_text': choices_text
    }

def analyze_reasoning_bias(consistent_records, mixed_records, consistent_file, mixed_file):
    """Analyze bias patterns in model reasoning across both consistent and mixed responses."""
    
    analysis_results = {
        "summary": {},
        "bias_patterns": [],
        "reasoning_analysis": {},
        "detailed_examples": [],
        "file_sources": {
            "consistent_file": consistent_file,
            "mixed_file": mixed_file,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    
    # Combine all records for analysis
    all_records = consistent_records + mixed_records
    
    # Summary statistics
    analysis_results["summary"] = {
        "total_pairs": len(all_records),
        "consistent_pairs": len(consistent_records),
        "mixed_cant_determine_pairs": len(mixed_records),
        "total_responses": len(all_records) * 2
    }
    
    # Bias detection in consistent pairs
    bias_pairs = [r for r in consistent_records if r["pair_analysis"]["bias_detected"]]
    analysis_results["summary"]["bias_pairs_count"] = len(bias_pairs)
    analysis_results["summary"]["bias_rate"] = len(bias_pairs) / len(consistent_records) if consistent_records else 0
    
    # Analyze reasoning patterns for bias
    reasoning_patterns = analyze_reasoning_patterns(all_records)
    analysis_results["reasoning_analysis"] = reasoning_patterns
    
    # Detailed bias analysis
    analysis_results["bias_patterns"] = analyze_bias_patterns(bias_pairs)
    
    # Case studies of clear bias examples
    analysis_results["detailed_examples"] = extract_bias_examples(bias_pairs)
    
    # Mixed pairs analysis
    analysis_results["mixed_pairs_analysis"] = analyze_mixed_pairs(mixed_records)
    
    return analysis_results

def analyze_reasoning_patterns(records):
    """Analyze patterns in reasoning that might indicate bias."""
    
    patterns = {
        "assumption_patterns": Counter(),
        "stereotyping_indicators": Counter(),
        "language_biases": Counter(),
        "certainty_levels": Counter()
    }
    
    # Enhanced bias indicators in reasoning
    stereotyping_phrases = [
        (r'\b(typical|usually|always|never|all|every)\b.*\b(man|woman|male|female|guy|girl|boy|grandmother|grandfather)', "gender_stereotyping"),
        (r'\b(should|ought to)\b.*\b(behave|act|think|parent)\b', "prescriptive_stereotyping"),
        (r'\b(because he|because she|as a man|as a woman)\b', "gender_assumption"),
        (r'\b(emotional|rational|strong|weak|nurturing|assertive)\b.*\b(man|woman|male|female)', "trait_stereotyping"),
        (r'\b(young|old).*(should|would)\b', "age_stereotyping"),
        (r'\b(pregnant).*(emotional|sensitive|moody|irrational)\b', "pregnancy_stereotyping"),
        (r'\b(mother|father).*(should|always|never)\b', "parent_role_stereotyping")
    ]
    
    assumption_phrases = [
        (r'\b(assum|presum)\b', "explicit_assumption"),
        (r'\b(likely|probably|seems like)\b', "probability_assumption"),
        (r'\b(without evidence|based on|from the context)\b', "context_assumption"),
        (r'\b(might be|could be|possibly)\b', "possibility_assumption")
    ]
    
    certainty_phrases = {
        "high": [(r'\b(clearly|obviously|definitely|certainly|without doubt)\b', "high_certainty")],
        "medium": [(r'\b(probably|likely|seems|appears)\b', "medium_certainty")],
        "low": [(r'\b(possibly|might|could|maybe|perhaps)\b', "low_certainty")]
    }
    
    for record in records:
        for response_key in ['response_a', 'response_b']:
            reasoning = record['model_responses'][response_key]['reasoning'].lower()
            
            # Check for stereotyping language
            for pattern, category in stereotyping_phrases:
                if re.search(pattern, reasoning, re.IGNORECASE):
                    patterns["stereotyping_indicators"][category] += 1
            
            # Check for assumption language
            for pattern, category in assumption_phrases:
                if re.search(pattern, reasoning, re.IGNORECASE):
                    patterns["assumption_patterns"][category] += 1
            
            # Check certainty levels
            for level, level_patterns in certainty_phrases.items():
                for pattern, category in level_patterns:
                    if re.search(pattern, reasoning, re.IGNORECASE):
                        patterns["certainty_levels"][level] += 1
    
    return patterns

def extract_demographic_groups(text):
    """Extract demographic groups from text with better precision."""
    groups = set()
    
    # Gender terms
    gender_terms = ['man', 'woman', 'male', 'female', 'boy', 'girl', 
                   'gentleman', 'lady', 'guy', 'gal']
    
    # Family/relation terms
    family_terms = ['grandmother', 'grandfather', 'mother', 'father', 
                   'wife', 'husband', 'sister', 'brother', 'son', 'daughter']
    
    # Life stage terms
    life_terms = ['pregnant', 'elderly', 'young', 'old', 'teenager', 'child']
    
    text_lower = text.lower()
    
    for term in gender_terms + family_terms + life_terms:
        if re.search(r'\b' + term + r'\b', text_lower):
            groups.add(term)
    
    return list(groups)

def analyze_bias_patterns(bias_pairs):
    """Analyze specific bias patterns in pairs where bias was detected."""
    
    bias_categories = defaultdict(list)
    
    for pair in bias_pairs:
        # Determine which response was correct and which was wrong
        correct_response = 'a' if pair['model_responses']['response_a']['is_correct'] else 'b'
        wrong_response = 'b' if correct_response == 'a' else 'a'
        
        # Parse the actual prompt content (not the example)
        prompt_a_content = parse_actual_prompt_content(pair['evaluation_data']['prompt_a'])
        prompt_b_content = parse_actual_prompt_content(pair['evaluation_data']['prompt_b'])
        
        # Extract the demographic/social groups from actual context
        groups_a = extract_demographic_groups(prompt_a_content['context'])
        groups_b = extract_demographic_groups(prompt_b_content['context'])
        
        # Analyze the reasoning differences
        correct_reasoning = pair['model_responses'][f'response_{correct_response}']['reasoning']
        wrong_reasoning = pair['model_responses'][f'response_{wrong_response}']['reasoning']
        
        bias_pattern = {
            'pair_index': pair['metadata']['pair_index'],
            'groups_a': groups_a,
            'groups_b': groups_b,
            'reasoning_differences': find_reasoning_differences(correct_reasoning, wrong_reasoning),
            'bias_type': classify_bias_type(correct_reasoning, wrong_reasoning, groups_a, groups_b),
            'correct_answer_a': pair['evaluation_data']['correct_answer_a'],
            'correct_answer_b': pair['evaluation_data']['correct_answer_b'],
            'model_answer_a': pair['model_responses']['response_a']['extracted_answer'],
            'model_answer_b': pair['model_responses']['response_b']['extracted_answer'],
            'question_a': prompt_a_content['question'],
            'question_b': prompt_b_content['question'],
            'choices_a': prompt_a_content['choices'],
            'choices_b': prompt_b_content['choices']
        }
        
        bias_categories[bias_pattern['bias_type']].append(bias_pattern)
    
    return bias_categories

def find_reasoning_differences(reasoning1, reasoning2):
    """Find key differences between two reasoning texts."""
    # Extract meaningful content words (nouns, adjectives, verbs)
    words1 = set(re.findall(r'\b[a-z]{4,}\b', reasoning1.lower()))
    words2 = set(re.findall(r'\b[a-z]{4,}\b', reasoning2.lower()))
    
    unique_to_1 = words1 - words2
    unique_to_2 = words2 - words1
    
    # Filter for meaningful differences (exclude common words)
    common_words = {'that', 'with', 'have', 'this', 'from', 'they', 'their', 'there', 'which', 'about', 'because', 'would', 'could'}
    meaningful_1 = [w for w in unique_to_1 if w not in common_words]
    meaningful_2 = [w for w in unique_to_2 if w not in common_words]
    
    return {
        'unique_to_correct': meaningful_1[:8],
        'unique_to_wrong': meaningful_2[:8],
        'total_difference_score': len(meaningful_1) + len(meaningful_2)
    }

def classify_bias_type(reasoning_correct, reasoning_wrong, groups_a, groups_b):
    """Classify the type of bias based on reasoning patterns."""
    
    reasoning_correct_lower = reasoning_correct.lower()
    reasoning_wrong_lower = reasoning_wrong.lower()
    
    # Check for gender-based stereotyping
    gender_terms = ['man', 'woman', 'male', 'female', 'mother', 'father', 'wife', 'husband']
    for term in gender_terms:
        if (term in reasoning_wrong_lower and term not in reasoning_correct_lower) or \
           (term in reasoning_correct_lower and term not in reasoning_wrong_lower):
            return "gender_bias"
    
    # Check for parenting role stereotyping
    parenting_terms = ['parent', 'parenting', 'mother', 'father', 'maternal', 'paternal']
    parenting_indicators = 0
    for term in parenting_terms:
        if term in reasoning_wrong_lower:
            parenting_indicators += 1
        if term in reasoning_correct_lower:
            parenting_indicators -= 1
    
    if abs(parenting_indicators) >= 2:
        return "parenting_role_bias"
    
    # Check for pregnancy-related bias
    pregnancy_terms = ['pregnant', 'pregnancy', 'hormonal', 'emotional']
    pregnancy_indicators = 0
    for term in pregnancy_terms:
        if term in reasoning_wrong_lower:
            pregnancy_indicators += 1
        if term in reasoning_correct_lower:
            pregnancy_indicators -= 1
    
    if abs(pregnancy_indicators) >= 2:
        return "pregnancy_bias"
    
    # Check for certainty bias
    high_certainty_terms = ['clearly', 'obviously', 'definitely', 'certainly', 'without doubt']
    low_certainty_terms = ['possibly', 'might', 'could', 'maybe', 'perhaps', 'uncertain']
    
    high_certainty_wrong = sum(1 for term in high_certainty_terms if term in reasoning_wrong_lower)
    high_certainty_correct = sum(1 for term in high_certainty_terms if term in reasoning_correct_lower)
    low_certainty_wrong = sum(1 for term in low_certainty_terms if term in reasoning_wrong_lower)
    low_certainty_correct = sum(1 for term in low_certainty_terms if term in reasoning_correct_lower)
    
    if (high_certainty_wrong > high_certainty_correct and low_certainty_correct > low_certainty_wrong):
        return "certainty_bias"
    
    return "unclassified_bias"

def extract_bias_examples(bias_pairs, max_examples=5):
    """Extract clear examples of bias for detailed analysis."""
    examples = []
    
    for i, pair in enumerate(bias_pairs[:max_examples]):
        correct_a = pair['model_responses']['response_a']['is_correct']
        
        # Parse the actual prompt content (not the example)
        prompt_a_content = parse_actual_prompt_content(pair['evaluation_data']['prompt_a'])
        prompt_b_content = parse_actual_prompt_content(pair['evaluation_data']['prompt_b'])
        
        example = {
            'pair_index': pair['metadata']['pair_index'],
            'context_a': prompt_a_content['context'],
            'context_b': prompt_b_content['context'],
            'question_a': prompt_a_content['question'],
            'question_b': prompt_b_content['question'],
            'choices_a': prompt_a_content['choices'],
            'choices_b': prompt_b_content['choices'],
            'correct_answer_a': pair['evaluation_data']['correct_answer_a'],
            'correct_answer_b': pair['evaluation_data']['correct_answer_b'],
            'response_a': {
                'answer': pair['model_responses']['response_a']['extracted_answer'],
                'correct': pair['model_responses']['response_a']['is_correct'],
                'reasoning': pair['model_responses']['response_a']['reasoning']
            },
            'response_b': {
                'answer': pair['model_responses']['response_b']['extracted_answer'],
                'correct': pair['model_responses']['response_b']['is_correct'],
                'reasoning': pair['model_responses']['response_b']['reasoning']
            },
            'bias_interpretation': interpret_bias_example(pair),
            'detected_groups_a': extract_demographic_groups(prompt_a_content['context']),
            'detected_groups_b': extract_demographic_groups(prompt_b_content['context'])
        }
        examples.append(example)
    
    return examples

def interpret_bias_example(pair):
    """Provide an interpretation of the bias in a given example."""
    correct_a = pair['model_responses']['response_a']['is_correct']
    
    if correct_a:
        correct_prompt = pair['evaluation_data']['prompt_a']
        wrong_prompt = pair['evaluation_data']['prompt_b']
        correct_reasoning = pair['model_responses']['response_a']['reasoning']
        wrong_reasoning = pair['model_responses']['response_b']['reasoning']
    else:
        correct_prompt = pair['evaluation_data']['prompt_b']
        wrong_prompt = pair['evaluation_data']['prompt_a']
        correct_reasoning = pair['model_responses']['response_b']['reasoning']
        wrong_reasoning = pair['model_responses']['response_a']['reasoning']
    
    # Parse actual content to get context for group extraction
    correct_content = parse_actual_prompt_content(correct_prompt)
    wrong_content = parse_actual_prompt_content(wrong_prompt)
    
    # Extract demographic groups from actual context
    groups_correct = extract_demographic_groups(correct_content['context'])
    groups_wrong = extract_demographic_groups(wrong_content['context'])
    
    interpretation = "The model showed differential reasoning for questions involving "
    
    if groups_correct and groups_wrong:
        interpretation += f"{', '.join(groups_correct)} vs {', '.join(groups_wrong)}. "
    else:
        interpretation += "different demographic groups. "
    
    # Add specific bias indicators
    bias_indicators = []
    
    # Check for stereotyping language
    stereotyping_terms = ['typical', 'usually', 'always', 'should', 'as a']
    for term in stereotyping_terms:
        if term in wrong_reasoning.lower() and term not in correct_reasoning.lower():
            bias_indicators.append(f"used stereotyping language ('{term}')")
            break
    
    # Check for assumption language
    assumption_terms = ['assume', 'presume', 'likely because']
    for term in assumption_terms:
        if term in wrong_reasoning.lower() and term not in correct_reasoning.lower():
            bias_indicators.append(f"made unfounded assumptions")
            break
    
    if bias_indicators:
        interpretation += f"The model {', '.join(bias_indicators)} only in the incorrect response."
    else:
        interpretation += "The reasoning patterns suggest inconsistent treatment of similar scenarios."
    
    return interpretation

def analyze_mixed_pairs(mixed_records):
    """Analyze mixed 'Can't determine' pairs for patterns."""
    analysis = {
        "total_mixed": len(mixed_records),
        "cant_determine_by_question": Counter(),
        "patterns": []
    }
    
    for record in mixed_records:
        # Determine which response was "Can't determine"
        if record['model_responses']['response_a']['is_cant_determine']:
            cant_determine_prompt = record['evaluation_data']['prompt_a']
            specific_prompt = record['evaluation_data']['prompt_b']
        else:
            cant_determine_prompt = record['evaluation_data']['prompt_b']
            specific_prompt = record['evaluation_data']['prompt_a']
        
        # Parse actual content
        cant_determine_content = parse_actual_prompt_content(cant_determine_prompt)
        specific_content = parse_actual_prompt_content(specific_prompt)
        
        # Extract demographic groups
        cant_determine_groups = extract_demographic_groups(cant_determine_content['context'])
        specific_groups = extract_demographic_groups(specific_content['context'])
        
        # Extract potential reasons for uncertainty
        pattern = {
            'pair_index': record['metadata']['pair_index'],
            'cant_determine_question': cant_determine_content['question'],
            'specific_question': specific_content['question'],
            'cant_determine_choices': cant_determine_content['choices'],
            'specific_choices': specific_content['choices'],
            'cant_determine_groups': cant_determine_groups,
            'specific_groups': specific_groups,
            'potential_reason': infer_uncertainty_reason(cant_determine_content, specific_content)
        }
        analysis['patterns'].append(pattern)
        
        # Count by question type
        analysis['cant_determine_by_question'][cant_determine_content['question'][:100]] += 1
    
    return analysis

def infer_uncertainty_reason(cant_determine_content, specific_content):
    """Infer potential reasons for model uncertainty in one prompt but not the other."""
    
    cant_groups = cant_determine_content.get('groups', [])
    spec_groups = specific_content.get('groups', [])
    
    # Look for demographic differences
    if cant_groups and spec_groups:
        unique_to_cant = set(cant_groups) - set(spec_groups)
        unique_to_spec = set(spec_groups) - set(cant_groups)
        
        if unique_to_cant:
            return f"Uncertainty may relate to: {', '.join(unique_to_cant)}"
        elif unique_to_spec:
            return f"Model was certain despite: {', '.join(unique_to_spec)}"
    
    # Look for question framing differences
    cant_question = cant_determine_content['question']
    spec_question = specific_content['question']
    
    if "good parent" in cant_question.lower() and "bad parent" in spec_question.lower():
        return "Uncertainty about 'good parent' but certain about 'bad parent'"
    elif "bad parent" in cant_question.lower() and "good parent" in spec_question.lower():
        return "Uncertainty about 'bad parent' but certain about 'good parent'"
    
    return "Uncertainty reason requires deeper analysis"

def format_choices_for_display(choices_dict):
    """Format choices dictionary for readable display."""
    if not choices_dict:
        return "No choices found"
    
    formatted = []
    for num, text in sorted(choices_dict.items(), key=lambda x: int(x[0])):
        formatted.append(f"{num}. {text}")
    return " | ".join(formatted)

def get_unique_output_filename(base_name, results_dir="results"):
    """Generate a unique filename for the analysis report."""
    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)
    
    # Check for existing files and increment counter
    counter = 1
    while True:
        if counter == 1:
            output_file = os.path.join(results_dir, f"{base_name}_analysis.md")
        else:
            output_file = os.path.join(results_dir, f"{base_name}_analysis_{counter}.md")
        
        if not os.path.exists(output_file):
            return output_file
        counter += 1

def generate_bias_report(analysis_results, output_file):
    """Generate a comprehensive markdown report of bias analysis."""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Model Bias Analysis Report\n\n")
        
        # File Sources Section
        f.write("## Data Sources\n\n")
        sources = analysis_results["file_sources"]
        f.write(f"- **Consistent Pairs File**: `{sources['consistent_file']}`\n")
        f.write(f"- **Mixed Pairs File**: `{sources['mixed_file']}`\n")
        f.write(f"- **Analysis Date**: {sources['analysis_date']}\n\n")
        
        # Summary Section
        f.write("## Executive Summary\n\n")
        summary = analysis_results["summary"]
        f.write(f"- **Total Pairs Analyzed**: {summary['total_pairs']}\n")
        f.write(f"- **Consistent Pairs**: {summary['consistent_pairs']}\n")
        f.write(f"- **Mixed 'Can't Determine' Pairs**: {summary['mixed_cant_determine_pairs']}\n")
        f.write(f"- **Pairs Showing Bias**: {summary['bias_pairs_count']} ({summary['bias_rate']*100:.1f}% of consistent pairs)\n\n")
        
        # Bias Patterns Section
        f.write("## Bias Patterns Detected\n\n")
        bias_patterns = analysis_results["bias_patterns"]
        
        if not bias_patterns:
            f.write("No specific bias patterns were classified. All biased pairs fell into 'unclassified_bias'.\n\n")
        else:
            for bias_type, patterns in bias_patterns.items():
                f.write(f"### {bias_type.replace('_', ' ').title()}\n")
                f.write(f"**Count**: {len(patterns)} pairs\n\n")
                
                for i, pattern in enumerate(patterns[:3], 1):
                    f.write(f"#### Example {i} (Pair {pattern['pair_index']})\n")
                    f.write(f"- **Groups in Context A**: {', '.join(pattern['groups_a']) if pattern['groups_a'] else 'None detected'}\n")
                    f.write(f"- **Groups in Context B**: {', '.join(pattern['groups_b']) if pattern['groups_b'] else 'None detected'}\n")
                    f.write(f"- **Question A**: {pattern['question_a']}\n")
                    f.write(f"- **Question B**: {pattern['question_b']}\n")
                    f.write(f"- **Choices A**: {format_choices_for_display(pattern['choices_a'])}\n")
                    f.write(f"- **Choices B**: {format_choices_for_display(pattern['choices_b'])}\n")
                    f.write(f"- **Correct Answers**: A={pattern['correct_answer_a']}, B={pattern['correct_answer_b']}\n")
                    f.write(f"- **Model Answers**: A={pattern['model_answer_a']}, B={pattern['model_answer_b']}\n")
                    f.write(f"- **Reasoning Differences**: {pattern['reasoning_differences']}\n\n")
        
        # Reasoning Analysis Section
        f.write("## Reasoning Pattern Analysis\n\n")
        reasoning = analysis_results["reasoning_analysis"]
        
        f.write("### Stereotyping Indicators\n")
        if reasoning["stereotyping_indicators"]:
            for category, count in reasoning["stereotyping_indicators"].most_common(10):
                f.write(f"- {category.replace('_', ' ').title()}: {count} occurrences\n")
        else:
            f.write("- No stereotyping indicators detected\n")
        f.write("\n")
        
        f.write("### Assumption Patterns\n")
        if reasoning["assumption_patterns"]:
            for category, count in reasoning["assumption_patterns"].most_common(10):
                f.write(f"- {category.replace('_', ' ').title()}: {count} occurrences\n")
        else:
            f.write("- No assumption patterns detected\n")
        f.write("\n")
        
        f.write("### Certainty Levels\n")
        for level, count in reasoning["certainty_levels"].items():
            f.write(f"- {level.title()} certainty: {count} occurrences\n")
        f.write("\n")
        
        # Detailed Examples Section
        f.write("## Detailed Bias Examples\n\n")
        for i, example in enumerate(analysis_results["detailed_examples"], 1):
            f.write(f"### Example {i}: Pair {example['pair_index']}\n\n")
            
            f.write("#### Context and Question A\n")
            f.write(f"**Context**: {example['context_a'][:200]}...\n\n")
            f.write(f"**Question**: {example['question_a']}\n")
            f.write(f"**Choices**: {format_choices_for_display(example['choices_a'])}\n")
            f.write(f"**Correct Answer**: {example['correct_answer_a']} ({example['choices_a'].get(example['correct_answer_a'], 'Unknown choice')})\n")
            f.write(f"**Detected Groups**: {', '.join(example['detected_groups_a']) if example['detected_groups_a'] else 'None'}\n\n")
            
            f.write("#### Context and Question B\n")
            f.write(f"**Context**: {example['context_b'][:200]}...\n\n")
            f.write(f"**Question**: {example['question_b']}\n")
            f.write(f"**Choices**: {format_choices_for_display(example['choices_b'])}\n")
            f.write(f"**Correct Answer**: {example['correct_answer_b']} ({example['choices_b'].get(example['correct_answer_b'], 'Unknown choice')})\n")
            f.write(f"**Detected Groups**: {', '.join(example['detected_groups_b']) if example['detected_groups_b'] else 'None'}\n\n")
            
            f.write("#### Model Response A\n")
            f.write(f"**Answer**: {example['response_a']['answer']} ({example['choices_a'].get(example['response_a']['answer'], 'Unknown choice')}) - **Correct**: {example['response_a']['correct']}\n")
            f.write("**Reasoning**:\n")
            f.write("> " + example['response_a']['reasoning'] + "\n\n")
            
            f.write("#### Model Response B\n")
            f.write(f"**Answer**: {example['response_b']['answer']} ({example['choices_b'].get(example['response_b']['answer'], 'Unknown choice')}) - **Correct**: {example['response_b']['correct']}\n")
            f.write("**Reasoning**:\n")
            f.write("> " + example['response_b']['reasoning'] + "\n\n")
            
            f.write("#### Bias Interpretation\n")
            f.write(f"{example['bias_interpretation']}\n\n")
            f.write("---\n\n")
        
        # Mixed Pairs Analysis
        if analysis_results["mixed_pairs_analysis"]["total_mixed"] > 0:
            f.write("## Mixed 'Can't Determine' Analysis\n\n")
            mixed = analysis_results["mixed_pairs_analysis"]
            f.write(f"**Total Mixed Pairs**: {mixed['total_mixed']}\n\n")
            
            for pattern in mixed['patterns'][:5]:
                f.write(f"### Pair {pattern['pair_index']}\n")
                f.write(f"**'Can't Determine' Question**: {pattern['cant_determine_question']}\n")
                f.write(f"**Choices**: {format_choices_for_display(pattern['cant_determine_choices'])}\n")
                f.write(f"**Groups**: {', '.join(pattern['cant_determine_groups']) if pattern['cant_determine_groups'] else 'None detected'}\n\n")
                f.write(f"**Specific Answer Question**: {pattern['specific_question']}\n")
                f.write(f"**Choices**: {format_choices_for_display(pattern['specific_choices'])}\n")
                f.write(f"**Groups**: {', '.join(pattern['specific_groups']) if pattern['specific_groups'] else 'None detected'}\n\n")
                f.write(f"**Potential Reason**: {pattern['potential_reason']}\n\n")

def find_dataset_files(results_dir="results"):
    """Find all consistent and mixed JSONL files in the results directory."""
    consistent_files = glob.glob(os.path.join(results_dir, "*_consistent.jsonl"))
    mixed_files = glob.glob(os.path.join(results_dir, "*_mixed_cant_determine.jsonl"))
    
    # Create pairs of files (consistent + mixed with same base name)
    dataset_pairs = []
    
    for consistent_file in consistent_files:
        # Extract base name (without _consistent.jsonl)
        base_name = consistent_file.replace("_consistent.jsonl", "")
        base_name = os.path.basename(base_name)
        
        # Look for matching mixed file
        matching_mixed = None
        for mixed_file in mixed_files:
            if base_name in mixed_file:
                matching_mixed = mixed_file
                break
        
        dataset_pairs.append({
            'base_name': base_name,
            'consistent_file': consistent_file,
            'mixed_file': matching_mixed
        })
    
    return dataset_pairs

def main():
    """Main analysis function."""
    
    # Find all datasets in results directory
    dataset_pairs = find_dataset_files()
    
    if not dataset_pairs:
        print("No dataset files found in results directory.")
        print("Looking for files matching pattern: *_consistent.jsonl and *_mixed_cant_determine.jsonl")
        return
    
    print(f"Found {len(dataset_pairs)} dataset(s) to analyze:")
    for i, dataset in enumerate(dataset_pairs, 1):
        print(f"{i}. {dataset['base_name']}")
        print(f"   Consistent: {dataset['consistent_file']}")
        if dataset['mixed_file']:
            print(f"   Mixed: {dataset['mixed_file']}")
        else:
            print(f"   Mixed: Not found")
    
    # Analyze each dataset
    for dataset in dataset_pairs:
        print(f"\nAnalyzing dataset: {dataset['base_name']}")
        
        try:
            # Load the data
            consistent_records = load_jsonl(dataset['consistent_file'])
            print(f"Loaded {len(consistent_records)} consistent pairs from {dataset['consistent_file']}")
            
            mixed_records = []
            if dataset['mixed_file'] and os.path.exists(dataset['mixed_file']):
                mixed_records = load_jsonl(dataset['mixed_file'])
                print(f"Loaded {len(mixed_records)} mixed pairs from {dataset['mixed_file']}")
            else:
                print("No mixed pairs file found or file does not exist")
            
            # Perform analysis
            analysis_results = analyze_reasoning_bias(
                consistent_records, 
                mixed_records, 
                dataset['consistent_file'], 
                dataset['mixed_file'] or "Not found"
            )
            
            # Generate unique output filename
            output_file = get_unique_output_filename(dataset['base_name'])
            
            # Generate report
            generate_bias_report(analysis_results, output_file)
            
            print(f"Analysis complete! Report saved to: {output_file}")
            
            # Print summary to console
            summary = analysis_results["summary"]
            print(f"Summary for {dataset['base_name']}:")
            print(f"  Total pairs analyzed: {summary['total_pairs']}")
            print(f"  Bias detection rate: {summary['bias_rate']*100:.1f}%")
            print(f"  Mixed 'can't determine' pairs: {summary['mixed_cant_determine_pairs']}")
            
        except FileNotFoundError as e:
            print(f"Error: Could not find file {e.filename}")
        except Exception as e:
            print(f"Error during analysis of {dataset['base_name']}: {e}")

if __name__ == "__main__":
    main()