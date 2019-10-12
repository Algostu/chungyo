import os
import numpy as np

from pprint import pprint as pp
# from pose_diff.util import Common, Data
import Common,Data

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

def test_filter_outlier():
    ex_name, test_sets = Data.load_testSet(3, view=2)
    part_name = Common.PART_NAMES
    i = 1
    for testset in test_sets:
        joints = list(zip(*testset))
        for joint, name in zip(joints[:10], part_name[:10]):
            Common.filter_outlier(list(joint), True, name+"_"+str(i))
        i+=1

def test_data():
    #########################
    # How it works
    # check x in (0< x < 0.5)
    #########################
    ex_name, test_sets = Data.load_testSet(3, view=2)
    part_name = Common.PART_NAMES
    for testset in test_sets:
        joints = list(zip(*testset))
        print("-------------------")
        for joint, name in zip(joints, part_name):
            print(name)
            outlier = [i for i,x in enumerate(joint) if .5>x[2]>0]
            print(outlier)

def test_filter_noise():
    ex_name, test_sets = Data.load_testSet(3)
    part_name = Common.PART_NAMES
    i = 1
    for testset in test_sets:
        joints = list(zip(*testset))
        for joint, name in zip(joints[1:2], part_name[1:2]):
            Common.filter_noise(list(joint), True, name+"_"+str(i))
        i+=1

def test_circle_filter_noise():
    ex_name, test_sets = Data.load_testSet(3)
    part_name = Common.PART_NAMES
    joints = list(zip(*test_sets[0]))
    Common.circle_filter_noise(joints[2], joints[3])

if __name__=='__main__':
    test_circle_filter_noise()
