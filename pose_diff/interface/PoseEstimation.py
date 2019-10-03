import subprocess
import os
import glob
import json
import shutil
import numpy as np
from pose_diff.util import Common
from pose_diff.core.run import Video

# OpenPose 빌드 다시하면 OpenPose도 추가하기

class PoseEstimation():
    def __init__(self):
        # self.screen = Screen()
        # self.pose_diff = PoseDiff()
        self.post_procedure_call_list = [
            "OpenPose로 동영상 분석해서 skeleton.npy저장"
            "Angle+Accuracy",
            "Pose Difference between User and Trainer",
            "Screen을 이용해서 Window에 출력",
            "tf-pose이용해서 window에 출력"
            "Train용으로 분석하기"
        ]
    def estimate_real_time(self, post_procedure_call_list):
        pass

    # json 파일 지우는거 해야됨
    def parse_video(self, user_name, input_folder, output_folder):
        print('Processing parse_video...')
        openpose_path = os.path.join('bin', 'OpenPoseDemo.exe')
        model = 'COCO'
        output_path = os.path.join('tmp', user_name)
        os.chdir('openpose')
        if os.path.isdir(output_path):
            shutil.rmtree(output_path)

        subprocess.call([openpose_path,
                        '--model_pose', model,
                        '--video', os.path.join('..',input_folder),
                        '--number_people_max', '1',
                        '--write_video', os.path.join(output_path, 'result.avi'),
                        '--write_json', output_path])
        os.chdir('..')

        # json file Read
        json_files = glob.glob(os.path.join('openpose/tmp/', user_name,'*.json')) # 저장한 폴더 바꿔주기
        json_files = sorted(json_files)

        num_frames = len(json_files)

        all_keypoints = np.zeros((num_frames, 18, 3))
        for i in range(num_frames):
            with open(json_files[i]) as f:
                json_obj = json.load(f)
                keypoints = np.array(json_obj['people'][0]['pose_keypoints_2d'])
                all_keypoints[i] = keypoints.reshape((18, 3))

        np.save(output_folder, all_keypoints)
        return True

    def parse_picture(self, user_name, input_folder, output_folder):
        print('Processing parse_picture...')
        openpose_path = os.path.join('bin', 'OpenPoseDemo.exe')
        model = 'COCO'
        output_path = os.path.join('tmp', user_name)
        os.chdir('openpose')
        if os.path.isdir(output_path):
            shutil.rmtree(output_path)

        subprocess.call([openpose_path,
                        '--model_pose', model,
                        '--image_dir', os.path.join('..',input_folder),
                        '--number_people_max', '1',
                        '--write_json', output_path])
        os.chdir('..')

        # json file Read
        json_files = glob.glob(os.path.join('openpose/tmp/', user_name,'*.json')) # 저장한 폴더 바꿔주기
        json_files = sorted(json_files)

        num_frames = len(json_files)

        all_keypoints = np.zeros((num_frames, 18, 3))
        for i in range(num_frames):
            with open(json_files[i]) as f:
                json_obj = json.load(f)
                keypoints = np.array(json_obj['people'][0]['pose_keypoints_2d'])
                all_keypoints[i] = keypoints.reshape((18, 3))

        np.save(output_folder, all_keypoints)
        return True

    def find_initial_skeleton(self, base, output_folder, numpy_file = 'initial_skeleton', img_file = 'initial_pose'):
        print('Processing find_initial_skeleton...')
        result = np.load(base)
        # check_accuracy(frames, exercise_type, exit_flags)
        accuracy, body_part = Common.check_accuracy(result, 0, 1)
        # body_part가 한개일때도 [frame] 이런 식으로 저장됨
        keypoints = np.array(body_part)
        # print(keypoints)
        np.save(os.path.join(output_folder, numpy_file), keypoints)

        # self.screen.draw_humans(body_part, os.path.join(output_folder, img_file))
        return True

    def analyze_exercise(self, ex_type, input_skeleton, output_skeleton, output_vector):
        print('Processing analyze_exercise...')
        skeleton = np.load(input_skeleton)
        static_skeleton = skeleton[0]
        dynamic_skeleton = np.load(output_skeleton)
        test_res = Common.check_accuracy(dynamic_skeleton, ex_type)

        if test_res[0] == True:
            res = Common.calculate_trainer(ex_type, static_skeleton, dynamic_skeleton)
            np.save(output_vector, res)
            return True
        else:
            print("This input file is not proper to use")
            return False

    def train_exercise(self, ex_type, input_skeleton, input_vector, output_coordinates):
        # print('ex_type : %d' % ex_type)
        # print('input_skeleton : %s' % input_skeleton)
        # print('input_vector : %s' % input_vector)
        # print('output_coordinates : %s' % output_coordinates)
        length = np.load(input_skeleton)
        vector = np.load(input_vector)
        res = Common.apply_vector(ex_type, length, vector)
        # self.screen.draw_humans(res)
        np.save(output_coordinates, res)
        return True

    def feedback(self, user, trainer, ex_type):
        print("feedback processing....", end="")

        video = Video(trainer, user, "pullup", "increase", "round", 1)
        return True


    def check_procedure_list(self, option_list):
        if len(option_list) != 5:
            raise MyException('Procedure List length should be 5')
        else:
            print("--------------Procedure List--------------------")
            for i, procedure in enumerate(self.post_procedure_call_list):
                if option_list[i] == 1:
                    print("%d. %s" % (i+1, procedure))
            print("------------------------------------------------")


class MyException(Exception):
    pass
