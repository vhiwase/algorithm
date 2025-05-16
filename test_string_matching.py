import unittest
from string_matching import calculate_string_similarity


class TestStringSimilarity(unittest.TestCase):
    """Test cases for string similarity metrics calculation."""

    def assert_metrics_structure(self, results):
        """Helper method to verify the structure of metrics dictionary."""
        expected_keys = {
            'dissimilarity_score',
            'text_length',
            'subtext_length',
            'unmatched_char_count',
            'matched_char_count',
            'gap_char_count',
            'inserted_char_count',
            'replaced_char_count'
        }
        self.assertEqual(set(results.keys()), expected_keys)
        for value in results.values():
            self.assertIsInstance(value, (int, float))

    def test_exact_substring_match(self):
        """Test case for exact substring matching."""
        text = "Hello World! This is a test string."
        subtext = "This is"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['matched_char_count'], len(subtext))
        self.assertEqual(results['unmatched_char_count'], 0)
        self.assertEqual(results['replaced_char_count'], 0)

    def test_case_insensitive_match(self):
        """Test case for case-insensitive matching."""
        text = "HELLO WORLD! This is a TEST string."
        subtext = "hello world"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['matched_char_count'], len(subtext))
        self.assertEqual(results['unmatched_char_count'], 0)

    def test_partial_match_with_replacements(self):
        """Test case for partial matching with character replacements."""
        text = "The quick brown fox jumps over the lazy dog"
        subtext = "The quack brown fox jumped over the dog"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['replaced_char_count'], 0)
        self.assertLess(results['matched_char_count'], len(subtext))

    def test_special_characters_match(self):
        """Test case for matching with special characters."""
        text = "Email: user@example.com, Phone: (123) 456-7890"
        subtext = "user@example.com"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['matched_char_count'], len(subtext))
        self.assertEqual(results['unmatched_char_count'], 0)

    def test_numbers_and_punctuation(self):
        """Test case for matching with numbers and punctuation."""
        text = "Invoice #12345 - Total: $199.99 (Due: 2024-01-31)"
        subtext = "Invoice #12345"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['matched_char_count'], len(subtext))
        self.assertEqual(results['unmatched_char_count'], 0)

    def test_multiline_text(self):
        """Test case for matching with multi-line text."""
        text = """First line of text
        Second line with different content
        Third line here"""
        subtext = "Second line with similar content"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['matched_char_count'], 0)
        self.assertGreater(results['unmatched_char_count'], 0)

    def test_unicode_characters(self):
        """Test case for matching with Unicode characters."""
        text = "Hello 👋 World! 🌍 Have a nice day! ⭐"
        subtext = "World! 🌍"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['matched_char_count'], len(subtext))
        self.assertEqual(results['unmatched_char_count'], 0)

    def test_whitespace_handling(self):
        """Test case for handling whitespace."""
        text = "This    has    multiple    spaces    between    words"
        subtext = "has multiple spaces"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['matched_char_count'], 0)
        self.assertGreater(results['gap_char_count'], 0)

    def test_no_match(self):
        """Test case for completely different strings."""
        text = "Completely different text"
        subtext = "No matching content here"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['dissimilarity_score'], 0)
        self.assertLess(results['matched_char_count'], len(subtext))

    def test_address_matching(self):
        """Test case for address matching."""
        text = "OFFICE OF ACQUISITION MANAGEMENT (A/LM/AQM) PO BOX 9115 ROSSLYN STATION US DEPARTMENT OF STATE ARLINGTON, VA 22219"
        subtext = "A/LM/AQM) BOX 9115"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['matched_char_count'], 0)
        self.assertGreater(results['gap_char_count'], 0)

    def test_empty_strings(self):
        """Test case for empty strings."""
        text = ""
        subtext = ""
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['text_length'], 0)
        self.assertEqual(results['subtext_length'], 0)
        self.assertEqual(results['matched_char_count'], 0)

    def test_single_character(self):
        """Test case for single character strings."""
        text = "a"
        subtext = "a"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['text_length'], 1)
        self.assertEqual(results['subtext_length'], 1)
        self.assertEqual(results['matched_char_count'], 1)

    def test_long_text(self):
        """Test case for long text strings."""
        text = "a" * 1000
        subtext = "a" * 100
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['text_length'], 1000)
        self.assertEqual(results['subtext_length'], 100)
        self.assertEqual(results['matched_char_count'], 100)


if __name__ == '__main__':
    unittest.main(verbosity=2) 