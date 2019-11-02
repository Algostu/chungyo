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
import matplotlib.pyplot as plt
from pose_diff.util import Common
from pose_diff.core.run import Video

def parse_person(input_video_loc, output_numpy, output_video):
    """
    Parse Video Using OpenPose
    """
    os.chdir('openpose')
    openpose_path = os.path.join('bin', 'OpenPoseDemo.exe')
    model = 'COCO'
    parsing_objects = '--video'
    output_path = 'output_json'

    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    time.sleep(1)

    os.mkdir(output_path)

    subprocess.call([openpose_path, # Issue : Output is only json
                    '--model_pose', model,
                    parsing_objects, os.path.join('..',input_video_loc),
                    '--output_resolution', '1280x720',
                    '--write_video', os.path.join('..',output_video),
                    '--number_people_max', '1',
                    '--write_json', output_path])

    # Read json file and Make Numpy Array
    json_files = glob.glob(os.path.join('output_json/', '*.json'))
    json_files = sorted(json_files)

    num_frames = len(json_files)

    all_keypoints = np.zeros((num_frames, 18, 3))
    for i in range(num_frames):
        with open(json_files[i]) as f:
            json_obj = json.load(f)
            keypoints = np.array(json_obj['people'][0]['pose_keypoints_2d'])
            all_keypoints[i] = keypoints.reshape((18, 3))

    np.save(os.path.join('..',output_numpy), all_keypoints)
    os.chdir('..')

def find_initial_skeleton(numpy_array, name, stilness=15):
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
    # np.save(name, [left_elbow, right_elbow, left_knee, right_knee])
    # Find 정지된 자세
    stop_len = stilness # 정지된 상태로 있어야 하는 시간이다. (단위는 프레임)
    stop_i = 0 # 정지된 상태가 지속된 시간이다.
    height = [] # 정지된 상태에서 측정된 키의 리스트이다.
    frames = [] # 정지된 상태에서의 프레임이다.
    frames_num = []

    stillness_list = []
    all_heigth_list = []
    i = 0
    for frame, l_e, r_e, l_k, r_k in zip(numpy_array, left_elbow, right_elbow, left_knee, right_knee):
        stillness_list.append(stop_i)
        all_heigth_list.append(Common.get_body_len(frame))
        if (170 < l_e < 190) and (170 < r_e < 190) and (170 < l_k < 190) and (170 < r_k < 190):
            stop_i += 1
        else:
            stop_i = 0

        if stop_i >= stop_len:
            frames_num.append(i)
            height.append(Common.get_body_len(frame))
            frames.append(frame)
        i += 1
    np.save(name, [stillness_list, all_heigth_list])
    # Initial Pose를 찾을 수 없을 경우 False를 Return 한다.
    if len(height) != 0:
        skeleton = frames[height.index(max(height))]
        frame_num = frames_num[height.index(max(height))]
    else:
        skeleton = False
        frame_num = -1

    return skeleton, frame_num

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
        return False

def resize(ex_type, input_skeleton, input_vector):
    length = input_skeleton
    vector = input_vector
    res = Common.apply_vector(ex_type, length, vector)
    return res

def feedback(user, trainer, ex_type):
    video = Video(trainer, user, 3)
    return True

def analyze_physical(file_name, exercise_id, user_numpy, trainer_numpy, user_name, trainer_name):
    pass
