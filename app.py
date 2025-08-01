from flask import Flask, render_template
from demos.loan_emi_simulator.app import loan_emi_simulator_bp
from demos.string_matching.app import string_matching_bp

app = Flask(__name__, static_folder='static')

app.register_blueprint(loan_emi_simulator_bp, url_prefix='/loan_emi_simulator')
app.register_blueprint(string_matching_bp, url_prefix='/string_matching')

 

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)