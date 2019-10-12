from pose_diff.util import Method, screen, bc_common
from pose_diff.interface import Screen, PoseDifference
from pose_diff.interface import get_result
import argparse
import numpy as np
import os
from pose_diff.core import run
import cv2

base_root_project_location = 'pose-difference'

def change_cwd():
    path = os.path.abspath(__file__)
    dirname = os.path.dirname(path)
    while os.path.split(dirname)[1] != base_root_project_location:
        dirname = os.path.dirname(dirname)
    os.chdir(dirname)

def main(option):
    change_cwd()
    parser = argparse.ArgumentParser(description='Pose Difference')
    parser.add_argument('--sys', type=int, default=0, help='Select System Operations')
    parser.add_argument('--type', type=int, default=0, help='Select System Operations')
    args = parser.parse_args()

    if args.sys == 1:
        Method.parse_person('video/user_init.mp4')
    elif args.sys == 2:
        type = ['trainer', 'user']
        selected = type[1]
        numpy = np.load('data/%s/exercise/raw/output_numpy/output.npy' % (selected,))
        (res1, res2) = Method.find_initial_skeleton(numpy, 'data/%s/exercise/exercise' % (selected,), 10)
        # print(res1, res2)
        # np.save('data/%s/init/init.npy' % (selected,), res1)
    elif args.sys == 3:
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

    elif args.sys == 4:
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

    elif args.sys == 5:
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

    elif args.sys == 6:
        video_name = 'data/result.avi'
        input1 = 'data/user/exercise/upgraded.npy'
        input2 = 'data/user/exercise/raw/output_numpy/output.npy'
        run.Video(input1, input2, video_name)

    elif args.sys == 7:
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

    elif args.sys == 10:
        PoseDifference.main_ui()


if __name__=="__main__":
    main(2)
