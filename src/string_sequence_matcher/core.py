import difflib
from typing import List, Tuple, Dict
from utils.logger_config import logger, log_memory_usage_function

__all__ = ['calculate_string_similarity', 'print_comparison_details']


def compare_strings(source_text: str, target_text: str) -> List[Tuple[str, str, str, int, int]]:
    """
    Compare two strings and return their differences using SequenceMatcher.
    Case sensitive comparison.
    
    Args:
        source_text: The source string to compare from
        target_text: The target string to compare against
        
    Returns:
        List of tuples containing (operation_type, source_substring, target_substring, source_start, target_start)
        where operation_type can be 'equal', 'replace', 'delete', or 'insert'
    """
    # Create a new sequence matcher with case-sensitive comparison
    sequence_matcher = difflib.SequenceMatcher(lambda x: False, source_text, target_text)
    differences = []
    for operation, src_start, src_end, tgt_start, tgt_end in sequence_matcher.get_opcodes():
        differences.append((operation, source_text[src_start:src_end], 
                          target_text[tgt_start:tgt_end], src_start, tgt_start))
    return differences

def calculate_string_similarity(text: str, subtext: str) -> Dict:
    """
    Calculate similarity metrics between a text and a subtext.
    Case sensitive comparison.
    
    Args:
        text: The main text to compare against
        subtext: The substring to find similarity metrics for
        
    Returns:
        Dictionary containing similarity metrics:
            - dissimilarity_score: Combined score of differences (lower is better)
            - text_length: Total length of the main text
            - subtext_length: Total length of the subtext
            - unmatched_char_count: Number of characters that don't match exactly
            - matched_char_count: Number of characters that match exactly
            - gap_char_count: Number of characters in gaps between matches
            - inserted_char_count: Number of extra characters
            - replaced_char_count: Number of replaced characters
            - matches: List of matching text segments
            - replacements: List of tuples containing (original_text, replacement_text)
            - gaps: List of gap text segments
    """
    matching_segments = []

    for operation, sub1, sub2, i, j in compare_strings(text, subtext):
        if operation in ['equal', 'replace', 'insert']:
            matching_segments.append((operation, (i, i + len(sub1)), (j, j + len(sub2))))

    # Sort by start index
    matching_segments.sort(key=lambda x: x[1][0])
    
    # Find unmatched segments in text
    unmatched_segments = []
    for i in range(len(matching_segments) - 1):
        end_current = matching_segments[i][1][1]
        start_next = matching_segments[i + 1][1][0]
        if end_current < start_next:
            unmatched_segments.append((end_current, start_next))
    
    # Collect matching segments with actual text
    exact_matches = [text[t_range[0]:t_range[1]] 
                    for op, t_range, _ in matching_segments if op == 'equal']
    
    # Collect replacement segments with actual text pairs
    replacements = [(text[t_range[0]:t_range[1]], subtext[s_range[0]:s_range[1]]) 
                   for op, t_range, s_range in matching_segments if op == 'replace']
    
    # Collect gaps with actual text
    gaps = [text[start:end] for start, end in unmatched_segments]
    
    # Calculate metrics
    gap_lengths = [(gap[1]-gap[0]) for gap in unmatched_segments]
    gap_char_count = sum(gap_lengths)

    exact_match_lengths = [(segment[2][1] - segment[2][0]) 
                          for segment in matching_segments if segment[0]=='equal']
    matched_char_count = sum(exact_match_lengths)

    insertion_lengths = [(segment[2][1] - segment[2][0]) 
                        for segment in matching_segments if segment[0]=='insert']
    inserted_char_count = sum(insertion_lengths)

    replacement_lengths = [(segment[1][1]-segment[1][0]) 
                          for segment in matching_segments if segment[0]=='replace']
    replaced_char_count = sum(replacement_lengths)
    
    text_length = len(text)
    subtext_length = len(subtext)
    unmatched_char_count = (subtext_length - matched_char_count)
    
    dissimilarity_score = (
                          unmatched_char_count + 
                          inserted_char_count + 
                          replaced_char_count + 
                          gap_char_count)
    
    return {
        'dissimilarity_score': dissimilarity_score,
        'text_length': text_length,
        'subtext_length': subtext_length,
        'unmatched_char_count': unmatched_char_count,
        'matched_char_count': matched_char_count,
        'gap_char_count': gap_char_count,
        'inserted_char_count': inserted_char_count,
        'replaced_char_count': replaced_char_count,
        'matches': exact_matches,
        'replacements': replacements,
        'gaps': gaps
    }


def print_comparison_details(text: str, subtext: str, results: Dict):
    """Helper function to print detailed comparison results."""
    logger.info("\nInput Strings:")
    logger.info(f"Text    : '{text}'")
    logger.info(f"Subtext : '{subtext}'")
    
    logger.info("\nMetrics:")
    for key, value in results.items():
        logger.info(f"{key:<20}: {value}")


def run_examples():
    """Run examples demonstrating string matching behavior with different scenarios."""
    
    logger.info("\n" + "=" * 80)
    logger.info("1. Basic Exact Match")
    logger.info("=" * 80)
    text = "Hello World! This is a test string."
    subtext = "This is"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("2. Case Sensitivity Example")
    logger.info("=" * 80)
    text = "HELLO WORLD! This is a TEST string."
    subtext = "hello world"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("3. Partial Match with Special Characters")
    logger.info("=" * 80)
    text = "User ID: #12345 (active) - user@example.com"
    subtext = "#12345 - user@example"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("4. Whitespace Handling")
    logger.info("=" * 80)
    text = "The    quick    brown    fox"
    subtext = "quick brown fox"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("5. Multi-line Text")
    logger.info("=" * 80)
    text = """First line of text
    Second line with important data
    Third line here"""
    subtext = "Second line with data"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    logger.info("\n" + "=" * 80)
    logger.info("6. Unicode and Emoji")
    logger.info("=" * 80)
    text = "Hello 👋 World! 🌍 Have a Nice Day! ⭐"
    subtext = "World! 🌍"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)


if __name__ == '__main__':
    run_examples()
