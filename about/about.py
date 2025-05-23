import streamlit as st

team = [
    {
        "name": "Archita",
        "role": "Project Lead",
        "major": "Computer Science",
        "year": "3rd Year",
        "img": "/images/archita.jpg",
    },
    {
        "name": "Caitlin",
        "role": "Project Lead",
        "major": "Computer Science",
        "year": "3rd Year",
        "img": "/images/caitlin.jpg",
    },
    {
        "name": "Sruthi",
        "role": "Developer",
        #major
        #year
        "img": "/images/sruthi.jpg",
    },
    {
        "name": "Kelly",
        "role": "Developer",
        "major": "Cognitive Science",
        "year": "1st Year",
        "img": "/images/kelly.jpg",
    },
    {
        "name": "Abirami",
        "role": "Developer",
        #major
        #year
        "img": "/images/abirami.jpg",
    },
    {
        "name": "Miumiu",
        "role": "Developer",
        #major
        #year
        "img": "/images/miumiu.jpg",
    }
]

st.title("About")

st.header("Meet the Team")

cols = st.columns(3)
i = 0
for member in team:
    with cols[i]:
        st.image(member["img"], width=150)
        st.subheader(member["name"])
        st.write(f"**Role:** {member['role']}")
        st.write(f"**Major:** {member['major']}")
        st.write(f"**Year:** {member['year']}")
    i += 1

st.header("About the Model")
st.write(
    "We created this model to..."
)