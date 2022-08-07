import streamlit as st
import pandas as pd
import numpy as np

from model import Exercise, Cardio, other, FitnessGoal, improvementTable, calendarExercises, fill
from main_page import sess


st.markdown("# stats")

muscleGroups = Exercise()
muscleGroups = muscleGroups.populateMuscle_groups(sess)

col1,  col3, col4, col5 = st.columns(4)
with col1:
    st.metric("Weekly cardio", Cardio.weeklyCardio(sess))

with col3:
    st.metric("Focus this week", other.focusWeekly(sess))
with col4:
    st.metric("Focus yesterday", other.focusYesterday(sess))
with col5:
    st.metric("Focus today", other.dailyFocus(sess)[0])
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("CHEST", muscleGroups['chest'])
with col2:
    st.metric("BACK", muscleGroups['back'])
with col3:
    st.metric("LEGS", muscleGroups['legs'])
with col4:
    st.metric("BICEPS", muscleGroups['biceps'])
with col5:
    st.metric("TRICEPS", muscleGroups['triceps'])
with col6:
    st.metric("SHOULDERS", muscleGroups['shoulders'])

muscleGroups = {}


d = improvementTable(sess)


df = pd.DataFrame( data = d )
st.table(df)  # Same as st.write(df)


k = calendarExercises(sess)
fill(k)


dp = pd.DataFrame( data = k )
st.table(dp)  # Same as st.write(df)

week = Exercise.weekWorkouts(sess)