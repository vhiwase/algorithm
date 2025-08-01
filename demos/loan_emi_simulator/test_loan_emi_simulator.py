import unittest
from ...loan_emi_simulator import calculate_emi, simulate_home_loan, INR

class TestHomeLoan(unittest.TestCase):
    def test_calculate_emi(self):
        # Test case 1: Basic EMI calculation
        principal = 1000000
        monthly_rate = 0.01  # 1% monthly
        months = 12
        emi = calculate_emi(principal, monthly_rate, months)
        self.assertAlmostEqual(emi, 88848.79, places=2)

        # Test case 2: Zero interest rate
        emi_zero_interest = calculate_emi(principal, 0, months)
        self.assertAlmostEqual(emi_zero_interest, principal/months, places=2)

        # Test case 3: Large loan amount
        large_principal = 5000000
        emi_large = calculate_emi(large_principal, monthly_rate, months)
        self.assertAlmostEqual(emi_large, 444243.94, places=2)

    def test_simulate_home_loan_fixed_emi(self):
        # Test case 1: Fixed EMI without lump sum
        loan_amount = 1000000
        annual_rate = 12  # 12% annual
        emi = 100000
        df, summary = simulate_home_loan(loan_amount, annual_rate, emi=emi)
        
        # Check if DataFrame is returned
        self.assertIsNotNone(df)
        self.assertIsNotNone(summary)
        # Check if first EMI matches
        self.assertEqual(df.iloc[0]['EMI'], INR(emi))
        # Check if last balance is zero or negative
        self.assertLessEqual(float(df.iloc[-1]['Remaining Balance'].replace('₹', '').replace(',', '')), 0)

    def test_simulate_home_loan_with_lump_sum(self):
        # Test case: Fixed EMI with lump sum payments
        loan_amount = 1000000
        annual_rate = 12
        emi = 100000
        lump_sums = {6: 200000}
        df = simulate_home_loan(loan_amount, annual_rate, emi=emi, lump_sums=lump_sums)
        
        # Check if lump sum is applied correctly
        self.assertEqual(df.iloc[5]['Lump Sum'], INR(200000))  # Month 6
        # Verify loan is paid off
        self.assertLessEqual(float(df.iloc[-1]['Remaining Balance'].replace('₹', '').replace(',', '')), 0)

    def test_simulate_home_loan_target_months(self):
        # Test case: Calculate EMI for target months
        loan_amount = 1000000
        annual_rate = 12
        target_months = 12
        df = simulate_home_loan(loan_amount, annual_rate, target_months=target_months)
        
        # Check if loan is paid off
        self.assertLessEqual(float(df.iloc[-1]['Remaining Balance'].replace('₹', '').replace(',', '')), 0)
        # Check if total months is close to target (allowing for rounding)
        self.assertLessEqual(len(df), target_months + 1)

    def test_inr_formatting(self):
        # Test INR formatting
        self.assertEqual(INR(1000), "₹1,000")
        self.assertEqual(INR(1000000), "₹1,000,000")
        self.assertEqual(INR(0), "₹0")
        self.assertEqual(INR(1000.5), "₹1,000")

    def test_edge_cases(self):
        # Test case: Very small loan amount
        df_small = simulate_home_loan(1000, 12, emi=100)
        self.assertLessEqual(len(df_small), 12)

        # Test case: Very high interest rate
        df_high_rate = simulate_home_loan(1000000, 24, emi=100000)
        self.assertIsNotNone(df_high_rate)

        # Test case: Zero loan amount
        with self.assertRaises(ValueError):
            simulate_home_loan(0, 12, emi=1000)

if __name__ == '__main__':
    unittest.main() 