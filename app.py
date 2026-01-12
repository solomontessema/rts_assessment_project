import streamlit as st
import joblib
import pandas as pd
import numpy as np
from financial_agent import ask_financial_agent

# 1. Page Config
st.set_page_config(page_title="Real Estate Financial Assistant", layout="wide")

# 2. Bright & Optimistic Glassmorphism CSS
st.markdown("""
    <style>
    /* 1. Bright, Optimistic Gradient Background */
    .stApp {
        background: linear-gradient(120deg, #e0f7fa 0%, #ffffff 50%, #e1f5fe 100%);
        background-attachment: fixed;
    }

    /* 2. Floating Sidebar (Light Glass) */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* 3. Floating Middle Section (Main Card) */
    .main .block-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 40px;
        margin-top: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); /* Soft, subtle shadow */
    }

    /* 4. Text & Header Colors (Clean Dark Grey for readability) */
    h1, h2, h3, p, span, label {
        color: #2c3e50 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 5. Modern Button Styling */
    .stButton>button {
        border-radius: 12px;
        background-color: #00bcd4;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0097a7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Artifact Loading ---
try:
    housing_model = joblib.load("artifacts/housing_regressor.joblib")
    bank_model = joblib.load("artifacts/bank_classifier.joblib")
    housing_scaler = joblib.load("artifacts/housing_scaler.joblib") 
    bank_scaler = joblib.load("artifacts/bank_scaler.joblib")
except Exception as e:
    st.error(f"Error loading models: {e}")

# --- Sidebar (Left Floating Card) ---
with st.sidebar:
    st.title("🏠 Property Value Predictor")
    income = st.number_input("Median Income ($10k)", value=3.5)
    age = st.number_input("Housing Age", value=20)
    rooms = st.number_input("Total Rooms", value=5)
    bedrooms = st.number_input("Total Bedrooms", value=1)
    pop = st.number_input("Population", value=500)
    households = st.number_input("Households", value=200)

    if st.button("Predict Future Value"):
        features = pd.DataFrame([[age, rooms, bedrooms, pop, households, income]], 
                                columns=["housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income"])
        features_scaled = housing_scaler.transform(features)
        prediction = housing_model.predict(features_scaled)
        st.success(f"Estimated Value: ${prediction[0]:,.2f}")

    st.markdown("---")
    st.subheader("✅ Risk Predictor")
    credit_score = st.slider("Credit Score", 300, 850, 700)
    debt_ratio = st.slider("Debt-to-Income", 0.0, 1.0, 0.3)
    if st.button("Classify Risk"):
        input_df = pd.DataFrame([[credit_score, debt_ratio]], columns=['credit_score', 'debt_ratio'])
        input_scaled = bank_scaler.transform(input_df)
        risk_code = bank_model.predict(input_scaled)
        risk = "Low Risk" if risk_code[0] == 1 else "High Risk"
        st.info(f"Classification: {risk}")

# --- Main Section (Middle Floating Card) ---
st.title("🏙️ Real Estate Financial Assistant")
st.markdown("Discover property insights and analyze SEC filings with AI.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = ask_financial_agent(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})