# Algorithm Collection

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.txt)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen)](https://github.com/vaibhavhiwase/algorithm#readme)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/vaibhavhiwase/algorithm/actions)

A curated collection of Python algorithms focusing on efficiency and practical applications.

## Table of Contents
- [Available Algorithms](#available-algorithms)
  - [String Algorithms](#string-algorithms)
  - [Financial Algorithms](#financial-algorithms)
- [Quick Start](#quick-start)
- [Algorithm Details](#algorithm-details)
  - [String Similarity Metrics](#string-similarity-metrics)
  
  - [Home Loan EMI Calculator](#home-loan-emi-calculator)
- [Contributing](#contributing)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

## Available Algorithms

### String Algorithms
- [String Similarity Metrics](src/string_algorithms/string_subsequence_matching.py) - Calculate similarity metrics between strings using sequence matching


### Financial Algorithms
- [Home Loan EMI Calculator](src/financial_algorithms/loan_emi_calculator.py) - Calculate and simulate home loan repayments with flexible EMI, lump sum payments, and target month calculations

## Quick Start

```bash
git clone https://github.com/vaibhavhiwase/algorithm.git
cd algorithm
```

## Running Demos

To run the web-based demos for the Loan EMI Simulator and Sub Sequence String Matching:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Flask Application:**
    ```bash
    FLASK_APP=src/main_app/app.py flask run --port=5000
    ```

3.  **Access Demos:**
    Once the server is running, you can access the demos in your web browser:
    *   **Main Demo Page:** `http://127.0.0.1:5000/`
    *   **Loan EMI Simulator:** `http://127.0.0.1:5000/financial_algorithms/loan_emi_calculator`
    *   **Sub Sequence String Matching:** `http://127.0.0.1:5000/string_algorithms/string_subsequence_matching`

    *(Note: The server runs in debug mode, so changes to the code will automatically restart the server.)*

## Algorithm Details

### String Similarity Metrics

#### Overview
A robust string comparison algorithm that provides detailed similarity metrics between two strings, supporting case-sensitive matching, Unicode characters, and comprehensive difference tracking.

#### Basic Usage
```python
from string_algorithms import calculate_substring_similarity

text = "Hello World! This is a test."
subtext = "Hello world"
results = calculate_substring_similarity(text, subtext)
```

#### Features
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
results = calculate_substring_similarity(text, subtext)
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
results = calculate_substring_similarity(text, subtext)
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
results = calculate_substring_similarity(text, subtext)
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

The Sub Sequence String Matching algorithm uses Python's `difflib.SequenceMatcher` with careful configuration for precise matching:

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
python -m unittest src/string_algorithms/tests/test_string_algorithms.py -v
```

Test coverage includes:
- Basic functionality (exact/partial matches)
- Case sensitivity (upper/lowercase differences)
- Edge cases (empty strings, long texts)
- Special cases (Unicode, whitespace, numbers)
- Comprehensive index tracking
- Junk parameter behavior



### Home Loan EMI Calculator

#### Overview
A comprehensive home loan calculator that simulates loan repayments with support for flexible EMI calculations, lump sum payments, and target month calculations.

#### Basic Usage
```python
from financial_algorithms import simulate_home_loan

# Example 1: Fixed EMI
simulate_home_loan(
    loan_amount=1712369,
    annual_interest_rate=9.2,
    emi=61200
)

# Example 2: Fixed EMI with Lump Sum Payments
simulate_home_loan(
    loan_amount=1712369,
    annual_interest_rate=9.2,
    emi=61200,
    lump_sums={6: 100000, 12: 50000}
)

# Example 3: Target Months (calculate EMI)
simulate_home_loan(
    loan_amount=1712369,
    annual_interest_rate=9.2,
    target_months=24
)
```

#### Features
- Calculate EMI for given principal, interest rate, and loan term
- Simulate complete loan repayment schedule
- Support for lump sum payments at specific months
- Option to calculate EMI based on target repayment period
- Detailed monthly breakdown of payments
- Summary statistics including total interest paid and total amount paid

#### Testing
The calculator includes comprehensive test cases covering:
- Basic EMI calculations
- Zero interest rate scenarios
- Large loan amounts
- Fixed EMI payments
- Lump sum payments
- Target month calculations
- Currency formatting
- Edge cases (small amounts, high rates)

Run tests using:
```bash
python -m unittest src/financial_algorithms/tests/test_loan_emi_calculator.py -v
```

#### Dependencies
- Python 3.x
- pandas

#### Notes
- EMI is calculated using the standard formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
- All amounts are formatted in Indian Rupees (₹)
- The schedule shows detailed breakdown of each payment including:
  - EMI
  - Lump sum payments
  - Interest paid
  - Principal paid
  - Remaining balance

## Contributing
1. Fork and clone the repository
2. Create your feature branch
3. Add tests and documentation
4. Submit a Pull Request

## Dependencies
- Python 3.6+
- Standard library (difflib, typing, unittest)
- pandas (for homeloan calculator)

## License
[MIT License](LICENSE.txt)

## Author
Vaibhav Hiwase 