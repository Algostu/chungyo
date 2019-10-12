import os
import numpy as np
def load_testSet(ex_type,user_type=1, view=1):
    user = 'userSet' if user_type == 1 else 'trainerSet'
    view = 'front' if view == 1 else 'side'
    fileloc = os.path.join('data', 'exercise.txt')
    ex_list = []
    with open(fileloc, 'r') as f:
        ex_list = [line.rstrip('\n') for line in f]
        ex_list = [ex[3:] for ex in ex_list]
    path = os.path.join('data', 'testSets', ex_list[ex_type-1], view, user)
    numpy_list = [np.load(os.path.join(path, file)) for file in os.listdir(path)]
    return ex_list[ex_type-1], numpy_list
