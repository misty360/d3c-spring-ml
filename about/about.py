
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(layout="wide")

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