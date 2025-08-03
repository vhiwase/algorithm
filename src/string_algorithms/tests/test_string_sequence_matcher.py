import unittest
from io import StringIO
from contextlib import redirect_stdout
from string_algorithms import calculate_string_similarity, print_comparison_details

__all__ = ['TestStringSimilarity']

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
            'replaced_char_count',
            'matches',
            'replacements',
            'gaps'
        }
        self.assertEqual(set(results.keys()), expected_keys)
        for key, value in results.items():
            if key in ['matches', 'replacements', 'gaps']:
                self.assertIsInstance(value, list)
                for item in value:
                    if key == 'replacements':
                        self.assertIsInstance(item, tuple)
                        self.assertEqual(len(item), 2)
                        self.assertIsInstance(item[0], str)
                        self.assertIsInstance(item[1], str)
                    else:
                        self.assertIsInstance(item, str)
            else:
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
        
        # Verify match content
        self.assertEqual(len(results['matches']), 1)
        self.assertEqual(results['matches'][0], "This is")

    def test_case_sensitive_mismatch(self):
        """Test case for case-sensitive matching."""
        text = "HELLO"
        subtext = "hello"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['dissimilarity_score'], 0)
        self.assertGreater(results['unmatched_char_count'], 0)
        
        # Verify that case differences are treated as replacements
        self.assertGreater(len(results['replacements']), 0)
        for orig, repl in results['replacements']:
            self.assertEqual(len(orig), len(repl))
            # Characters differ at least in case
            self.assertNotEqual(orig, repl)
            self.assertEqual(orig.lower(), repl.lower())

    def test_partial_match_with_replacements(self):
        """Test case for partial matching with character replacements."""
        text = "The quick brown fox jumps over the lazy dog"
        subtext = "The Quick Brown fox jumped over the dog"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['replaced_char_count'], 0)
        self.assertLess(results['matched_char_count'], len(subtext))
        
        # Verify matches and replacements content
        for match in results['matches']:
            self.assertIn(match, text)
            self.assertIn(match, subtext)
        
        for orig, repl in results['replacements']:
            self.assertIn(orig, text)
            self.assertIn(repl, subtext)
            self.assertNotEqual(orig, repl)

    def test_special_characters_match(self):
        """Test case for matching with special characters."""
        text = "Email: User@Example.com, Phone: (123) 456-7890"
        subtext = "User@Example.com"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['matched_char_count'], len(subtext))
        self.assertEqual(results['unmatched_char_count'], 0)
        
        # Verify exact match content
        self.assertEqual(len(results['matches']), 1)
        self.assertEqual(results['matches'][0], "User@Example.com")

    def test_numbers_and_punctuation(self):
        """Test case for matching with numbers and punctuation."""
        text = "Invoice #12345 - Total: $199.99 (Due: 2024-01-31)"
        subtext = "Invoice #12345"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['matched_char_count'], len(subtext))
        self.assertEqual(results['unmatched_char_count'], 0)
        
        # Verify match content
        self.assertEqual(len(results['matches']), 1)
        self.assertEqual(results['matches'][0], "Invoice #12345")

    def test_multiline_text(self):
        """Test case for matching with multi-line text."""
        text = """First Line of text
        Second Line with different content
        Third Line here"""
        subtext = "Second Line with similar content"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['matched_char_count'], 0)
        self.assertGreater(results['unmatched_char_count'], 0)
        
        # Verify matches content
        for match in results['matches']:
            self.assertIn(match, text)
            self.assertIn(match, subtext)

    def test_unicode_characters(self):
        """Test case for matching with Unicode characters."""
        text = "Hello 👋 World! 🌍 Have a Nice Day! ⭐"
        subtext = "World! 🌍"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['matched_char_count'], len(subtext))
        self.assertEqual(results['unmatched_char_count'], 0)
        
        # Verify Unicode character handling in matches
        self.assertEqual(len(results['matches']), 1)
        self.assertEqual(results['matches'][0], "World! 🌍")

    def test_whitespace_handling(self):
        """Test case for handling whitespace."""
        text = "This    Has    Multiple    Spaces    Between    Words"
        subtext = "Has Multiple Spaces"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['matched_char_count'], 0)
        
        # Verify gap content
        for gap in results['gaps']:
            self.assertTrue(all(c.isspace() for c in gap))

    def test_no_match(self):
        """Test case for completely different strings."""
        text = "ABCDEFGHIJKLMNOP"  # Using a string with no common substrings
        subtext = "123456789"      # Completely different characters
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['dissimilarity_score'], 0)
        self.assertEqual(len(results['matches']), 0)
        self.assertGreater(len(results['replacements']), 0)  # Characters will be treated as replacements
        self.assertEqual(len(results['gaps']), 0)
        self.assertEqual(results['matched_char_count'], 0)
        self.assertGreater(results['replaced_char_count'], 0)
        self.assertEqual(results['gap_char_count'], 0)
        self.assertEqual(results['unmatched_char_count'], len(subtext))

    def test_address_matching(self):
        """Test case for address matching."""
        text = "OFFICE OF ACQUISITION MANAGEMENT (A/LM/AQM) PO BOX 9115 ROSSLYN STATION US DEPARTMENT OF STATE ARLINGTON, VA 22219"
        subtext = "A/LM/AQM) PO BOX 9115"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertGreater(results['matched_char_count'], 0)
        
        # Verify matches content
        for match in results['matches']:
            self.assertIn(match, text)
            self.assertIn(match, subtext)

    def test_empty_strings(self):
        """Test case for empty strings."""
        text = ""
        subtext = ""
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['text_length'], 0)
        self.assertEqual(results['subtext_length'], 0)
        self.assertEqual(results['matched_char_count'], 0)
        self.assertEqual(len(results['matches']), 0)
        self.assertEqual(len(results['replacements']), 0)
        self.assertEqual(len(results['gaps']), 0)

    def test_single_character(self):
        """Test case for single character strings."""
        text = "A"
        subtext = "a"
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['text_length'], 1)
        self.assertEqual(results['subtext_length'], 1)
        self.assertEqual(results['matched_char_count'], 0)
        self.assertEqual(results['replaced_char_count'], 1)
        
        # Verify replacement content for single character
        self.assertEqual(len(results['replacements']), 1)
        orig, repl = results['replacements'][0]
        self.assertEqual(len(orig), 1)
        self.assertEqual(len(repl), 1)

    def test_long_text(self):
        """Test case for long text strings."""
        text = "A" * 1000
        subtext = "A" * 100
        results = calculate_string_similarity(text, subtext)
        
        self.assert_metrics_structure(results)
        self.assertEqual(results['text_length'], 1000)
        self.assertEqual(results['subtext_length'], 100)
        self.assertEqual(results['matched_char_count'], 100)
        
        # Verify match content for long text
        self.assertEqual(len(results['matches']), 1)
        self.assertEqual(len(results['matches'][0]), 100)
        self.assertEqual(results['matches'][0], "A" * 100)

    def test_print_comparison_details(self):
        """Test case for print_comparison_details output format."""
        text = "Hello World"
        subtext = "hello"
        results = calculate_string_similarity(text, subtext)
        
        # Capture the printed output
        output = StringIO()
        with redirect_stdout(output):
            print_comparison_details(text, subtext, results)
        
        printed_output = output.getvalue()
        
        # Verify the output format
        self.assertIn("Input Strings:", printed_output)
        self.assertIn(f"Text    : '{text}'", printed_output)
        self.assertIn(f"Subtext : '{subtext}'", printed_output)
        self.assertIn("Metrics:", printed_output)
        
        # Verify all metrics are present in the output
        for key in results.keys():
            self.assertIn(key, printed_output)


if __name__ == '__main__':
    unittest.main(verbosity=2) 