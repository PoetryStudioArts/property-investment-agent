# app.py

import streamlit as st

# --- Mock Data Dictionaries ---
mock_str_income = {
    "10001": 3200,
    "90210": 5200,
    "30303": 2800,
    "78701": 3600,
    "60614": 3100
}

mock_tax_rate = {
    "10001": 1.2,
    "90210": 0.8,
    "30303": 1.1,
    "78701": 1.5,
    "60614": 1.3
}

mock_insurance = {
    "10001": 1500,
    "90210": 1200,
    "30303": 1300,
    "78701": 1600,
    "60614": 1400
}

# --- User Inputs ---
st.title("🏡 Property Investment Analyzer")
st.write("Estimate rental income, taxes, and insurance for a given ZIP code.")

zip_code = st.text_input("Enter ZIP Code (e.g., 90210)")
price = st.number_input("Enter Property Purchase Price ($)", value=300000)
down_payment = st.number_input("Enter Down Payment Amount ($)", value=60000)

# --- Calculations ---
if zip_code and zip_code in mock_str_income:
    monthly_income = mock_str_income[zip_code]
    annual_income = monthly_income * 12

    tax_rate = mock_tax_rate[zip_code] / 100
    annual_tax = price * tax_rate

    insurance_cost = mock_insurance[zip_code]

    loan_amount = price - down_payment
    mortgage_payment = (loan_amount * 0.07) / 12  # 7% fixed interest assumption

    monthly_expenses = mortgage_payment + (annual_tax + insurance_cost) / 12
    monthly_net = monthly_income - monthly_expenses
    annual_net = monthly_net * 12

    cash_on_cash_roi = (annual_net / down_payment) * 100

    # --- Output ---
    st.subheader("📈 Investment Summary")
    st.write(f"**Estimated Monthly STR Income:** ${monthly_income:,.0f}")
    st.write(f"**Estimated Annual Property Taxes:** ${annual_tax:,.0f}")
    st.write(f"**Estimated Annual Insurance Cost:** ${insurance_cost:,.0f}")
    st.write(f"**Estimated Monthly Mortgage:** ${mortgage_payment:,.0f}")
    st.write(f"**Monthly Net Income:** ${monthly_net:,.0f}")
    st.write(f"**Annual Cash-on-Cash ROI:** {cash_on_cash_roi:.2f}%")
else:
    if zip_code:
        st.error("Sorry! No mock data for that ZIP code yet.")
