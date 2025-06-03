import streamlit as st
import pycountry
import pandas as pd
import requests
from PIL import Image, ImageOps

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
            response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
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
    def load_and_resize_image(img_path, size=(200, 200)):
        try:
            image = Image.open(img_path)
            image = ImageOps.fit(image, size, method=Image.LANCZOS)  # Crop to fit square
            return image
        except Exception as e:
            st.error(f"Error loading image {img_path}: {e}")
            return None

    team = [
        {"name": "Archita", 
        "role": "Project Lead", 
        "major": "Computer Science", 
        "year": "2nd Year", 
        "img": "headshots/archita.jpg"},

        {"name": "Caitlin", 
        "role": "Project Lead", 
        "major": "Computer Science", 
        "year": "3rd Year", 
        "img": "headshots/caitlin.png"},

        {"name": "Sruthi", 
        "role": "Developer", 
        "major": "Cognitive Science", 
        "year": "1st Year", 
        "img": "headshots/sruthi.jpg"},

        {"name": "Abirami", 
        "role": "Developer", 
        "major": "Data Science", 
        "year": "2nd Year", 
        "img": "headshots/abirami.jpg"},

        {"name": "Miumiu", 
        "role": "Developer", 
        "major": "Statistics", 
        "year": "1st Year", 
        "img": "headshots/miumiu.jpg"},

        {"name": "Viet-Thy", 
        "role": "Developer", 
        "major": "Computer Science", 
        "year": "2nd Year", 
        "img": "headshots/viet-thy.jpeg"}
    ]

    st.title("About")
    st.header("Meet the Team")

    # for i in range(0, len(team), 3):
    #     cols = st.columns(6)
    #     for j in range(3):
    #         if i + j < len(team):
    #             member = team[i + j]
    #             with cols[j]:
    #                 image = load_and_resize_image(member.get("img", ""))
    #                 if image:
    #                     st.image(image, width=150)
    #                 st.subheader(member["name"])
    #                 st.write(f"**Role:** {member['role']}")
    #                 st.write(f"**Major:** {member['major']}")
    #                 st.write(f"**Year:** {member['year']}")

    cols = st.columns(6)
    for idx, member in enumerate(team):
        with cols[idx % 6]:
            image = load_and_resize_image(member.get("img", ""))
            if image:
                st.image(image, width=170)
            st.subheader(member["name"])
            st.markdown(f"**Role:** {member['role']}  ")
            st.markdown(f"**Major:** {member['major']}  ")
            st.markdown(f"**Year:** {member['year']}  ")

    st.header("About the Model")
    st.write("We used an XGBoost classifier to predict the likelihood of being deported based off of 4 critical factors: unviersity, country of origin, visa status, and level of involvement in activism. XGBoost is a high-performance, ensemble-based machine learning algorithms, meaning it builds a series of decision trees in a sequential boosting manner to optimize prediction accuracy. We processed the categorical variables with OrdinalEncoder which maps each category, including unseen categories, to a numerical value. We trained the model using a labeled data set and split the training and test sets in an 80/20 ratio. We trained the model to allow for real-time prediction of deportation probability based on user-provided inputs.")

    st.header("Why We Created Deportation Detector")
    st.write("When we began this project in April 2025, the federal government had begun revoking international student visas at an unprecedented rate, often without clear explanation or adherence to proper due process. In response to this rapidly evolving and opaque issue, we set out to create a resource to support international students facing heightened uncertainty. We developed a deportation prediction tool powered by artificial intelligence that analyzes individual characteristics to estimate the likelihood of deportation, aiming to provide clarity and guidance during a time of significant instability.")

with tabs[2]:
    st.title("🌍 UC Davis International Student Resources")
    st.write(
        'This page is a compiled list of publicly available resources we’ve '
        'gathered to support the UC Davis international and undocumented student community. '
        'If you or someone you know is experiencing immigration-related concerns, we encourage '
        'you to explore the links below or reach out to the listed contacts for support.'
    )

    # Card style with larger fonts
    card_style = """
        <style>
            .resource-card {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 24px;
                background-color: #f9f9f9;
                margin-bottom: 24px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                transition: all 0.2s ease-in-out;
            }
            .resource-card:hover {
                box-shadow: 0 6px 16px rgba(0,0,0,0.1);
                transform: translateY(-2px);
            }
            .resource-title {
                font-weight: 800;
                font-size: 22px;
                margin-bottom: 12px;
            }
            .resource-desc {
                color: #333;
                font-size: 18px;
                line-height: 1.5;
            }
            .resource-link {
                color: #4a8fe7;
                font-weight: bold;
                font-size: 18px;
                text-decoration: none;
                margin-top: 12px;
                display: inline-block;
            }
        </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    # Reusable card component
    def card(title, description, link_text=None, link_url=None, contact_info=None):
        html = f"""
        <div class='resource-card'>
            <div class='resource-title'>{title}</div>
            <div class='resource-desc'>{description}</div>
        """
        if link_url:
            html += f"<div><a class='resource-link' href='{link_url}' target='_blank'>{link_text}</a></div>"
        if contact_info:
            html += f"<div style='margin-top:12px; font-size:18px'>{contact_info}</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)

    # Layout in 2 columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("General Legal Support")

        card(
            title="CIE Guidance for International Scholars and Students",
            description="Official support from UC Davis Global Affairs for international students and scholars.",
            link_text="View",
            link_url="https://cie.ucdavis.edu/resources-and-support/guidance-international-scholars-students"
        )

        card(
            title="Chancellor May Statement on Immigration Enforcement",
            description="Chancellor Gary S. May’s message regarding UC Davis' stance on immigration enforcement actions.",
            link_text="View",
            link_url="https://www.ucdavis.edu/news/statement-chancellor-gary-s-may-federal-immigration-enforcement-actions"
        )

        card(
            title="SISS Immigration News & Updates",
            description="Latest immigration-related news and updates from Services for International Students and Scholars.",
            link_text="View",
            link_url="https://siss.ucdavis.edu/tags/immigration"
        )

        card(
            title="UC Immigrant Legal Services Center",
            description="Free immigration legal support for UC students, including DACA and family petitions.",
            contact_info="📧 ucimm@law.ucdavis.edu | 📞 (530) 752-7996"
        )

        card(
            title="United We Dream Hotline",
            description="A national hotline for reporting immigration-related incidents and seeking urgent help.",
            contact_info="📞 844-363-1423"
        )

    with col2:
        st.subheader("Documents & Policy Letters")

        card(
            title="UC Letter from President Drake and Chancellors (PDF)",
            description="A public statement of support for international and undocumented students and employees across UC campuses.",
            link_text="View",
            link_url="https://cie.ucdavis.edu/sites/g/files/dgvnsk6861/files/media/documents/Letter%20from%20President%20Drake%20-%20Chancellors%20Re%20Guidance%20for%20International%20Undoc%20Students%20and%20Employees.pdf"
        )

        card(
            title="UC Davis Undocumented Student Center",
            description="Campus support center offering advising, financial aid resources, and community support for undocumented students.",
            link_text="Visit",
            link_url="https://undocumented.ucdavis.edu"
        )

        card(
            title="Know Your Rights Flyer (PDF)",
            description="A downloadable flyer outlining your rights in immigration enforcement situations.",
            link_text="View",
            link_url="https://ucdavis.app.box.com/s/qkq3md603pz2pg6739gmxz8x0am1zp1f"
        )

        card(
            title="ICE Guidance on DACA and Enforcement (PDF)",
            description="Information on federal enforcement and Deferred Action for Childhood Arrivals (DACA) policy guidance.",
            link_text="View",
            link_url="https://ucdavis.app.box.com/s/b9hfopab6skq5hbfmcyh2rysw2mk7xs0"
        )

        card(
            title="Quick Guide for UC Davis International & Immigrant Community (PDF)",
            description="A summary resource for finding legal help, emergency contacts, and immigration updates relevant to UC Davis.",
            link_text="View",
            link_url="https://ucdavis.app.box.com/s/knvyfs1wsl1b9v061b1tugk8a38k7yl1"
        )
