import os
from pose_diff.interface.PoseSystem import PoseSystem

# SubClass
class RegisterSystem(PoseSystem):
    def __init__(self, user_type):
        super().__init__(user_type)

    def regist_info(self):
        if self.user_info.user_type == 'u':
            name = os.path.join('data', 'user', self.user_info.user_id)
        else:
            name = os.path.join('data', 'trainer', self.user_info.user_id)
        res = self.db.create_user(name)
        if res==True:
            print('Done')
        else:
            print('Fail')
            raise MyException('create_user() fail, because this user already exist!')

class MyException(Exception):
    pass
