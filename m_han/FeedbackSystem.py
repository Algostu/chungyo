import os

from m_han.PoseSystem import PoseSystem


class FeedbackSystem(PoseSystem):
    def __init__(self, user_type):
        super().__init__(user_type)

    def get_real_time_feedback(self):
        ex_type = self.user_info.preferred_exercise_type
        exercise = self.ex[ex_type]
        # path = os.path.join(self.user_base_folder, self.user_info.user_id, exercise, "trained_skeleton.npy")
        path = os.path.join(self.trainer_base_folder, self.user_info.user_id, 'skeleton.npy')
        print(path)
        self.pose_estimation.show_skeleton(path)
