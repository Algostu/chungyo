import os
import numpy as np
from pose_diff.util import Common

def test_check_accuracy():
    test_set = load_testSet(1)
    ret_val = Common.check_accuracy(test_set, 1)
    print("Average accuracy: ", ret_val[1])
    assert ret_val[0] == True

def load_testSet(ex_type):
    fileloc = os.path.join('data', 'exercise.txt')
    ex_list = []
    with open(fileloc, 'r') as f:
        ex_list = [line.rstrip('\n') for line in f]
        ex_list = [ex[3:] for ex in ex_list]
    file_name = ex_list[ex_type-1]
    print(file_name)
    testSet = np.load(os.path.join('data', 'testSets', file_name+'.npy'))
    return testSet
