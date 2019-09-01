'''
* Writer : hankyul
* Last updated : 2019-08-22
* About what : Estimate Pose from frames
* contens : class->PoseEstimation, function->estimateRealTime,...
'''
import subprocess
import os
import glob
import json
import shutil
import numpy as np
import cv2

# from m_da.PoseDiff import PoseDiff
# from m_seung.Screen import Screen
from m_han.Screen import Screen
from m_han.Common import Common
from m_seung.run import run

# from trainer.parse import load_ps
# from trainer.evaluate import evaluate_pose


# TF-Pose-Estimation
# from tf_pose.estimator import TfPoseEstimator
# from tf_pose.networks import get_graph_path, model_wh

# OpenPose 빌드 다시하면 OpenPose도 추가하기

class PoseEstimation():
    def __init__(self):
        self.common = Common()
        self.screen = Screen()
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
        accuracy, body_part = self.common.check_accuracy(result, -1, 1)
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
        # print(dynamic_skeleton)
        accuracy, body_part = self.common.check_accuracy(dynamic_skeleton, 3, 0)
        l_f = 0
        for part in body_part[1]:
            if part == 1:
                l_f += 1

        res = self.common.calculate_trainer(ex_type, static_skeleton, body_part[0], body_part[1])
        print(res)
        np.save(output_vector, res)
        return True

    def train_exercise(self, ex_type, input_skeleton, input_vector, output_coordinates):
        # print('ex_type : %d' % ex_type)
        # print('input_skeleton : %s' % input_skeleton)
        # print('input_vector : %s' % input_vector)
        # print('output_coordinates : %s' % output_coordinates)
        length = np.load(input_skeleton)
        vector = np.load(input_vector)
        res = self.common.apply_vector(ex_type, length, vector)
        self.screen.draw_humans(res)
        np.save(output_coordinates, res)
        return True

    def show_skeleton(self, npfile):
        run(npfile)

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
