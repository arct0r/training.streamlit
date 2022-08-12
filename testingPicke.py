import pickle

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

pickled_groups = pickle.dump(ex_muscle_groups, open("ex_groups", "wb"))

unpickled_groups = pickle.load(open("ex_groups", "rb"))
print(unpickled_groups)