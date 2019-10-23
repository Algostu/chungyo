from pose_diff.util import Method, screen, bc_common
from pose_diff.interface import Screen, PoseDifference
from pose_diff.interface import get_result
from pose_diff.DB import DB
import argparse
import numpy as np
import os
from pose_diff.core import run
import cv2
import shutil
import time

def main_function(option, *args):
    base_folder = 'temp'
    if os.path.exists(base_folder):
        shutil.rmtree(base_folder)
    time.sleep(1)
    os.mkdir(base_folder)

    # args = (address_init, address_ex, user_id, exercise_id)
    if option == 1:
        # Usage - store blob data into table
        # file_naming - ./temp/column_name+적절한 확장자
        # Store file in temp
        # insert_input_list(1, 0, "./temp/init_numpy.py", "./temp/init_video.avi", "./temp/exercise_numpy.py", "./temp/exercise_video.avi")
        # delete temp folder

        # Usage - read blob data from table
        # make temp folder
        # readBlobData(1, 1, 'temp')
        print(args)

        input_init = args[0]
        input_exercise = args[1]
        output_init_numpy = os.path.join(base_folder, 'init_numpy.npy')
        output_init_video = os.path.join(base_folder, 'init_video.avi')
        output_ex_numpy = os.path.join(base_folder, 'exercise_numpy.npy')
        output_ex_video = os.path.join(base_folder, 'exercise_video.avi')

        Method.parse_person(input_init, output_init_numpy, output_init_video)
        Method.parse_person(input_exercise, output_ex_numpy, output_ex_video)

        DB.insert_input_list(args[2], args[3], output_init_numpy, output_init_video, output_ex_numpy, output_ex_video)

    elif option == 2:
        DB.read_from_input_list(args[0], base_folder)
        numpy = np.load(os.path.join(base_folder, 'init_numpy.npy'))
        skeleton_numpy = 'skeleon.npy'
        graph_numpy = 'graph.npy'
        (res1, res2) = Method.find_initial_skeleton(numpy, os.path.join(base_folder,graph_numpy), 10)
        # print(res1, res2)
        np.save(os.path.join(base_folder, skeleton_numpy), res1)
        DB.save_skeleton(args[0], os.path.join(base_folder,skeleton_numpy), os.path.join(base_folder,graph_numpy))
    
    elif option == 3:
        type = ['trainer', 'user']
        frame = [48, 22]
        selected = type[args.type]
        found = frame[args.type]
        input1 = 'data/%s/init/init.png' % (selected,)
        input2 = 'data/%s/init/raw/output_video/result.avi' % (selected,)
        file_names = ['data/%s/init/init_left_elbow.npy' % (selected,),
        'data/%s/init/init_right_elbow.npy' % (selected,),
        'data/%s/init/init_left_knee.npy' % (selected,),
        'data/%s/init/init_right_knee.npy' % (selected,)]
        plot_titles = ['left_elbow angle', "right_elbow angle", "left_knee angle", "right_knee angle"]

        get_result.debugger(found, isImage = True, video=input1, video2=input2,
        file_name=file_names,
        plot_title = plot_titles,
        title='%s initial pose' % (selected,), title1 = '%s video' % (selected,), title2 = 'graph data for main angle')

    elif option == 4:
        ex_type = 2
        numpy_array = np.load('data/trainer/exercise/raw/output_numpy/output.npy')
        skeleton = np.load('data/trainer/init/init.npy')
        target_skeleton = np.load('data/user/init/init.npy')

        common = bc_common.Common()
        accuracy, body_part = common.check_accuracy(numpy_array, 3, 0)
        input_vector = common.calculate_trainer(ex_type, skeleton, body_part[0], body_part[1])
        resized = common.apply_vector(ex_type, target_skeleton, input_vector)
        np.save('data/user/exercise/upgraded.npy', resized)
        # screen = run.human_pic(numpy_array,'data/user/exercise/original.avi')
        # screen = run.human_pic(resized,'data/user/exercise/upgraded.avi')

    elif option == 5:
        input2 = 'data/user/exercise/upgraded.avi'
        input1 = 'data/user/exercise/raw/output_video/result.avi'
        selected = 'trainer'
        file_names = ['data/%s/init/init_left_elbow.npy' % (selected,),
        'data/%s/init/init_right_elbow.npy' % (selected,),
        'data/%s/init/init_left_knee.npy' % (selected,),
        'data/%s/init/init_right_knee.npy' % (selected,)]
        plot_titles = ['left_elbow angle', "right_elbow angle", "left_knee angle", "right_knee angle"]

        get_result.debugger(0, isImage = False, video=input1, video2=input2,
        file_name=file_names,
        plot_title = plot_titles,
        title1='applied user exercise', title = 'original user exercise', title2 = 'graph data for main angle')

    # args = (input_id, sample_id)
    elif option == 6:
        video_name = os.path.join(base_folder, 'output.avi')
        DB.load_applied_skeleton_file(args[1], base_folder)
        DB.load_input_list(args[0], base_folder)
        input1 = os.path.join(base_folder, 'upgraded.npy')
        input2 = os.path.join(base_folder, 'exercise_numpy.npy')

        run.Video(input1, input2, video_name)

    elif option == 7:
        input2 = 'data/result.avi'
        input1 = 'data/user/exercise/raw/output_video/result.avi'
        selected = 'user'
        file_names = ['data/%s/exercise/exercise_left_elbow.npy' % (selected,),
        'data/%s/exercise/exercise_right_elbow.npy' % (selected,),
        'data/%s/exercise/exercise_left_knee.npy' % (selected,),
        'data/%s/exercise/exercise_right_knee.npy' % (selected,)]
        plot_titles = ['left_elbow angle', "right_elbow angle", "left_knee angle", "right_knee angle"]

        get_result.debugger(0, isImage = False, video=input1, video2=input2,
        file_name=file_names,
        plot_title = plot_titles,
        title1='pose difference algorithm', title = 'original user exercise', title2 = 'graph data for main angle')

    elif option == 10:
        PoseDifference.main_ui()
