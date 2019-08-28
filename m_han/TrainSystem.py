from m_han.PoseSystem import PoseSystem
import os

class TrainSystem(PoseSystem):
    def __init__(self, user_type):
        super().__init__(user_type)

    def train_user_skeleton(self):
        pass

    def analysis_trainer_skeleton(self):
        # 동영상이 저장되어있는 Path와 운동별로 저장할 폴더를 설정
        ex_type = self.user_info.preferred_exercise_type
        exercise = self.ex[ex_type]
        path = os.path.join(self.trainer_base_folder, self.user_info.user_id)
        base = os.path.join(path, exercise)
        # print("Debug Base Folder loc : ", base)

        # user
        print('Check target folder exist...', end=' ')
        res = os.path.isdir(path)
        if res == True:
            print("Done")
        else:
            print("Fail")
            raise MyException("This user does not exist!")

        # input
        print('Check if trainer skeletons are analized...', end=' ')
        skeleton = os.path.join(path, 'base')
        res = os.path.isdir(skeleton)
        if res == True:
            input_skeleton = os.path.join(skeleton, 'initial_skeleton.npy')
            print("Done")
        else:
            print("Fail")
            raise MyException("This trainer have not registered yet")
        input_video= ""
        for file in os.listdir(path):
            if os.path.splitext(file)[0] == exercise:
                input_video = os.path.join(path, os.path.basename(file))
        if input_video == "":
            raise MyException("%s video file does not exist" % exercise)

        # output
        if os.path.isdir(base) == False:
            os.mkdir(base)
        output_skeleton = os.path.join(base, self.skeleton)
        output_vector = os.path.join(base, self.vector)

        print('Target exercise are analized before..?', end = ' ')
        if os.path.isfile(output_skeleton+'.npy') == False:
            print("Nope")
            res = self.pose_estimation.parse_video(self.user_info.user_id, input_video, output_skeleton)
            if res == True:
                print("Done")
                print("Successfully stored skeleton.npy into /data/%s/%s/%s folder" % (self.user_info.user_type, self.user_info.user_id, exercise))
            else:
                print("Fail")
                raise MyException('parse_video failed for some reason')
        else:
            print('Yes!')
        
        res = self.pose_estimation.analyze_exercise(ex_type, input_skeleton, output_skeleton+'.npy', output_vector)
        if res == True:
            print('Done')
            print("Successfully stored vector.npy into /data/%s/%s/%s folder" % (self.user_info.user_type, self.user_info.user_id, exercise))
        else:
            print("Fail")
            raise MyException('analyze_exercise failed for some reason')
class MyException(Exception):
    pass
