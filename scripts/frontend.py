import streamlit as st
import pycountry
import pandas as pd
import requests

#Define countries and colleges possible for the dropdown
df = pd.read_csv("us_universities.csv")
universities = sorted(df["name"].dropna().unique().tolist())
countries = sorted([country.name for country in pycountry.countries])

st.header("Deportation Detector")
university_name = st.selectbox(label = "University Name", options = universities)
country_name = st.selectbox(label = "Country Name", options = countries)
visa_status = st.selectbox(label = "US Visa", options = (0, 1))
activism_status = st.selectbox(label = "Activist", options = (0, 1))

chance = st.button(label = "Determine Chance")
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
        st.write(f"Predicted Deportation Probability: {result['deportation_probability']:.2%}")
    else:
        st.error("Error: Could not get prediction from API")