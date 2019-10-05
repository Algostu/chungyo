############################################
# Basic Info
# 주요 기능들의 Interface격인 함수들을 모아놨다.
# parse_person : openpose를 이용해서 사람의 부위 분석
# find_initial_skeleton : 운동 동영상 내에서 사람의 신체 길이 측정
# analyze_exercise : 운동에 필요한 부위가 들어있는지, Outlier는 없는지 등을 검사하고 운동할때 발생하는 값들을 저장한다.

# Feature
#

# Todo
#
############################################
import subprocess
import os
import glob
import json
import shutil
import time
import numpy as np
from pose_diff.util import Common
import matplotlib.pyplot as plt

def parse_person(input_video_loc, option=1):
    ####################################
    # Basic Info
    # Params
    # input_video_loc : Video location for parsing
    # How it works
    # input_video_loc으로 전달받은 비디오를 openpose로 분석한다.
    # Return
    # 좌표값이 들어간 numpy

    # Feature
    # option = 1 : Video Parsing
    # opetion = 2 : Image Parsing

    # Todo
    # Json, Video, Image Option
    # Demo -> Build
    ####################################

    # Parse video using OpenPose Demo
    os.chdir('openpose')
    openpose_path = os.path.join('bin', 'OpenPoseDemo.exe')
    model = 'COCO'
    output_path = 'temp'

    parsing_objects = ['--video', '--image_dir']
    if option not in (1, 2):
        print("Error: Option should be 1 or 2")
        return

    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    time.sleep(1)

    os.mkdir(output_path)

    subprocess.call([openpose_path, # Issue : Output is only json
                    '--model_pose', model,
                    parsing_objects[option-1], os.path.join('..',input_video_loc),
                    '--number_people_max', '1',
                    '--write_json', output_path])

    # Read json file and Make Numpy Array
    json_files = glob.glob(os.path.join('temp/', '*.json'))
    json_files = sorted(json_files)

    num_frames = len(json_files)

    all_keypoints = np.zeros((num_frames, 18, 3))
    for i in range(num_frames):
        with open(json_files[i]) as f:
            json_obj = json.load(f)
            keypoints = np.array(json_obj['people'][0]['pose_keypoints_2d'])
            all_keypoints[i] = keypoints.reshape((18, 3))

    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.chdir('..')

    return all_keypoints

def find_initial_skeleton(numpy_array):
    ####################################
    # Basic Info
    # params
    # numpy_array: 서있는 모습이 담긴 numpy array이다.
    # How it works
    # 팔꿈치와 무릎의 각도가 일정한 각도에서 일정하게 유지될때 중에서 신체의 길이가 가장 길때를 신체 사이즈로 측정한다.
    # Return Values
    # skeleton이 담긴 numpy array
    # Return값이 False인경우 Initial Pose를 찾지 못했다.

    # Feature
    #

    # Todo
    # UI
    # UI Event 설정
    ####################################
    skeleton = []
    left_elbow = []
    right_elbow = []
    left_knee = []
    right_knee = []

    # Calculate angle
    for frame in numpy_array:
        left_elbow.append(Common.get_angle(frame[2], frame[3], frame[4]))
        right_elbow.append(Common.get_angle(frame[5], frame[6], frame[7]))
        left_knee.append(Common.get_angle(frame[8], frame[9], frame[10]))
        right_knee.append(Common.get_angle(frame[11], frame[12], frame[13]))

    # Find 정지된 자세
    stop_len = 30 # 정지된 상태로 있어야 하는 시간이다. (단위는 프레임)
    stop_i = 0 # 정지된 상태가 지속된 시간이다.
    height = [] # 정지된 상태에서 측정된 키의 리스트이다.
    frames = [] # 정지된 상태에서의 프레임이다.
    for frame, l_e, r_e, l_k, r_k in zip(numpy_array, left_elbow, right_elbow, left_knee, right_knee):
        if (175 < l_e < 185) and (175 < r_e < 185) and (175 < l_k < 185) and (175 < r_k < 185):
            stop_i += 1
        else:
            stop_i = 0
        if stop_i >= stop_len:
            height.append(get_body_len(frame))
            frames.append(frame)

    # Initial Pose를 찾을 수 없을 경우 False를 Return 한다.
    if len(height) != 0:
        skeleton = frames[height.index(max(height))]
    else:
        skeleton = False

    return skeleton

def analyze_exercise(numpy_array, exercise_id, skeleton):
    ####################################
    # Basic Info
    # Params
    # numpy_array: 사람의 부위별 좌표를 포함한 리스트
    # exercise_id: exercise_list의 PK로 사용될 값
    # skeleton: 초기 자세가 들어있는 배열
    # How it works
    # numpy_array가 운동에 필요한 부위가 들어있는지 확인한다.
    # numpy_array에서 outlier를 제거한다.
    #
    # Return
    # (math_info)

    # Feature
    #

    # Todo
    # 보정이 들어간 것도 구해보면 좋을 듯
    ####################################
    test_res = Common.check_accuracy(numpy_array, exercise_id)

    if test_res[0] == True:
        result = Common.get_math_info(exercise_id, skeleton, numpy_array)
        return result
    else:
        print("This input file is not proper to use")
        return False, False

def train_exercise(ex_type, input_skeleton, input_vector, output_coordinates):
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

def feedback(user, trainer, ex_type):
    print("feedback processing....", end="")

    video = Video(trainer, user, "pullup", "increase", "round", 1)
    return True
