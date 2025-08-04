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

from financial_algorithms.demos.app import financial_algorithms_bp
from string_algorithms.demos.app import string_sequence_matching_bp
from utils.logger_config import configure_logger, logger

configure_logger()

app = Flask(__name__, static_folder='static')

app.register_blueprint(financial_algorithms_bp, url_prefix='/financial_algorithms')
app.register_blueprint(string_sequence_matching_bp, url_prefix='/string_sequence_matching')


@app.route('/')
def index():
    return render_template('index.html')


