import os

from pose_diff.interface.PoseSystem import PoseSystem


class FeedbackSystem(PoseSystem):
    def __init__(self, user_type):
        super().__init__(user_type)

    def get_feedback(self):
        ex_type = self.user_info.preferred_exercise_type
        exercise = self.ex[ex_type]
        tr_type = self.user_info.preferred_trainer
        traier = self.trainer_list[tr_type]
        trainer = os.path.join(self.trainer_base_folder, traier, exercise, 'skeleton.npy')
        user = os.path.join(self.user_base_folder, self.user_info.user_id, exercise, 'trained_skeleton.npy')
        print(trainer)
        print(user)
        re = self.pose_estimation.feedback(user, trainer, ex_type)
        if re == True:
            print("Done")

    def get_real_time_feedback(self):
        pass
