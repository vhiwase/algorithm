# Algorithm Collection

A curated collection of Python algorithms focusing on efficiency and practical applications.

## Available Algorithms

### String Algorithms
- [String Similarity Metrics](string_matching.py) - Calculate similarity metrics between strings using sequence matching

## Quick Start

```bash
git clone https://github.com/vaibhavhiwase/algorithm.git
cd algorithm
```

## String Similarity Metrics

### Basic Usage
```python
from string_matching import calculate_string_similarity

text = "Hello World! This is a test."
subtext = "Hello world"
results = calculate_string_similarity(text, subtext)
```

### Features
- Case-sensitive comparison
- Unicode support (including emojis)
- Detailed similarity metrics
- Handles special characters and whitespace
- Precise control over character matching
- Comprehensive index tracking for matches, replacements, and gaps

### Example Output
```python
# Case 1: Exact Match
text = "Hello World!"
subtext = "World"
results = calculate_string_similarity(text, subtext)
print_comparison_details(text, subtext, results)

Input Strings:
Text    : 'Hello World!'
Subtext : 'World'

Metrics:
dissimilarity_score : 0
text_length         : 12
subtext_length      : 5
unmatched_char_count: 0
matched_char_count  : 5
gap_char_count      : 0
inserted_char_count : 0
replaced_char_count : 0
matches             : ['World']
replacements        : []
gaps               : []

# Case 2: Case-Sensitive Mismatch
text = "HELLO"
subtext = "hello"
results = calculate_string_similarity(text, subtext)
print_comparison_details(text, subtext, results)

Input Strings:
Text    : 'HELLO'
Subtext : 'hello'

Metrics:
dissimilarity_score : 5
text_length         : 5
subtext_length      : 5
unmatched_char_count: 0
matched_char_count  : 0
gap_char_count      : 0
inserted_char_count : 0
replaced_char_count : 5
matches             : []
replacements        : [('HELLO', 'hello')]
gaps               : []

# Case 3: Partial Match with Replacements and Gaps
text = "The quick brown fox jumps over the lazy dog"
subtext = "The Quick Brown fox jumped over the dog"
results = calculate_string_similarity(text, subtext)
print_comparison_details(text, subtext, results)

Input Strings:
Text    : 'The quick brown fox jumps over the lazy dog'
Subtext : 'The Quick Brown fox jumped over the dog'

Metrics:
dissimilarity_score : 12
text_length         : 43
subtext_length      : 39
unmatched_char_count: 4
matched_char_count  : 35
gap_char_count      : 5
inserted_char_count : 0
replaced_char_count : 3
matches             : ['The ', 'uick ', 'rown fox jump', ' over the ', 'dog']
replacements        : [('q', 'Q'), ('b', 'B'), ('s', 'ed')]
gaps               : ['lazy ']
```

### Advanced Usage: SequenceMatcher Configuration

The string matching algorithm uses Python's `difflib.SequenceMatcher` with careful configuration for precise matching:

```python
# Default behavior (may use heuristics)
matcher = difflib.SequenceMatcher(None, text1, text2)

# Strict character-by-character comparison (our implementation)
matcher = difflib.SequenceMatcher(lambda x: False, text1, text2)

# Custom junk function (e.g., ignore whitespace)
matcher = difflib.SequenceMatcher(lambda x: x.isspace(), text1, text2)
```

The implementation uses `lambda x: False` as the junk parameter to ensure:
- Strict case-sensitive matching
- No automatic junk character detection
- Consistent and predictable comparison behavior
- Equal treatment of all characters

### Testing
```bash
python -m unittest test_string_matching.py -v
```

Test coverage includes:
- Basic functionality (exact/partial matches)
- Case sensitivity (upper/lowercase differences)
- Edge cases (empty strings, long texts)
- Special cases (Unicode, whitespace, numbers)
- Comprehensive index tracking
- Junk parameter behavior

## Contributing
1. Fork and clone the repository
2. Create your feature branch
3. Add tests and documentation
4. Submit a Pull Request

## Dependencies
- Python 3.6+
- Standard library only (difflib, typing, unittest)

## License
[MIT License](LICENSE.txt)

## Author
Vaibhav Hiwase 