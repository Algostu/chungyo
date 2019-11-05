############################################
# Basic Info
# Logical part of PoseDifference
# 각 시나리오별로 필요한 함수들을 호출한다.

# Feature
# 1. Register Trainer
# 2. Tell Difference between Two Videos
# 3. Analysis Physical Data and Tell Difference between Two Videos

# Todo
#
############################################
import os
import random
import string

import numpy as np
from pose_diff.DB import DB
from pose_diff.util import Method


def regist_trainer(trainer_id, exercise_id, input_video_loc):
    # openpose를 통해서 분석
    result_numpy = Method.parse_person(input_video_loc)

    # 초기자세를 분석
    skeleton = Method.find_initial_skeleton(result_numpy)

    # 초기에 서 있는 자세를 찾을 수 없는 경우
    if skeleton == False:
        print("Error: Couldn't find initial pose. Find another one")
        return False

    # 보정 및 운동 분석
    math_info = Method.analyze_exercise(result_numpy, exercise_id, skeleton)

    # Issue: 운동 분석을 통한 보정 결과물도 얻을 수 있도록 수정
    # if sample_numpy == False:
    #     print("Error: You can't use it")
    #     return False
    if math_info == False:
        print("Error: ") # Issue: math_info Extraction 오류 잡기
        return False

    # 파일이름으로 사용할 값 생성
    file_name = id_generator() + '.npy'

    # Store
    sample_id = DB.save_sample(trainer_id, sample_numpy, file_name, exercise_id)
    skeleton_id = DB.save_skeleton(trainer_id, skeleton, file_name)
    math_info_names = [os.path.split(file_name)[0]+str(i)+os.path.split(file_name)[1] for i in range(len(math_info))]
    extraction_id = DB.save_math_info_extraction(skeleton_id, exercise_id, sample_id, math_info, math_info_names)

    return True

def get_feedback(standard_id, exercise_id, input_video_loc):
    # openpose를 통해서 분석
    result_numpy = Method.parse_person(input_video_loc)

    # 초기자세를 분석
    skeleton = Method.find_initial_skeleton(result_numpy)

    # 초기에 서 있는 자세를 찾을 수 없는 경우
    if skeleton == False:
        print("Error: Couldn't find initial pose. Find another one")
        return False

    # Load Math_info extraction info
    rows = DB.get_math_info(extraction_id)
    vectors = np.load(rows[0])

    # Resizing
    resized_numpy = Method.resize(exercise_id, skeleton, vectors)

    # Issue : 운동 분석을 통한 보정
    # sample, math_info = Method.analyze_exercise(result_numpy, exercise_id, skeleton)
    # Issue: 운동 분석을 통한 보정 결과물도 얻을 수 있도록 수정
    # if sample_numpy == False:
    #     print("Error: You can't use it")
    #     return False

    # 파일이름으로 사용할 값 생성
    file_name = id_generator() + '.npy'

    # Issue: Store 구현

    return True

def get_real_time_feedback():
    pass

def get_physical_report(applied_sample_id, exercise_id, sample_location, user_name, applied_sample_location, trainer_name):
    file_name = id_generator() + '.docx'
    user_numpy = np.load(sample_location)
    trainer_numpy = np.load(applied_sample_location)
    Method.analyze_physical(file_name, exercise_id, user_numpy, trainer_numpy, user_name, trainer_name)

    return True
def id_generator(size = 10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
