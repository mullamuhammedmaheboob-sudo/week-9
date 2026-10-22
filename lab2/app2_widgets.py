
import streamlit as st
from datetime import date

st.title("Widgets Playground")
name = st.text_input("Name")
age = st.number_input("Age", 1, 100, 20)
marks = st.slider("Marks", 0, 100, 75)
city = st.selectbox("City", ["Chennai", "Mumbai", "Delhi"])
skills = st.multiselect("Skills", ["Python", "ML", "SQL", "Streamlit"])
gender = st.radio("Gender", ["Male", "Female", "Other"])
agree = st.checkbox("I agree to terms")
dob = st.date_input("Date of Birth", date(2000, 1, 1))
file = st.file_uploader("Upload a file")



if st.button("Submit"):
    st.write("Name:", name)
    st.write("Age:", age)
    st.write("Marks:", marks)
    st.write("City:", city)
    st.write("Skills:", skills)
    st.write("Gender:", gender)
    st.write("Agreed:", agree)
    st.write("DOB:", dob)

    if file:
        st.write("File uploaded:", file.name)

st.divider()

st.subheader("Exercise 1: Color Picker")

color = st.color_picker("Pick a color", "#00FF00")
st.write("Selected color:", color)

st.subheader("Exercise 2: Select Slider")

marks_range = st.select_slider(
    "Select a range of marks",
    options=list(range(0, 101)),
    value=(40, 80)
)
st.write("Range:", marks_range)

st.subheader("Exercise 3: Widget Value Types")
st.write("name type:", type(name))
st.write("age type:", type(age))
st.write("marks type:", type(marks))
st.write("city type:", type(city))
st.write("skills type:", type(skills))
st.write("gender type:", type(gender))
st.write("agree type:", type(agree))
st.write("dob type:", type(dob))
if file:
    st.write("file type:", type(file))
