import streamlit as st

# Page setup
st.set_page_config(page_title="UC Davis International Student Resources", layout="wide")

# Title & intro
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
