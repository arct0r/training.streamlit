from sqlalchemy.orm import sessionmaker
#connection to the db
from model import Exercise
from sqlalchemy import create_engine
import streamlit as st
from datetime import datetime

engine = create_engine('sqlite:///stats.sqlite3')
Session = sessionmaker(bind = engine) #this is to connect to the db (engine)
sess = Session()