from m_han.RegisterSystem import RegisterSystem
from m_han.TrainSystem import TrainSystem
from m_han.FeedbackSystem import FeedbackSystem

# PoseDifference Class used for delegation
class PoseDifference():
    def __init__(self):
        self.pose_system=None

    def choose_sys_and_option(self, user_type, sys_type, input_type=None):
        u, s = user_type, sys_type

        if s == 0 or u == '':
            raise MyException("Usage: python main.py --user [user type] --sys [system type]")
        elif s == 1:
            self.pose_system = RegisterSystem(u)
            if u == "u":
                self.pose_system.user_info.set_user_id("Enter User Name(will create folder with this name):")
            else:
                self.pose_system.user_info.set_user_id("Enter Trainer Name(will create folder with this name):")
            self.pose_system.regist_info()

        elif s == 2:
            self.pose_system = RegisterSystem(u)
            if u == "u":
                self.pose_system.user_info.set_user_id("Enter User Name(wiil be stored into this user's folder):")
            else:
                self.pose_system.user_info.set_user_id("Enter Trainer Name(wiil be stored into trainer's folder):")
            self.pose_system.regist_skeleton(input_type)

        elif s == 3:
            self.pose_system = TrainSystem(u)
            self.pose_system.user_info.set_user_id("Enter User Name(where output files are stored into):")
            self.pose_system.user_info.set_preferred_exercise_type([self.pose_system.exercise_types,"Enter which exercise you want to train your skeleton:"])
            self.pose_system.user_info.set_preferred_trainer([self.pose_system.trainer_list,'Enter which trainer you want to train your skeleton from:'])
            self.pose_system.train_user_skeleton()
        elif s == 4:
            if u=='u':
                raise MyException("Usage: analysis trainer skeleton only accept trainer")
            self.pose_system = TrainSystem(u)
            self.pose_system.user_info.set_user_id('Enter Trainer Name(where output file will be stored into):')
            self.pose_system.user_info.set_preferred_exercise_type([self.pose_system.exercise_types,'Enter which exercise you want to anaysis:'])
            self.pose_system.analysis_trainer_skeleton()
        elif s == 5:
            self.pose_system = FeedbackSystem(u)
            self.pose_system.user_info.set_user_id("Enter User Name(where output files are stored into):")
            self.pose_system.user_info.set_preferred_exercise_type([self.pose_system.exercise_types,"Enter which exercise you want to learn:"])
            self.pose_system.get_real_time_feedback()
            # 이후에 계속 추가
        else:
            raise MyException("Usage: --sys [1-5]")

class MyException(Exception):
    pass
