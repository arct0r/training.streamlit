from datetime import datetime
from model import ex_muscle_groups
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
        




st.markdown(md)

"**Exercise List**"
st.json(ex_muscle_groups, expanded = True)
