from flask import Blueprint, render_template, request
from string_matching import calculate_string_similarity

import os

string_matching_bp = Blueprint('string_matching', __name__,
                             template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@string_matching_bp.route('/')
def index():
    return render_template('string_matching_index.html')

@string_matching_bp.route('/compare', methods=['POST'])
def compare():
    text = request.form['text']
    subtext = request.form['subtext']
    results = calculate_string_similarity(text, subtext)
    return render_template('string_matching_results.html', text=text, subtext=subtext, results=results)
