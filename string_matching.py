import difflib
from typing import List, Tuple, Dict

__all__ = ['calculate_string_similarity']


def compare_strings(source_text: str, target_text: str) -> List[Tuple[str, str, str, int, int]]:
    """
    Compare two strings and return their differences using SequenceMatcher.
    
    Args:
        source_text: The source string to compare from
        target_text: The target string to compare against
        
    Returns:
        List of tuples containing (operation_type, source_substring, target_substring, source_start, target_start)
        where operation_type can be 'equal', 'replace', 'delete', or 'insert'
    """
    sequence_matcher = difflib.SequenceMatcher(None, source_text, target_text)
    differences = []
    for operation, src_start, src_end, tgt_start, tgt_end in sequence_matcher.get_opcodes():
        differences.append((operation, source_text[src_start:src_end], 
                          target_text[tgt_start:tgt_end], src_start, tgt_start))
    return differences


def calculate_string_similarity(text: str, subtext: str) -> Dict:
    """
    Calculate similarity metrics between a text and a subtext.
    
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
    """
    lower_text = text.lower()
    lower_subtext = subtext.lower()
    matching_segments = []

    for operation, sub1, sub2, i, j in compare_strings(lower_text, lower_subtext):
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
    
    dissimilarity_score = (unmatched_char_count + 
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
        'replaced_char_count': replaced_char_count
    }


def print_comparison_details(text: str, subtext: str, results: Dict):
    """Helper function to print detailed comparison results."""
    print(f"\nComparing:")
    print(f"Text   : '{text}'")
    print(f"Subtext: '{subtext}'")
    print("\nDetailed comparison:")
    for operation, src_text, tgt_text, src_pos, tgt_pos in compare_strings(text, subtext):
        print(f"{operation.upper():<7} at source[{src_pos}:{src_pos+len(src_text)}], "
              f"target[{tgt_pos}:{tgt_pos+len(tgt_text)}]: '{src_text}' → '{tgt_text}'")
    print("\nMetrics:")
    for key, value in results.items():
        print(f"{key:<20}: {value}")

def run_examples():
    """Run various examples demonstrating different string matching scenarios."""
    
    print("=" * 80)
    print("1. Exact Substring Match")
    print("=" * 80)
    text = "Hello World! This is a test string."
    subtext = "This is"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("2. Case Insensitive Match")
    print("=" * 80)
    text = "HELLO WORLD! This is a TEST string."
    subtext = "hello world"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("3. Partial Match with Replacements")
    print("=" * 80)
    text = "The quick brown fox jumps over the lazy dog"
    subtext = "The quack brown fox jumped over the dog"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("4. Match with Special Characters")
    print("=" * 80)
    text = "Email: user@example.com, Phone: (123) 456-7890"
    subtext = "user@example.com"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("5. Match with Numbers and Punctuation")
    print("=" * 80)
    text = "Invoice #12345 - Total: $199.99 (Due: 2024-01-31)"
    subtext = "Invoice #12345"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("6. Multi-line Text Match")
    print("=" * 80)
    text = """First line of text
    Second line with different content
    Third line here"""
    subtext = "Second line with similar content"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("7. Unicode Characters Match")
    print("=" * 80)
    text = "Hello 👋 World! 🌍 Have a nice day! ⭐"
    subtext = "World! 🌍"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("8. Whitespace Handling")
    print("=" * 80)
    text = "This    has    multiple    spaces    between    words"
    subtext = "has multiple spaces"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("9. No Match Case")
    print("=" * 80)
    text = "Completely different text"
    subtext = "No matching content here"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)

    print("\n" + "=" * 80)
    print("10. Address Matching Example")
    print("=" * 80)
    text = "OFFICE OF ACQUISITION MANAGEMENT (A/LM/AQM) PO BOX 9115 ROSSLYN STATION US DEPARTMENT OF STATE ARLINGTON, VA 22219"
    subtext = "A/LM/AQM) BOX 9115"
    results = calculate_string_similarity(text, subtext)
    print_comparison_details(text, subtext, results)


if __name__ == '__main__':
    run_examples()