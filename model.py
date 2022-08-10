from unicodedata import name
import sqlalchemy
from sqlalchemy import create_engine 
from sqlalchemy import Column, String, Integer, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from os import path
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date


Base = declarative_base()
ex_muscle_groups = {
    'dips': ['chest', 'triceps', 'shoulders'],
    'ohp_kb' : ['shoulders', 'triceps'],
    'pullups' : ['back', 'biceps'],
    'chinups' : ['back', 'biceps'],
    'squat' : ['legs'],
    'deadlift' : ['legs', 'back'],
    'bent_over_rows' : ['back', 'biceps'],
    'triceps_extensions' : ['triceps'],
    'bicep_curl' : ['biceps'],
    'leg_curl' : ['legs'],
    'split_squats' : ['legs'],
    't_bar_rows' : ['back', 'biceps'],
    'leg_press' : ['legs'],
    'db_bench_press' : ['chest', 'triceps', 'shoulders'],
    '1arm_crossover' : ['chest'],
    'pullups_bw' : ['back', 'biceps'],
    'nordic_curl' : ['legs']
}

def toWeekDay(num):
    days = { 
        0 : 'monday',
        1 : 'tuesday',
        2 : 'wednesday',
        3 : 'thursday',
        4 : 'friday',
        5 : 'saturday',
        6 : 'sunday'

    }
    return days[num]

def pastDate(days):
    past_date = datetime.now() - timedelta(days=days)
    return past_date

class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    reps = Column(Integer)
    sets = Column(Integer)
    weight = Column(Integer)
    date = Column(DateTime(timezone=True), default=func.now())

    def addExercise(self, sess):
        sess.add(self)
        sess.commit()
        return 0
    
    def weeklyExercises(self, sess):
        past_date = pastDate(7)
        exercises = sess.query(Exercise).filter(
            Exercise.date > past_date
        ).all()
        return exercises
    
    def populateMuscle_groups(self, sess):
        MuscleGroups = {
            'chest' : 0,
            'shoulders' : 0,
            'triceps' : 0 ,
            'back' : 0 ,
            'biceps' : 0 ,
            'legs' : 0,
        }
        exercises = self.weeklyExercises(sess)
        for ex in exercises:
            for group in ex_muscle_groups[ex.name]:
                MuscleGroups[group] += ex.sets
        
        return MuscleGroups

    def weekWorkouts(sess):
        #prima di tutto devo capire che giorno della settimana è questo
        day = datetime.today().weekday() 
        past_date = pastDate(day).date()
        print(past_date)

        #ora trovo tutti gli esercizi fatti durante la settimana
        exs = sess.query(Exercise).filter(
            Exercise.date > past_date
            ).all()
        
        print(exs)
        #ora li ordino in base alla giornata. Non la giornata della settimana. 

        ex_by_day = {}
        

        for ex in exs: 
            weekday = toWeekDay(ex.date.weekday())
            ex_by_day[weekday] = []

        for ex in exs: 
            weekday = toWeekDay(ex.date.weekday())
            ex_by_day[weekday].append(ex)

        print (ex_by_day)


        return ex_by_day
        
    
    def allExercisesTimeFrame(days, sess):
        #returns all the exercises done in the given timeframe for a given user

        pastdate = pastDate(days)
        currentDate = date.today()

        exList = sess.query(Exercise).filter(
                Exercise.date > pastdate
            ).all

    def currentMax(sess, exName):
        
        currentBest = 0
        best = " "
        allExs = sess.query(Exercise).filter_by(name = exName).all()
        for ex in allExs:
            if oneRepMax(ex.weight, ex.reps) > currentBest:
                currentBest = oneRepMax(ex.weight, ex.reps)
                best = f"{ex.weight}kg x {ex.reps}"

        
        return best
    





class Cardio(Base):
    __tablename__ = 'cardio'

    id = Column(Integer(), primary_key=True)
    zone = Column(Integer)
    duration = Column(Integer)
    medium = Column(String(30))
    date = Column(DateTime(timezone=True), default=func.now())

    def addCardio(self, sess):
        sess.add(self)
        sess.commit()
        return 0

    def weeklyCardio(sess):
        weeklyCardio = 0
        past_date = pastDate(7)

        cardioSessions = sess.query(Cardio).filter(
            Cardio.date > past_date
        ).all()

        for session in cardioSessions:
            weeklyCardio += session.duration
        
        return weeklyCardio
    
class FitnessGoal(Base):
    __tablename__ = 'fitnessgoal'

    id = Column(Integer(), primary_key=True)
    name = Column(String(20), unique=True)
    reps = Column(Integer)
    weight = Column(Integer)
    
    def addFitnessGoal(name, weight, reps, sess):
        #qui dovrai aggiungere la ricerca: se esiste già va aggiornato
        goalFound = sess.query(FitnessGoal).filter_by(
            name = name
        ).first()

        if goalFound:
            goalFound.weight = weight
            goalFound.reps = reps
            sess.commit()
            print("goal updated")


        else:
            newGoal = FitnessGoal(name = name, reps = reps, weight = weight)
            sess.add(newGoal)
            sess.commit()
            print("goal added")
        return 0
    
    def goalList(sess):
        goals = sess.query(FitnessGoal).all()
        return goals


class other(Base):
    __tablename__ = 'other'

    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    duration = Column(Integer)
    date = Column(DateTime(timezone=True), default=func.now())

    def addOther(self, sess):
        sess.add(self)
        sess.commit()
        return 0

    def dailyFocus(sess):
        dailyFocus = 0

        focusSessions = sess.query(other).filter(
            other.name == 'focus'
        ).filter(
            other.date > date.today()
        ).all()


        for session in focusSessions:
            dailyFocus += session.duration
        # Get hours with floor division
        hours = dailyFocus // 60

        # Get additional minutes with modulus
        minutes = dailyFocus % 60

        
        return [f"{hours, minutes}"]
    
    def focusYesterday(sess):
        dailyFocus = 0

        focusSessions = sess.query(other).filter(
            other.name == 'focus'
        ).filter(
            other.date == pastDate(1)
        ).all()


        for session in focusSessions:
            dailyFocus += session.duration
        # Get hours with floor division
        hours = dailyFocus // 60

        # Get additional minutes with modulus
        minutes = dailyFocus % 60

        
        return f"{hours, minutes}"
    
    def focusWeekly(sess):
        days = 7
        totalFocus = 0

        focusSessions = sess.query(other).filter(
            other.name == 'focus'
        ).filter(
            other.date > pastDate(7)
        ).all()

def createApp():
    DB_NAME = "database"
    url = 'mysql://sql11512029:hHGENBFyPB@sql11.freemysqlhosting.net/sql11512029'
    
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine) #this is to connect to the db (engine)
    sess = Session()



    return sess



def oneRepMax(weight, reps):
        oneRepMax =  weight / ( 1.0278 - 0.0278 * reps )

        return int(oneRepMax)




def current_maxes(sess, maxesNames):
    
    maxesWeights = []

    for exercise in maxesNames:
        allExs = sess.query(Exercise).filter_by(name = exercise).all()

        bestWeight = 0
        oneRep = 0

        for ex in allExs:
            if oneRepMax(ex.weight, ex.maxReps) > oneRep:
                bestWeight = ex.weight
                oneRep = oneRepMax(ex.weight, ex.maxReps)
                bestString = f"{bestWeight}kg x {ex.maxReps}"
                maxesWeights.append(bestString)

    return maxesWeights

def improvementTable(sess):
    tab = {
    'exercise' : [],
    'current max' : [],
    'goal' : [],
    }
    '''    '30 days imp' : [],
    '90 days imp' : [],
    '180 days imp' : []'''

    goalList = FitnessGoal.goalList(sess)
    
    for goal in goalList:
        tab['exercise'].append(goal.name)

    maxList = []
    for ex in tab['exercise']:
        tab['current max'].append(Exercise.currentMax(sess, ex))
    
    for goal in goalList:
        tab['goal'].append(f"{goal.weight}kg x {goal.reps}")



    return tab

def calendarExercises(sess):
    k = {
    'monday' : [],
    'tuesday' : [],
    'wedsnesday' : [],
    'thursday' : [],
    'friday' : [],
    'saturday' : [],
    'sunday' : [],
    }
    n_to_day = {
        0 : 'monday',
        1 : 'tuesday',
        2 : 'wedsnesday',
        3 : 'thursday',
        4 : 'friday',
        5 : 'saturday',
        6 : 'sunday'
    }
    bob = Exercise()
    weekExercises = bob.weeklyExercises(sess)
    for ex in weekExercises:
        date = ex.date.weekday()
        k[n_to_day[date]].append(f"{ex.name} {ex.weight}kg {ex.sets}x{ex.reps}")
    
    return k

def fill(Dict):
    
    maxLength = 0

    for key in Dict:
        length = len(Dict[key])
        if length > maxLength: 
            maxLength = length
    
    print("max length is ", maxLength)

    emptyList = [' ' for num in range(maxLength)]

    for key in Dict:
        if len(Dict[key]) == 0:
            Dict[key] = emptyList
        elif len(Dict[key]) != 0 and len(Dict[key]) < maxLength:
            difference = maxLength - len(Dict[key])
            for diff in range(difference):
                Dict[key].append(' ')
