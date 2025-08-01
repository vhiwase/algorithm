from flask import Blueprint, render_template, request, jsonify
from string_matching import calculate_string_similarity

import os

string_matching_bp = Blueprint('string_matching', __name__,
                             template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@string_matching_bp.route('/')
def index():
    return render_template('string_matching_index.html')

@string_matching_bp.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    text = data['text']
    subtext = data['subtext']
    results = calculate_string_similarity(text, subtext)
    return jsonify({'matches': results})
