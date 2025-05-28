import streamlit as st

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
        #CHECK THIS
        "major": "Cognitive Science",
        "year": "1st Year",
        #"img": "/images/sruthi.jpg",
    },
    {
        "name": "Abirami",
        "role": "Developer",
        #CHECK THIS
        "major": "Data Science",
        "year": "1st Year",
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
        "year": "1st Year",
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