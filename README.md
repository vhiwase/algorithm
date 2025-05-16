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

### Example Output
```python
# Case 1: Exact Match
text = "Hello World!"
subtext = "World"
results = calculate_string_similarity(text, subtext)
{
    'dissimilarity_score': 0,
    'text_length': 12,
    'subtext_length': 5,
    'matched_char_count': 5,
    'unmatched_char_count': 0,
    'gap_char_count': 0,
    'inserted_char_count': 0,
    'replaced_char_count': 0
}

# Case 2: Partial Match with Replacements
text = "The quick brown fox"
subtext = "The quack brown"
results = calculate_string_similarity(text, subtext)
{
    'dissimilarity_score': 2,
    'text_length': 19,
    'subtext_length': 14,
    'matched_char_count': 12,
    'unmatched_char_count': 2,
    'gap_char_count': 0,
    'inserted_char_count': 0,
    'replaced_char_count': 2
}

# Case 3: Unicode Support
text = "Hello 👋 World! 🌍"
subtext = "World! 🌍"
results = calculate_string_similarity(text, subtext)
{
    'dissimilarity_score': 0,
    'text_length': 15,
    'subtext_length': 8,
    'matched_char_count': 8,
    'unmatched_char_count': 0,
    'gap_char_count': 0,
    'inserted_char_count': 0,
    'replaced_char_count': 0
}
```

### Features
- Case-insensitive comparison
- Unicode support (including emojis)
- Detailed similarity metrics
- Handles special characters and whitespace

### Testing
```bash
python -m unittest test_string_matching.py -v
```

Test coverage includes:
- Basic functionality (exact/partial matches)
- Edge cases (empty strings, long texts)
- Special cases (Unicode, whitespace, numbers)

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