'''
* Writer : hankyul
* Last updated : 2019-08-19
* About what : parse options and delegate user operation to right modules
* contens : function -> main
'''
import argparse
import os
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt

from m_han.parse import parse_sequence, load_ps
from m_han.evaluate import evaluate_pose

# get option list from user, and pass them to proper modules
def main():
    parser = argparse.ArgumentParser(description='Pose Difference')
    parser.add_argument('--mode', type=str, default='check', help='Pose Difference application mode')
    # parser.add_argument('--display', type=int, default=1, help='display openpose video')
    parser.add_argument('--input_folder', type=str, default='videos', help='input folder for videos')
    parser.add_argument('--output_folder', type=str, default='poses', help='output folder for pose JSON')
    parser.add_argument('--video', type=str, help='input video filepath for evaluation')
    parser.add_argument('--file', type=str, help='input npy file for evaluation')
    parser.add_argument('--exercise', type=str, default='bicep_curl', help='exercise type to evaluate')

    args = parser.parse_args()


    if args.mode == 'check':
        import tf_pose
        print('Hello Pose Difference')

    # parse every video in input_folder and store .json files into out_folder by video names
    elif args.mode == 'batch_json':
        print("If you want to use batch_json option, you should install openpose yourself")
        # read filenames from the videos directory
        videos = os.listdir(args.input_folder)

        # openpose requires running from its directory
        os.chdir('openpose')

        for video in videos:
            print('processing video file:' + video)
            video_path = os.path.join('..', args.input_folder, video)
            output_path = os.path.join('..', args.output_folder, os.path.splitext(video)[0])
            openpose_path = os.path.join('bin', 'OpenPoseDemo.exe')
            subprocess.call([openpose_path,
                            '--video', video_path,
                            '--write_keypoint_json', output_path])

    # videoName.avi -> input video file
    # videoName/*.json -> output json filenames
    # videoname.npy -> output numpy
    elif args.mode == 'evaluate':
        if args.video:
            print('processing video file...')
            video = os.path.basename(args.video)

            output_path = os.path.join('..', os.path.splitext(video)[0])
            openpose_path = os.path.join('bin', 'OpenPoseDemo.exe')
            os.chdir('openpose')
            subprocess.call([openpose_path,
                            '--video', os.path.join('..', args.video),
                            '--write_keypoint_json', output_path])
            parse_sequence(output_path, '..')
            pose_seq = load_ps(os.path.join('..', os.path.splitext(video)[0] + '.npy'))
            (correct, feedback) = evaluate_pose(pose_seq, args.exercise)
            if correct:
                print('Exercise performed correctly!')
            else:
                print('Exercise could be improved:')
            print(feedback)
        else:
            print('No video file specified.')
            return

    # using file flags
    # numpyFileName.npy -> input
    elif args.mode == 'evaluate_npy':
        if args.file:
            pose_seq = load_ps(args.file)
            (correct, feedback) = evaluate_pose(pose_seq, args.exercise)
            if correct:
                print('Exercise performed correctly:')
            else:
                print('Exercise could be improved:')
            print(feedback)
        else:
            print('No npy file specified.')
            return

    elif args.mode == 'm_da':
        from m_da.main import main
        main()

    elif args.mode == 'm_byung':
        from m_byung.main import main
        main()

    elif args.mode == 'm_seung':
        from m_seung.main import main
        main()

    else:
        print('Unrecognized mode option.')
        return


if __name__ == "__main__":
    main()
