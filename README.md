# Algorithm Collection

A curated collection of various algorithms implemented in Python, focusing on efficiency, readability, and practical applications.

## Available Algorithms

### String Algorithms
- [String Similarity Metrics](string_matching.py) - Calculate detailed similarity metrics between strings using sequence matching

## Installation

```bash
# Clone the repository
git clone https://github.com/vaibhavhiwase/algorithm.git

# Navigate to the directory
cd algorithm
```

No additional installation is required as all implementations use only Python standard library modules.

## Algorithms Details

### String Similarity Metrics

#### Features
- Compare strings using sequence matching algorithms
- Calculate multiple similarity metrics:
  - Character-level matching scores
  - Gap analysis
  - Insertion detection
  - Replacement identification
- Case-insensitive comparison
- Detailed position tracking of differences
- Efficient substring similarity analysis

#### Usage

```python
from string_matching import calculate_string_similarity

# Example usage
text = 'OFFICE OF ACQUISITION MANAGEMENT (A/LM/AQM) PO BOX 9115 ROSSLYN STATION US DEPARTMENT OF STATE ARLINGTON, VA 22219'
subtext = 'A/LM/AQM) BOX 9115'

# Calculate similarity metrics
results = calculate_string_similarity(text, subtext)

# Print results
from pprint import pprint
pprint(results)
```

#### Output Format

The function returns a dictionary containing the following similarity metrics:

- `dissimilarity_score`: Combined score of differences (lower is better)
- `text_length`: Total length of the main text
- `subtext_length`: Total length of the subtext
- `unmatched_char_count`: Number of characters that don't match exactly
- `matched_char_count`: Number of characters that match exactly
- `gap_char_count`: Number of characters in gaps between matches
- `inserted_char_count`: Number of extra characters
- `replaced_char_count`: Number of replaced characters

#### How It Works

The utility uses Python's `difflib.SequenceMatcher` to perform detailed string comparisons. It:

1. Converts all text to lowercase for case-insensitive matching
2. Identifies exact matches, replacements, and insertions
3. Calculates gaps between matching segments
4. Computes various similarity metrics based on the comparison results

## General Information

### Dependencies
- Python 3.6+
- Standard library modules only:
  - difflib
  - typing

### Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create your feature branch
3. Implement your algorithm
4. Add appropriate documentation and examples
5. Submit a Pull Request

### Future Additions
The following categories of algorithms will be added in the future:
- Sorting Algorithms
- Search Algorithms
- Graph Algorithms
- Dynamic Programming
- Machine Learning Algorithms
- Data Structure Implementations
- Cryptography Algorithms
- Optimization Algorithms

### License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

### Author

Vaibhav Hiwase 