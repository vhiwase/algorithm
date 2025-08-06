from flask import Blueprint, render_template, request, jsonify
from string_algorithms import calculate_substring_similarity
import unicodedata

import os
from utils.logger_config import configure_logger

logger = configure_logger()

string_subsequence_matching_bp = Blueprint('string_subsequence_matching', __name__,
                             static_folder=os.path.join(os.path.dirname(__file__), 'static'),
                             template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@string_subsequence_matching_bp.route('/')
def index():
    logger.info("Accessing string_subsequence_matching index page.")
    return render_template('string_subsequence_matching_index.html')

@string_subsequence_matching_bp.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    text = data['text']
    subtext = data['subtext']
    case_sensitive = data.get('case_sensitive', True)
    ignore_whitespace = data.get('ignore_whitespace', False)
    normalize = data.get('normalize', False)

    logger.info(
        f"Comparing text: '{text}' with subtext: '{subtext}' "
        f"(case_sensitive={case_sensitive}, ignore_whitespace={ignore_whitespace}, normalize={normalize})"
    )

    results = calculate_substring_similarity(
        text,
        subtext,
        case_sensitive=case_sensitive,
        ignore_whitespace=ignore_whitespace,
        normalize=normalize,
        # debug=True
    )
    # logger.info(f"{results=}")
    logger.info(f"String comparison successful.")
    return jsonify({'matches': results})

@string_subsequence_matching_bp.route('/debug_unicode')
def debug_unicode():
    composed = "Café"            # Uses U+00E9
    decomposed = "Cafe\u0301"    # Uses 'e' + U+0301 (combining acute)

    results = {
        'original': {
            'composed': composed,
            'decomposed': decomposed,
            'are_equal': composed == decomposed
        },
        'normalizations': {}
    }

    for form in ['NFC', 'NFD', 'NFKC', 'NFKD']:
        normalized_composed = unicodedata.normalize(form, composed)
        normalized_decomposed = unicodedata.normalize(form, decomposed)

        results['normalizations'][form] = {
            'normalized_composed': normalized_composed,
            'normalized_decomposed': normalized_decomposed,
            'are_equal': normalized_composed == normalized_decomposed
        }

    return jsonify(results)