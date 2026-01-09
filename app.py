import streamlit as st
import joblib
import pandas as pd
import numpy as np
from financial_agent import ask_financial_sage

# Load your real ML artifacts
# Ensure these files are in your project folder!
try:
    housing_model = joblib.load("housing_regressor.joblib")
    bank_model = joblib.load("bank_classifier.joblib")
    scaler = joblib.load("bank_scaler.joblib")
except Exception as e:
    st.error(f"Error loading models: {e}")

st.set_page_config(page_title="Financial Assistant Sage", layout="wide")

with st.sidebar:
    st.title("🏠 Property Value Sage")
    
    # Collect all 6 features required by your model
    income = st.number_input("Median Income (in $10,000s)", value=3.5)
    age = st.number_input("Housing Median Age", value=20)
    rooms = st.number_input("Total Rooms", value=5)
    bedrooms = st.number_input("Total Bedrooms", value=1)
    pop = st.number_input("Population", value=500)
    households = st.number_input("Households", value=200)

    if st.button("Predict Future Value"):
        # 1. Create a DataFrame with the 6 features in the CORRECT ORDER
        # Order must match: housing_median_age, total_rooms, total_bedrooms, population, households, median_income
        features = pd.DataFrame([[age, rooms, bedrooms, pop, households, income]], 
                                columns=["housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income"])
        
        # 2. Scale the features using the loaded scaler
        features_scaled = scaler.transform(features)
        
        # 3. Make the prediction
        prediction = housing_model.predict(features_scaled)
        st.success(f"Predicted Value: ${prediction[0]:,.2f}")

    # Section 2: Logistic Regression (Real Classification)
    st.subheader("✅ Investment Risk Sage")
    credit_score = st.slider("Credit Score", 300, 850, 700)
    debt_ratio = st.slider("Debt-to-Income Ratio", 0.0, 1.0, 0.3)
    if st.button("Classify Risk"):
        # Create input array for the classifier
        # Ensure the order matches your training data (e.g., [Credit, Debt])
        input_data = np.array([[credit_score, debt_ratio]])
        risk_code = bank_model.predict(input_data)
        risk = "Low Risk" if risk_code[0] == 1 else "High Risk"
        st.warning(f"Real Classification: {risk}")
st.title("🏙️ Real Estate Financial Assistant")
st.markdown("Ask me about local properties or SEC filings (e.g., AAPL).")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ask_financial_sage(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})