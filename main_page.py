from datetime import datetime
from model import ex_muscle_groups, newEx_muscleGroup, ex_muscles_reset
from interprete import stringChecker, exEstractor
from sqlalchemy import create_engine
from model import createApp
import streamlit as st  


def main_page():
    st.markdown("# terminal")

def page2():
    st.markdown("# stats")
 
page_names_to_funcs = {
    "terminal": main_page,
    "stats": page2,
}


st.markdown("# terminal")
st.sidebar.markdown("# terminal")


fOpen = open("terminal.md", "r")
md = fOpen.read()

name = st.text_area(label = "terminal", height = 40, placeholder=">")
submit = st.button("aight")

if submit and name:
    try:
        stringType = stringChecker(name)
        st.success("data added!")
    except Exception as e:
        name
        st.error(e)
        

col1, col2 = st.columns(2)

with col1:
    with st.expander("Terminal instructions"):
        st.markdown(md)
with col2:
    with st.expander("add an exercise"):

        st.markdown("### Add an exercise")
        exName = st.text_input("exercise name")
        options = st.multiselect(
            'Pick the muscle it works',
            ['chest', 'back', 'shoulders', 'triceps', 'biceps', 'legs'])
        muscleButton = st.button("add exercise")
        exName, options

        if muscleButton and exName and options:
            newEx_muscleGroup(exName, options)
            st.success('exercise added!')



ex_muscle_groups = ex_muscles_reset()
"**Current Exercise List**"
st.json(ex_muscle_groups, expanded = False)
