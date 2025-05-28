import streamlit as st

st.set_page_config(page_title="UC Davis International Student Resources", layout="wide")

st.title("🌍 UC Davis International Student Resources")

st.write(
    "Welcome to the UC Davis International Student Resource Hub. "
    "Below are key resources for international and undocumented students, "
    "including legal support, official statements, and informational guides."
)

st.header("🔗 Key Resource Links")

col1, col2 = st.columns(2)

with col1:
    st.subheader("General & Legal Support")
    st.write("CIE Guidance for International Scholars and Students")
    st.link_button("View", "https://cie.ucdavis.edu/resources-and-support/guidance-international-scholars-students")

    st.write("UC Davis Statement on Immigration Enforcement")
    st.link_button("View", "https://www.ucdavis.edu/news/statement-chancellor-gary-s-may-federal-immigration-enforcement-actions")

    st.write("SISS Immigration Tag")
    st.link_button("View", "https://siss.ucdavis.edu/tags/immigration")

    st.write("SISS Main Page")
    st.link_button("Visit", "https://siss.ucdavis.edu/")

    st.write("UC Immigrant Legal Services Center")
    st.write("📧 ucimm@law.ucdavis.edu | 📞 (530) 752-7996")

    st.write("United We Dream Hotline")
    st.write("📞 844-363-1423")

with col2:
    st.subheader("Documents & Policy Letters")
    st.write("Letter from President Drake and Chancellors (PDF)")
    st.link_button("View", "https://cie.ucdavis.edu/sites/g/files/dgvnsk6861/files/media/documents/Letter%20from%20President%20Drake%20-%20Chancellors%20Re%20Guidance%20for%20International%20Undoc%20Students%20and%20Employees.pdf")

    st.write("UC Davis Undocumented Student Center")
    st.link_button("Visit", "https://undocumented.ucdavis.edu")

    st.write("Know Your Rights Flyer (PDF)")
    st.link_button("View", "https://ucdavis.app.box.com/s/qkq3md603pz2pg6739gmxz8x0am1zp1f")

    st.write("ICE Guidance on DACA and Enforcement (PDF)")
    st.link_button("View", "https://ucdavis.app.box.com/s/b9hfopab6skq5hbfmcyh2rysw2mk7xs0")

    st.write("Quick Guide for UC Davis International & Immigrant Community (PDF)")
    st.link_button("View", "https://ucdavis.app.box.com/s/knvyfs1wsl1b9v061b1tugk8a38k7yl1")

st.write("---")
st.write(
    "For urgent matters, please don't hesitate to reach out directly to the listed contacts. "
    "UC Davis is committed to supporting its international and undocumented community."
)