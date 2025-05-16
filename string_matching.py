import difflib
from typing import List, Tuple

__all__ = ['calculate_string_similarity_metrics']


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


def calculate_string_similarity_metrics(lines: List[str], text: str):
    """
    Calculate similarity metrics between a text and multiple lines.
    
    Args:
        lines: List of strings to compare against
        text: The source text to compare from
        
    Returns:
        List of dictionaries containing similarity metrics for each line:
            - line_index: Index of the line in the input list
            - dissimilarity_score: Combined score of differences (lower is better)
            - line_length: Total length of the line
            - unmatched_char_count: Number of characters that don't match exactly
            - matched_char_count: Number of characters that match exactly
            - gap_char_count: Number of characters in gaps between matches
            - inserted_char_count: Number of extra characters
            - replaced_char_count: Number of replaced characters
    """
    lower_text = text.lower()
    results = []

    for idx, line in enumerate(lines):
        lower_line = line.lower()
        matching_segments = []

        for operation, sub1, sub2, i, j in compare_strings(lower_text, lower_line):
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
        
        line_length = len(line)
        unmatched_char_count = (line_length - matched_char_count)
        
        dissimilarity_score = (unmatched_char_count + 
                             inserted_char_count + 
                             replaced_char_count + 
                             gap_char_count)
        
        # Append metrics for this line
        results.append({
            'line_index': idx,
            'dissimilarity_score': dissimilarity_score,
            'line_length': line_length,
            'unmatched_char_count': unmatched_char_count,
            'matched_char_count': matched_char_count,
            'gap_char_count': gap_char_count,
            'inserted_char_count': inserted_char_count,
            'replaced_char_count': replaced_char_count
        })
              
    return results


if __name__ == '__main__':
    # Example usage
    sample_text1 = 'A/LM/AQM) BOX 9115'
    sample_text2 = 'A/LM/AQM) PPO BOX 9135'

    for operation, src_text, tgt_text, src_pos, tgt_pos in compare_strings(sample_text1, sample_text2):
        print(f"{operation.upper():<7} at source[{src_pos}:{src_pos+len(src_text)}], "
              f"target[{tgt_pos}:{tgt_pos+len(tgt_text)}]: '{src_text}' → '{tgt_text}'")

    sample_lines = [sample_text1, sample_text2]
    sample_full_text = 'OFFICE OF ACQUISITION MANAGEMENT (A/LM/AQM) PO BOX 9115 ROSSLYN STATION US DEPARTMENT OF STATE ARLINGTON, VA 22219'
    results = calculate_string_similarity_metrics(sample_lines, sample_full_text)
                               
    from pprint import pprint
    pprint(results)