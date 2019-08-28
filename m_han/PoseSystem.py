import os
from enum import Enum

from m_han.UserInfo import UserInfo
from m_han.DB import DB
from m_han.PoseEstimation import PoseEstimation

# Super Class for Each System
class PoseSystem():
    def __init__(self, user_type):
        self.user_info = UserInfo(user_type)
        self.db = DB()
        self.pose_estimation = PoseEstimation()
        self.user_base_folder = os.path.join('data', 'user')
        self.trainer_base_folder = os.path.join('data', 'trainer')
        self.trainer_list = self.db.read_dir_list(self.trainer_base_folder)
        self.user_list = self.db.read_dir_list(self.user_base_folder)
        self.exercise_types = self.db.read_exercise_list(None)

        # fileNames
        self.initial = 'initial_video'
        self.skeleton = 'skeleton'
        self.initial_skeleton = 'initial_skeleton'
        self.trained_skeleton = 'trained_skeleton'
        self.vector = 'vector'
        self.size = 'size'
        self.ex = [type[3:] for type in self.exercise_types]


    def check_exists(self, u, name):
        print('Check target folder...', end='')
        if u == 'u':
            if name in self.user_list:
                return True
            else:
                return False
        else:
            if name in self.trainer_list:
                return True
            else:
                return False
