import streamlit as st
import joblib
import pandas as pd
import numpy as np
from financial_agent import ask_financial_sage

# 1. Page Configuration
st.set_page_config(page_title="Financial Assistant Sage", layout="wide")

# 2. Custom CSS for background contrast and layout
st.markdown("""
    <style>
    /* Background for the Left Sidebar column */
    .stColumn:nth-child(1) {
        background-color: #f1f3f6;
        padding: 15px;
        border-radius: 10px;
    }
    /* Background for the Right Sidebar column */
    .stColumn:nth-child(3) {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
    }
    /* Style for titles within sidebars */
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Models
try:
    housing_model = joblib.load("housing_regressor.joblib")
    bank_model = joblib.load("bank_classifier.joblib")
    scaler = joblib.load("reg_scaler.joblib")
except Exception as e:
    st.error(f"Error loading models: {e}")

# 3. Create the Three-Column Layout
# Sidebars are in col1 and col3, Chat is in col2
col1, col2, col3 = st.columns([1, 2, 1], gap="medium")

# --- LEFT COLUMN (Property Value) ---
with col1:
    st.markdown('<p class="sidebar-title">🏠 Property Sage</p>', unsafe_allow_html=True)
    with st.expander("Show/Hide Controls", expanded=True):
        income = st.number_input("Median Income ($10k)", value=3.5)
        age = st.number_input("Housing Age", value=20)
        rooms = st.number_input("Total Rooms", value=5)
        bedrooms = st.number_input("Total Bedrooms", value=1)
        pop = st.number_input("Population", value=500)
        households = st.number_input("Households", value=200)

        if st.button("Predict Future Value"):
            features = pd.DataFrame([[age, rooms, bedrooms, pop, households, income]], 
                                    columns=["housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income"])
            features_scaled = scaler.transform(features)
            prediction = housing_model.predict(features_scaled)
            st.success(f"Value: ${prediction[0]:,.2f}")

# --- MIDDLE SECTION (Chat Interface) ---
with col2:
    st.title("🏙️ Real Estate Assistant")
    
    # Placeholder for chat history to keep it separate from input
    chat_container = st.container()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input is naturally positioned at the bottom of the column
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        with chat_container:
            with st.chat_message("assistant"):
                response = ask_financial_sage(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# --- RIGHT COLUMN (Investment Risk) ---
with col3:
    st.markdown('<p class="sidebar-title">✅ Risk Sage</p>', unsafe_allow_html=True)
    with st.expander("Show/Hide Controls", expanded=True):
        credit_score = st.slider("Credit Score", 300, 850, 700)
        debt_ratio = st.slider("Debt-to-Income", 0.0, 1.0, 0.3)
        
        if st.button("Classify Risk"):
            input_data = np.array([[credit_score, debt_ratio]])
            risk_code = bank_model.predict(input_data)
            risk = "Low Risk" if risk_code[0] == 1 else "High Risk"
            st.warning(f"Classification: {risk}")