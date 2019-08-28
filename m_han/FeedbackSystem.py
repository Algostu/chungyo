from m_han.PoseSystem import PoseSystem

class FeedbackSystem(PoseSystem):
    def __init__(self, user_type):
        super().__init__(user_type)

    def get_real_time_feedback(self):
        pass
