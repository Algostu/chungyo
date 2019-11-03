import os
import numpy as np
import matplotlib.pyplot as plt
from pose_diff.core import run


def test_video():
    print("Testing run.video...")
    base_folder = 'pose_diff/Test/core/test_data2'
    # input1 = os.path.join(base_folder, 'upgraded.npy')
    # input2 = os.path.join(base_folder, 'exercise_numpy.npy')
    # video_name = os.path.join(base_folder, 'output.avi')
    # run.Video(input1, input2, video_name)

    # score
    graph_numpy = np.load(os.path.join(base_folder, 'graph.npy'))
    score_numpy = graph_numpy[0]
    average_score = sum(score_numpy) / len(score_numpy)

    plt.plot(score_numpy)
    plt.ylim([0, 100])
    plt.axhline(y = average_score, c='r', ls='--', label='avergae score: %d' % average_score)
    plt.legend()
    plt.show()

    # graph
    gap_numpy = graph_numpy[1:7]
    f, axes = plt.subplots(3, 2, figsize=(10,10))
    plain_axes = list(zip(*axes))[0] + list(zip(*axes))[1]

    titles = ['left_shoulder', 'left_elbow', 'left_wrist', 'right_shoulder', 'right_elbow', 'right_wrist']
    f.tight_layout()
    for ax, gap, title in zip(plain_axes, gap_numpy, titles):
        xs, ys = list(zip(*gap))[0], list(zip(*gap))[1]
        x_max = max([abs(x) for x in xs])
        y_max = max([abs(y)for y in ys])
        ax.scatter(xs, ys)
        ax.set_xlim([-x_max, x_max])
        ax.set_ylim([-y_max, y_max])
        ax.grid(True)
        ax.axhline(y=0, c='black', ls='--')
        ax.axvline(x=0, c='black', ls='--')
        ax.set_title(title)
    plt.show()

    print("Done")
