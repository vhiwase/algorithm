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


if __name__ == '__main__':
    # Example usage
    sample_text = 'OFFICE OF ACQUISITION MANAGEMENT (A/LM/AQM) PO BOX 9115 ROSSLYN STATION US DEPARTMENT OF STATE ARLINGTON, VA 22219'
    sample_subtext = 'A/LM/AQM) BOX 9115'
    
    # Show detailed comparison
    print("Detailed comparison:")
    for operation, src_text, tgt_text, src_pos, tgt_pos in compare_strings(sample_text, sample_subtext):
        print(f"{operation.upper():<7} at source[{src_pos}:{src_pos+len(src_text)}], "
              f"target[{tgt_pos}:{tgt_pos+len(tgt_text)}]: '{src_text}' → '{tgt_text}'")
    
    # Calculate similarity metrics
    print("\nSimilarity metrics:")
    results = calculate_string_similarity(sample_text, sample_subtext)
    from pprint import pprint
    pprint(results)