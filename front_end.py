import streamlit as st

st.set_page_config(page_title="UC Davis International Student Resources", layout="wide")

st.header("🔗 Key Resource Links")
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
