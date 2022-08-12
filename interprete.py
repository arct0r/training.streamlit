from time import timezone
from model import ex_muscle_groups
from model import Cardio, FitnessGoal, createApp, Exercise, other
from datetime import datetime
import streamlit as st
from model import createApp

sess = createApp()

def stringChecker(String):
    initialString = String
    hasLines = False
    if initialString.split("\n"):
        hasLines = True

    start = String.lower().split()[0]
    if start == 'goal' and String.lower().split()[1] in ex_muscle_groups:
        print("setting goal")
        return goalExtractor(String)
    if start == 'cardio':
        print("extracting cardio")
        return cardioExtractor(String)
    if start == 'focus':
        print("extracting focus")
        return focusExtractor(String)
    if ex_muscle_groups[start] and hasLines:
        print("extracting multiple lines res")
        return lines_exEstractor(initialString)
    if ex_muscle_groups[start]:
        print("adding res")
        exAdded = exEstractor(String)
        return exAdded
    elif start == 'focus':
        return 'focus'

    elif start == 'set':

        return 'goal'

def goalExtractor(String):
    #goal dips 30kg x3
    String = String.rstrip().lower().split()
    name = String[1]
    weight = String[2][:-2]
    reps = String[3][1:]

    try:
        FitnessGoal.addFitnessGoal(name, weight, reps, sess)
        sess.commit()
    except:
        sess.rollback()
        raise

def cardioExtractor(String):
    #cardio zone 2 30min cyclette
    String = String.rstrip().lower().split()
    String.pop(0)
    String.pop(0)
    zone = String[0]
    String.pop(0)
    duration = String[0][:-3]
    String.pop(0)
    medium = String[0]

    newCardio = Cardio(zone = zone, duration = duration, medium = medium, date = datetime.now())
    try:
        newCardio.addCardio(sess)
        sess.commit()
    except:
        sess.rollback()
        raise

def focusExtractor(String):
    #focus 30min
    String = String.rstrip().lower().split()
    String.pop(0)
    time = String[0][:-3]

    newFocus = other(name = 'focus', duration = time, date = datetime.now())
    try:
        newFocus.addOther(sess)
        sess.commit()
    except:
        sess.rollback()
        raise

def lines_exEstractor(String):
    for line in String.split("\n"):
        exEstractor(line)


def exEstractor(String):
    #type 1: dips 100kg 3x5

    exercise = {
        'name' : None,
        'weight' : None,
        'sets' : None,
        'maxReps' : None
        
    }
    String = String.lower().rstrip().split()
    name = String[0]
    weight = String[1][:-2]
    sets = String[2].split("x")[0]
    reps = String[2].split("x")[1]
    
    ex = Exercise(name = name, reps = reps, sets = sets, weight = weight, date = datetime.now())
    try:
        ex.addExercise(sess)
        sess.commit()
        return f"Added {ex.name} {ex.weight}kg {ex.sets}x{ex.reps}"

    except:
        sess.rollback()
        raise

