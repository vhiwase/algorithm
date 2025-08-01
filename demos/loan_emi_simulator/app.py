from flask import Blueprint, render_template, request
from loan_emi_simulator import simulate_home_loan
import pandas as pd

import os

loan_emi_simulator_bp = Blueprint('loan_emi_simulator', __name__,
                                template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@loan_emi_simulator_bp.route('/')
def index():
    return render_template('loan_emi_simulator_index.html')

@loan_emi_simulator_bp.route('/simulate', methods=['POST'])
def simulate():
    loan_amount = float(request.form['loan_amount'])
    annual_interest_rate = float(request.form['annual_interest_rate'])
    emi = float(request.form['emi'])
    
    schedule_df = simulate_home_loan(loan_amount, annual_interest_rate, emi)
    
    summary = {
        'Total Months': len(schedule_df),
        'Total Interest Paid': schedule_df['Interest Paid'].apply(lambda x: float(x.replace('₹', '').replace(',', ''))).sum(),
        'Total Paid': float(schedule_df.iloc[-1]['Remaining Balance'].replace('₹', '').replace(',', '')) + float(schedule_df['Principal Paid'].apply(lambda x: float(x.replace('₹', '').replace(',', ''))).sum()),
        'Last EMI': schedule_df.iloc[-1]['EMI']
    }
    
    # Convert dataframe to html
    schedule_html = schedule_df.to_html(classes='table table-striped', index=False)

    return render_template('results.html', summary=summary, schedule_html=schedule_html)