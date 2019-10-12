############################################
# Basic Info
# UI

# Feature
# 1. Register Trainer
# 2. Tell Difference between Two Videos
# 3. Analysis Physical Data and Tell Difference between Two Videos

# Todo
# Replace console to pyqt5
# Add senario for advanced Usage
############################################
from pose_diff.DB import DB
from pose_diff.interface import PoseSystem
import os
import traceback

def main_ui():
    ####################################
    # Basic Info
    # 처음 시작 UI

    # Feature
    # 3가지의 시나리오를 분리합니다.

    # Todo
    # Scene no.2, no.3 완성
    # Advanced Usage를 위한 경우를 마련해야 합니다.
    ####################################
    print("""
    ==================================================================
    CHOOSE WHAT SCENARIO YOU WANT TO USE
    1. Register Trainer
    2. Get Advice about Exercise Captured from Video
    3. Analyze Physical Data and Get Advice from it
    ------------------------------------------------------------------
    FOR DEVELOPERS
    4. Initialize DataBase (Init data folder in project root directory)
    ==================================================================
    """)

    main_option = int(input("Enter: "))

    if main_option == 1:
        trainer_ui()
    elif main_option == 2:
        diff_videos_ui()
    elif main_option == 3:
        physical_ui()
    elif main_option == 4:
        DB.initialize()

def physical_ui():
    indent = " "*4

    # (exercise_name)
    # (applied_sample_id, exercise_id, sample_location, user_name, applied_sample_location, trainer_name)
    exercise_list = DB.get_exercise_names()
    applied_samples = DB.load_applied_skeleton_list()
    print(exercise_list)
    print("""
    ==================================================================
    CHOOSE EXERCISE DATA WHERE YOU WANT TO GET REPORT(USER)""")
    for idx, row in enumerate(applied_samples):
        print(indent+"%d. %s: %s by %s" % (idx+1, exercise_list[row[1]-1][0], row[3], row[5]))
    print(indent+"""==================================================================
    """)

    option = int(input("Enter: "))
    args = applied_samples[option]

    ret_val = PoseSystem.Analyze_Physical_Data(*args)
    if ret_val == True:
        print("""
    ==================================================================
    END OF ANALYZE PHYSICAL DATA PROCESS
    RESULT : SUCCESS
    ==================================================================
        """)
    else:
        print("""
    ==================================================================
    END OF ANALYZE PHYSICAL DATA PROCESS
    RESULT : FAIL
    ==================================================================
        """)
    return


def diff_videos_ui():
    ####################################
    # Basic Info
    # Scene No.2 유저가 비디오 분석을 받기 위한 UI이다.
    # Console Based UI가 기본이고 INPUT에 대한 exception을 처리한다.

    # Feature
    # 유저로부터 Input을 받고 적절한 함수를 호출합니다.

    # Todo
    # 결과창 띄우기 (A+)
    # 비디오 분석 건너 뛰기 옵션 적용 (A)
    # Video 조건 영어로 번역
    ####################################
    # For Print Format
    indent = " "*4

    # Get the number of math_info for exercise
    exercise_list = DB.get_exercise_list()
    for idx, exercise in enumerate(exercise_list):
        exercise_list[idx] = list(exercise) + [len(DB.get_math_info_list_per_exercise(exercise[0]))]

    # Select Exercise
    print("""
    ==================================================================
    CHOOSE WHICH EXERCISE YOU WANT TO GET ADVICE FOR""")
    for idx, row in enumerate(exercise_list):
            print(indent+"%d. %s [%d]" % (idx+1, row[1], row[2]))
    print(indent+"""==================================================================
    """)

    option = int(input("Enter: "))
    if exercise_list[option-1][2] == 0:
        print("""
    ==================================================================
    END OF GET ADVICE PROCESS
    RESULT : FAIL
    ERROR : Select Exercise Which Trainer Registered Before
    ==================================================================
        """)
        return

    exercise_id = exercise_list[option-1][0]

    # Select Math Info
    rows = DB.get_math_info_list_per_exercise(exercise_id)
    print("""
    ==================================================================
    CHOOSE TRAINER WHO YOU WANT TO GET ADVICE FROM""")
    for idx, row in enumerate(rows):
        print(indent+"%d. %s: %s" % (idx+1, row[3], row[2]))
    print(indent+"""==================================================================
    """)

    option = int(input("Enter: "))
    standard_id = rows[option-1][0]

    print("""
    ==================================================================
    ENTER LOCATION OF INPUT VIDEO FILE (PLEASE CHECK VIDEO CONDITION)
    1. Stand Upright Still at Least 1 Sec
    2. 카메라로부터 운동하는 사람과의 거리는 해당 사람이 똑바로 서있을때와 동일해야 합니다.
    3. The Maximum number of people in Video is 1
    4. Cam should not Move
    ==================================================================
    """)

    input_video_loc = input("Enter (relative path): ")
    ret_val = False
    try:
        if os.path.exists(input_video_loc):
            ret_val = PoseSystem.get_feedback(standard_id, exercise_id, input_video_loc)
        else:
            raise Exception()
    except Exception:
        traceback.print_exc()
        return

    if ret_val == True:
        print("""
    ==================================================================
    END OF GET ADVICE PROCESS
    RESULT : SUCCESS
    ==================================================================
        """)
    else:
        print("""
    ==================================================================
    END OF GET ADVICE PROCESS
    RESULT : FAIL
    ==================================================================
        """)
    return

def trainer_ui():
    ####################################
    # Basic Info
    # Scene No.1 트레이너 등록을 위한 UI 이다.
    # Console Based UI가 기본이고 INPUT에 대한 exception을 처리한다.

    # Feature
    # 유저로부터 Input을 받고 적절한 함수를 호출합니다.

    # Todo
    # 결과창 띄우기 (A+)
    # 비디오 분석을 건너뛰고 등록된 sample을 이용할 수 있는 옵션 추가(A)
    # Exercise 추가 기능 (B)
    # Video 조건 영어로 번역 (A)
    ####################################
    # For Print Format
    indent = " "*4

    # Select Exercise
    rows = DB.get_user_list('standard')
    rows.append([])
    print("""
    ==================================================================
    CHOOSE WHICH TRAINER YOU WANT TO REGISTER EXERCISE FOR""")
    for idx, row in enumerate(rows):
        if idx != len(rows)-1:
            print(indent+"%d. %s" % (idx+1, row[1]))
        else:
            print(indent+"%d. Register New Trainer" % (idx+1,))
    print(indent+"""==================================================================
    """)

    option = int(input("Enter: "))

    # Get PK for table of user_list
    trainer_id = 0
    if option == len(rows):
        print("""
        ==================================================================
        Register New Trainer
        1. Name (English)
        2. Weight (kg)
        3. Stature (cm)
        4. Other Info
        5. Sex (men or women)
        ==================================================================
        """)
        # Regist New Trainer
        register_form = ['standard']
        try:
            register_form.append(input("Enter Name: "))
            register_form.append(int(input("Enter Weight(kg): ")))
            register_form.append(int(input("Enter Height(cm): ")))
            register_form.append(input("Enter Other Info: "))
            register_form.append(input("Enter Sex: "))
            if register_form[5] not in ('men', 'women', ''):
                raise Exception()
        except ValueError:
            print('Please enter an integer')
            return
        except Exception:
            print("Please enter men or women for your sex")
            return

        trainer_id = DB.create_user(*register_form)
    else:
        trainer_id = rows[option-1][0]

    # Get the number of Exercise for trainer
    exercise_list = DB.get_exercise_list()
    for idx, exercise in enumerate(exercise_list):
        exercise_list[idx] = list(exercise) + [len(DB.get_registered_exercise_for_one_user(trainer_id, exercise[0]))]

    # Select Exercise Type
    print("""
    ==================================================================
    CHOOSE WHICH EXERCISE YOU WANT TO REGISTER EXERCISE FOR""")
    for idx, row in enumerate(exercise_list):
            print(indent+"%d. %s [%d]" % (idx+1, row[1], row[2]))
    print(indent+"""==================================================================
    """)

    option = int(input("Enter: "))
    exercise_id = exercise_list[option-1][0]

    print("""
    ==================================================================
    ENTER LOCATION OF INPUT VIDEO FILE (PLEASE CHECK VIDEO CONDITION)
    1. Stand Upright Still at Least 1 Sec
    2. 카메라로부터 운동하는 사람과의 거리는 해당 사람이 똑바로 서있을때와 동일해야 합니다.
    3. The Maximum number of people in Video is 1
    4. Cam should not Move
    ==================================================================
    """)

    input_video_loc = input("Enter (relative path): ")
    ret_val = False
    try:
        if os.path.exists(input_video_loc):
            ret_val = PoseSystem.regist_trainer(trainer_id, exercise_id, input_video_loc)
        else:
            raise Exception()
    except Exception:
        traceback.print_exc()
        return

    if ret_val == True:
        print("""
        ==================================================================
        END OF TRAINER REGISTER PROCESS
        RESULT : SUCCESS
        ==================================================================
        """)
    else:
        print("""
        ==================================================================
        END OF TRAINER REGISTER PROCESS
        RESULT : FAIL
        ==================================================================
        """)
    return
