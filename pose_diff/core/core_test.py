from pose_diff.core import run
import  numpy as np
from pose_diff.core.pose_diff_test import diffing_angle

class Testclass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.score = 100

    def set_score(self):
        self.score = self.score - 1

if __name__ == '__main__':
    user = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/user/IU/walk/trained_skeleton.npy'
    trainer = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/trainer/IU/walk/skeleton.npy'
    exercise = 1 # 'pullup'
    way = 'round'  # round_up, round_down.
    average = 1  # 1은 apply 2는 non
    diffing = 'increase'  # decrease
    run.Video(trainer, user, exercise, diffing, way, average)




    # a = Testclass(10,20)
    # a.set_score()
    # a.set_score()
    #
    # print(a.score)
