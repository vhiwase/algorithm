__all__ = ['calculate_emi', 'simulate_loan', 'INR']

import pandas as pd
try:
    # Project‑specific logger configuration; fallback to a simple console logger.
    from utils.logger_config import configure_logger
except ModuleNotFoundError:
    # If the utils package cannot be found, add the project root to ``sys.path``.
    import sys
    from pathlib import Path

    def _add_project_root_to_sys_path() -> None:
        project_root = Path(__file__).resolve().parents[1]
        if str(project_root) not in sys.path:
            sys.path.append(str(project_root))

    _add_project_root_to_sys_path()
    from utils.logger_config import configure_logger

logger = configure_logger()

# Utility to format currency
INR = lambda x: f"₹{int(round(x)):,}"

def calculate_emi(P, r, n):
    """
    Calculate EMI for given principal, monthly rate, and months.
    """
    if r == 0:
        return P / n
    return P * r * (1 + r) ** n / ((1 + r) ** n - 1)

def simulate_loan(
    loan_amount,
    annual_interest_rate,
    emi=None,
    lump_sums=None,
    target_months=None
):
    """
    Simulate a home loan repayment with flexible EMI, optional lump sum(s), or target months.
    - emi: fixed monthly payment (if None and target_months is set, will be calculated)
    - lump_sums: dict {month: amount} or list of (month, amount) for extra payments
    - target_months: if set, calculate EMI to finish in this many months
    """
    monthly_interest_rate = annual_interest_rate / 12 / 100
    schedule = []
    balance = loan_amount
    month = 0
    total_interest_paid = 0
    lump_sums = lump_sums or {}
    if isinstance(lump_sums, list):
        lump_sums = dict(lump_sums)

    # Calculate EMI if target_months is given
    if emi is None and target_months is not None:
        emi = calculate_emi(balance, monthly_interest_rate, target_months)
        logger.info(f"To finish in {target_months} months, you need to pay EMI: {INR(emi)}")
    elif emi is None:
        raise ValueError("You must specify either emi or target_months.")

    MAX_MONTHS = 1200  # Safeguard to prevent infinite loops (100 years)

    while balance > 0 and month < MAX_MONTHS:
        month += 1
        interest = balance * monthly_interest_rate
        # Check if EMI is too low *after* interest is calculated for the current month
        if emi < interest:
            raise ValueError("EMI is too low to cover even the interest. Loan will never be repaid.")

        principal_payment = emi - interest
        lump_sum = lump_sums.get(month, 0)
        total_payment = principal_payment + lump_sum
        if total_payment > balance:
            principal_payment = balance - lump_sum
            if principal_payment < 0:
                principal_payment = 0
                lump_sum = balance
            emi = interest + principal_payment
        balance -= (principal_payment + lump_sum)
        total_interest_paid += interest
        schedule.append({
            'Month': month,
            'EMI': INR(emi),
            'Lump Sum': INR(lump_sum) if lump_sum else '',
            'Interest Paid': INR(interest),
            'Principal Paid': INR(principal_payment + lump_sum),
            'Remaining Balance': INR(balance if balance > 0 else 0)
        })
        if balance <= 0:
            break

    df = pd.DataFrame(schedule)
    logger.info("\nRepayment Schedule (first 24 months or full schedule if shorter):")
    logger.info(df.head(24).to_string(index=False))
    if len(df) > 24:
        logger.info(f"... (showing first 24 of {len(df)} months)")
    logger.info(f"\nSUMMARY:")
    logger.info(f"  Total Months: {month}")
    logger.info(f"  Total Interest Paid: {INR(total_interest_paid)}")
    logger.info(f"  Total Paid: {INR(total_interest_paid + loan_amount)}")
    if df.empty:
        raise ValueError("Loan amount must be greater than zero and result in a valid schedule.")
    logger.info(f"  Last EMI: {df.iloc[-1]['EMI']}")
    if any(df['Lump Sum']):
        logger.info(f"  Lump Sums Paid: {', '.join([f'M{m}: {l}' for m, l in zip(df['Month'], df['Lump Sum']) if l])}")
    logger.info("\n")
    return df

# --- EXAMPLES TO EXPERIMENT WITH ---
if __name__ == "__main__":
    loan_amount = 1712369
    annual_interest_rate = 9.2

    logger.info("\n--- Example 1: Fixed EMI ---")
    simulate_loan(loan_amount, annual_interest_rate, emi=61200)

    logger.info("\n--- Example 2: Fixed EMI + Lump Sums in Month 6 and 12 ---")
    simulate_loan(
        loan_amount, annual_interest_rate, emi=61200, lump_sums={6: 100000, 12: 50000}
    )

    logger.info("\n--- Example 3: Pay off in months (calculate EMI) ---")
    simulate_loan(
        loan_amount, annual_interest_rate, target_months=24
    )
