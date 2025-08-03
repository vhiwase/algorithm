from flask import Blueprint, render_template, request, jsonify
from string_algorithms import calculate_string_similarity

import os
from utils.logger_config import logger

string_sequence_matching_bp = Blueprint('string_sequence_matching', __name__,
                             static_folder=os.path.join(os.path.dirname(__file__), 'static'),
                             template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@string_sequence_matching_bp.route('/')
def index():
    logger.info("Accessing string_sequence_matching index page.")
    return render_template('string_sequence_matching_index.html')

@string_sequence_matching_bp.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    text = data['text']
    subtext = data['subtext']
    logger.info(f"Comparing text: '{text}' with subtext: '{subtext}'")
    results = calculate_string_similarity(text, subtext)
    logger.info("String comparison successful.")
    return jsonify({'matches': results})
