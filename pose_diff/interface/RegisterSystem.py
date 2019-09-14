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

    def regist_skeleton(self, input_type):
        # User와 Trainer따로 구분하는 부분
        input = ""
        output = ""
        if self.user_info.user_type == 'u':
            # 파일이름은 정해진대로 사용한다.
            type = 'user'
            path = os.path.join(self.user_base_folder, self.user_info.user_id)
        else:
            type = 'trainer'
            path = os.path.join(self.trainer_base_folder, self.user_info.user_id)

        # User가 존재하는지 확인하는 부분
        res = self.check_exists(self.user_info.user_type, self.user_info.user_id)
        if res == True:
            print("Done")
        else:
            print("Fail")
            raise MyException("This user does not exist!")

        # input과 output을 정하는 부분
        for file in os.listdir(path):
            if os.path.splitext(file)[0] == self.initial:
                input = os.path.join(path, os.path.basename(file))

        output = os.path.join(path, self.skeleton)
        output_folder = output+'.npy'
        base = os.path.join(path, 'base')
        if os.path.isdir(base) == False:
            os.mkdir(base)

        if input == "" and input_type == None:
            raise MyException("initial_video file does not exist")

        # self.pose_estimation.check_procedure_list([0,0,0,0,0])
        if input_type != None:
            res = self.pose_estimation.parse_picture(self.user_info.user_id, path, os.path.join(base, 'initial_skeleton'))
            if res == True:
                print("Done")
                print("Successfully stored initial_skeleton.npy into /data/%s/%s/base folder" % (type, self.user_info.user_id))
                return True
            else:
                raise MyException('parse_picture failed for some reason')

        if os.path.isfile(output_folder) == False:
            res = self.pose_estimation.parse_video(self.user_info.user_id, input, output)
            if res == True:
                print("Done")

        res = self.pose_estimation.find_initial_skeleton(output_folder, base)
        if res == True:
            print('Done')
            print("Successfully stored skeleton.json into /data/%s/%s/ folder" % (type, self.user_info.user_id))
        else:
            print("Fail")
            raise MyException('estimate_video failed for some reason')
class MyException(Exception):
    pass
