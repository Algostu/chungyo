import os
import numpy as np

from pprint import pprint as pp
from pose_diff.util import Common

# Test functions
def test_check_accuracy():
    test_set = load_testSet(1)
    ret_val = Common.check_accuracy(test_set, 1)
    print("Average accuracy: ", ret_val[1])
    assert ret_val[0] == True

def test_calculate_trainer():
    assert 1==1
    # for i in range(pairs_len):
    #     if frames_len_1 != len(body_movement_length[i]):
    #         print("%d : length numbers are not same" % i)
    #         frames_len_1 = len(body_movement_length[i])
    #         print(frames_len_1)
    #     if frames_len_2 != len(body_movement_vector[i]):
    #         print("%d : vector numbers are not same" % i)
    #         frames_len_2 = len(body_movement_vector[i])
    #         print(frames_len_2)
    #
    # if frames_len_1 == frames_len_2:
    #     frame_len = frames_len_1

def test_cal_blank():
    test_set = load_testSet(1)
    for testset in test_set:
        joints = zip(*testset)
