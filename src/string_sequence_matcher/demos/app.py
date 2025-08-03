from flask import Blueprint, render_template, request, jsonify
from string_sequence_matcher.core import calculate_string_similarity

import os

string_sequence_matching_bp = Blueprint('string_sequence_matching', __name__,
                             static_folder=os.path.join(os.path.dirname(__file__), 'static'),
                             template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@string_sequence_matching_bp.route('/')
def index():
    return render_template('string_sequence_matcher_index.html')

@string_sequence_matching_bp.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    text = data['text']
    subtext = data['subtext']
    results = calculate_string_similarity(text, subtext)
    return jsonify({'matches': results})
