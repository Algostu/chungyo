import os
import numpy as np
from pose_diff.core import run


def test_video():
    print("Testing run.video...")
    base_folder = 'pose_diff/Test/core/test_data2'
    # input1 = os.path.join(base_folder, 'upgraded.npy')
    # input2 = os.path.join(base_folder, 'exercise_numpy.npy')
    # video_name = os.path.join(base_folder, 'output.avi')
    # run.Video(input1, input2, video_name)
    graph_numpy = np.load(os.path.join(base_folder, 'graph.npy'))
    print(len(graph_numpy))

    print("Done")
