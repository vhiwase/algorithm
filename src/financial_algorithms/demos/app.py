from flask import Blueprint, render_template, request, jsonify
from financial_algorithms import simulate_home_loan
import pandas as pd
import os
from utils.logger_config import logger

financial_algorithms_bp = Blueprint('financial_algorithms', __name__,
                                static_folder=os.path.join(os.path.dirname(__file__), 'static'),
                                template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@financial_algorithms_bp.route('/')
def index():
    logger.info("Accessing loan_emi_calculator index page.")
    return render_template('loan_emi_calculator_index.html')

@financial_algorithms_bp.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    loan_amount = float(data['loan_amount'])
    annual_interest_rate = float(data['annual_interest_rate'])
    emi = float(data['emi'])
    
    logger.info(f"Simulating loan with amount: {loan_amount}, interest: {annual_interest_rate}, EMI: {emi}")
    
    try:
        schedule_df = simulate_home_loan(loan_amount, annual_interest_rate, emi)

        # Convert relevant columns to numeric, removing '₹' and ','
        numeric_cols = ['EMI', 'Interest Paid', 'Principal Paid', 'Remaining Balance']
        for col in numeric_cols:
            if col in schedule_df.columns:
                schedule_df[col] = schedule_df[col].astype(str).str.replace('₹', '').str.replace(',', '').replace('', '0').astype(float)

        total_interest_payable = schedule_df['Interest Paid'].sum()
        total_payment = schedule_df['EMI'].sum()
        num_months = len(schedule_df)
        num_years = num_months / 12

        # Prepare schedule data for JSON response, mapping to frontend expectations
        schedule_data = []
        for i, row in schedule_df.iterrows():
            opening_balance = loan_amount if i == 0 else schedule_df.loc[i-1, 'Remaining Balance'] + schedule_df.loc[i-1, 'Principal Paid']
            schedule_data.append({
                'month': int(row['Month']),
                'opening_balance': opening_balance,
                'emi': row['EMI'],
                'interest': row['Interest Paid'],
                'principal': row['Principal Paid'],
                'closing_balance': row['Remaining Balance']
            })
        logger.info("Loan simulation successful.")
        return jsonify({
            'total_interest_payable': total_interest_payable,
            'total_payment': total_payment,
            'num_months': num_months,
            'num_years': num_years,
            'schedule': schedule_data
        })
    except ValueError as e:
        logger.error(f"Loan simulation failed: {e}")
        return jsonify({'error': str(e)}), 400