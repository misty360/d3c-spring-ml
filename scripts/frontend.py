import streamlit as st
import pycountry
import pandas as pd
import requests

#Set page configuration 
st.set_page_config(page_title = "Deportation Risk Detector", page_icon="⚖️", layout="wide")

st.markdown(
    """
    <style>
    body {
        background: white;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#Define countries and colleges possible for the dropdown
df = pd.read_csv("us_universities.csv")
universities = sorted(df["name"].dropna().unique().tolist())
countries = sorted([country.name for country in pycountry.countries])

st.header("Deportation Detector")
st.markdown("Predict the likelihood of deportation based on university, country, visa, and activism status.")
st.markdown("---")
# university_name = st.selectbox(label = "University Name", options = universities)
# country_name = st.selectbox(label = "Country Name", options = countries)
# visa_status = st.selectbox(label = "US Visa", options = (0, 1))
# activism_status = st.selectbox(label = "Activist", options = (0, 1))

col1, col2 = st.columns(2)

with col1:
    university_name = st.selectbox("🎓 University Name", options=universities)
    visa_status = st.selectbox("🛂 US Visa", options=[0, 1], format_func=lambda x: "Yes" if x else "No")

with col2:
    country_name = st.selectbox("🌍 Country Name", options=countries)
    activism_status = st.selectbox("✊ Activist", options=[0, 1], format_func=lambda x: "Yes" if x else "No")

chance = st.button(label = "🔍 Determine Chance")
if chance:
    input_data = {
        "university": university_name,
        "country": country_name,
        "visa_status": visa_status,
        "activism_status": activism_status
 
    }
    response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
    if response.status_code == 200:
        result = response.json()
        st.success(f"🧾 **Predicted Deportation Probability:** {result['deportation_probability']:.4%}")
    else:
        st.error("Error: Could not get prediction from API")

st.markdown("---")
st.caption("This tool is a prototype for educational purposes only.")
