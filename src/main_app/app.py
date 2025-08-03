import sys
from pathlib import Path

def add_project_root_to_sys_path():
    project_root = Path(__file__).resolve().parents[1]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.append(project_root_str)
        from utils.logger_config import configure_logger, logger
        configure_logger()
        logger.info(f"Added {project_root_str} to sys.path")

add_project_root_to_sys_path()

from flask import Flask, render_template

from loan_emi_calculator.demos.app import loan_emi_calculator_bp
from string_sequence_matcher.demos.app import string_sequence_matching_bp
from utils.logger_config import configure_logger, logger

configure_logger()

app = Flask(__name__, static_folder='static')

app.register_blueprint(loan_emi_calculator_bp, url_prefix='/loan_emi_calculator')
app.register_blueprint(string_sequence_matching_bp, url_prefix='/string_sequence_matching')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')