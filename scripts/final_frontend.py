import streamlit as st
import pycountry
import pandas as pd
import requests
from PIL import Image

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

#Implement tabs 
tabs = st.tabs(["Home", "About", "Resources"])

#Home page
with tabs[0]:
    image = Image.open("banner_image3.png")
    # width, height = image.size
    # new_height = height // 2  # Half the original height
    # resized_image = image.resize((width, new_height))
    st.image(image, use_container_width=True)
    st.title("Deportation Detector")
    st.markdown("Predict the likelihood of deportation based on university, country, visa, and activism status.")
    st.markdown("---")

    # Load data
    df = pd.read_csv("us_universities.csv")
    universities = sorted(df["name"].dropna().unique().tolist())
    countries = sorted([country.name for country in pycountry.countries])

    col1, col2 = st.columns(2)

    with col1:
        university_name = st.selectbox("University Name", options=universities)
        visa_status = st.selectbox("US Visa", options=[0, 1], format_func=lambda x: "Yes" if x else "No")

    with col2:
        country_name = st.selectbox("Country Name", options=countries)
        activism_status = st.selectbox("Activist", options=[0, 1], format_func=lambda x: "Yes" if x else "No")

    chance = st.button(label="🔍 Determine Chance")
    if chance:
        input_data = {
            "university": university_name,
            "country": country_name,
            "visa_status": visa_status,
            "activism_status": activism_status
        }
        try:
            response = requests.post("http://127.0.0.1:8501/predict", json=input_data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"🧾 **Predicted Deportation Probability:** {result['deportation_probability']:.4%}")
            else:
                st.error("Error: Could not get prediction from API")
        except:
            st.error("Failed to connect to prediction API.")

    st.markdown("---")
    st.caption(
    "This tool is a prototype created solely for educational and awareness purposes. "
    "It is not intended to predict real-world outcomes, cause alarm, or promote fear. "
    "Rather, it aims to highlight how certain factors may influence risk in a data-driven context and "
    "encourage informed dialogue around immigration systems and advocacy support."
)


#About page 
with tabs[1]:
    team = [
        {
            "name": "Archita",
            "role": "Project Lead",
            "major": "Computer Science",
            "year": "3rd Year",
            #"img": "/images/archita.jpg",
        },
        {
            "name": "Caitlin",
            "role": "Project Lead",
            "major": "Computer Science",
            "year": "3rd Year",
            #"img": "/images/caitlin.jpg",
        },
        {
            "name": "Sruthi",
            "role": "Developer",
            "major": "Cognitive Science",
            "year": "1st Year",
            #"img": "/images/sruthi.jpg",
        },
        {
            "name": "Abirami",
            "role": "Developer",
            "major": "Data Science",
            "year": "2nd Year",
            #"img": "/images/abirami.jpg",
        },
        {
            "name": "Miumiu",
            "role": "Developer",
            #CHECK THIS
            "major": "Statistics",
            "year": "1st Year",
            #"img": "/images/miumiu.jpg",
        },
        {
            "name": "Viet-Thy",
            "role": "Developer",
            #CHECK THIS
            "major": "Computer Science",
            "year": "2nd Year",
            #"img": "/images/miumiu.jpg",
        }
    ]

    st.title("About")

    st.header("Meet the Team")

    for i in range(0, len(team), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(team):
                member = team[i + j]
                with cols[j]:
                    # st.image(member.get("img", ""), width=150)
                    st.subheader(member["name"])
                    st.write(f"**Role:** {member['role']}")
                    st.write(f"**Major:** {member['major']}")
                    st.write(f"**Year:** {member['year']}")

    st.header("About the Model")
    st.write(
        "We created this model to..."
    )

with tabs[2]:
    st.title("Key Resource Links")
    st.write('This page is a compiled list of publicly available resources we’ve '
         'gathered to support the UC Davis international and undocumented student community. '
         'If you or someone you know is experiencing immigration-related concerns, we encourage '
         'you to explore the links below or reach out to the listed contacts for support.')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("General Legal Support")

        st.write("CIE Guidance for International Scholars and Students")
        st.write("<small style='color:gray'>Official support from UC Davis Global Affairs for international students and scholars.</small>", unsafe_allow_html=True)
        st.link_button("View", "https://cie.ucdavis.edu/resources-and-support/guidance-international-scholars-students")

        st.write("Chancellor May Statement on Immigration Enforcement")
        st.write("<small style='color:gray'>Chancellor Gary S. May’s message regarding UC Davis' stance on immigration enforcement actions.</small>", unsafe_allow_html=True)
        st.link_button("View", "https://www.ucdavis.edu/news/statement-chancellor-gary-s-may-federal-immigration-enforcement-actions")

        st.write("SISS Immigration News & Updates")
        st.write("<small style='color:gray'>Latest immigration-related news and updates from Services for International Students and Scholars (SISS).</small>", unsafe_allow_html=True)
        st.link_button("View", "https://siss.ucdavis.edu/tags/immigration")

        st.write("UC Immigrant Legal Services Center")
        st.write("<small style='color:gray'>Free immigration legal support for UC students, including DACA and family petitions.</small>", unsafe_allow_html=True)
        st.write("📧 ucimm@law.ucdavis.edu | 📞 (530) 752-7996")

        st.write("United We Dream Hotline")
        st.write("<small style='color:gray'>A national hotline for reporting immigration-related incidents and seeking urgent help.</small>", unsafe_allow_html=True)
        st.write("📞 844-363-1423")

    with col2:
        st.subheader("Documents & Policy Letters")

        st.write("UC Letter from President Drake and Chancellors (PDF)")
        st.write("<small style='color:gray'>A public statement of support for international and undocumented students and employees across UC campuses.</small>", unsafe_allow_html=True)
        st.link_button("View", "https://cie.ucdavis.edu/sites/g/files/dgvnsk6861/files/media/documents/Letter%20from%20President%20Drake%20-%20Chancellors%20Re%20Guidance%20for%20International%20Undoc%20Students%20and%20Employees.pdf")

        st.write("UC Davis Undocumented Student Center")
        st.write("<small style='color:gray'>Campus support center offering advising, financial aid resources, and community support for undocumented students.</small>", unsafe_allow_html=True)
        st.link_button("Visit", "https://undocumented.ucdavis.edu")

        st.write("Know Your Rights Flyer (PDF)")
        st.write("<small style='color:gray'>A downloadable flyer outlining your rights in immigration enforcement situations.</small>", unsafe_allow_html=True)
        st.link_button("View", "https://ucdavis.app.box.com/s/qkq3md603pz2pg6739gmxz8x0am1zp1f")

        st.write("ICE Guidance on DACA and Enforcement (PDF)")
        st.write("<small style='color:gray'>Information on federal enforcement and Deferred Action for Childhood Arrivals (DACA) policy guidance.</small>", unsafe_allow_html=True)
        st.link_button("View", "https://ucdavis.app.box.com/s/b9hfopab6skq5hbfmcyh2rysw2mk7xs0")

        st.write("Quick Guide for UC Davis International & Immigrant Community (PDF)")
        st.write("<small style='color:gray'>A summary resource for finding legal help, emergency contacts, and immigration updates relevant to UC Davis.</small>", unsafe_allow_html=True)
        st.link_button("View", "https://ucdavis.app.box.com/s/knvyfs1wsl1b9v061b1tugk8a38k7yl1")
