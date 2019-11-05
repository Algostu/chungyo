import os

import matplotlib.pyplot as plt
import numpy as np
from pose_diff.core import run
# from pose_diff.core import save_docx
from pose_diff.core.report import insert_image_and_pictures


def test_video(option=1):
    '''
    Test result of graph.npy
    '''
    print("Testing run.video...")
    base_folder = 'pose_diff/Test/core/test_data2'
    if option == 2:
        base_folder = 'temp'
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

def test_video2():
    '''
    Test result of video

    Todo
        1. cutframes의 개수가 75보다 낮은 것들은 작동하지 않는다. 따라서 제외한다. 왜 작동하지 않는지도 알아내야 한다.
        2. 에러값을 주면 오류가 난다. 원인: run.py score_angle부분에서 에러가 발생한다.
    '''
    #
    # base_folder = 'pose_diff/Test/core/test_data2'
    # input1 = os.path.join(base_folder, 'standard_trainer.npy')
    # input2 = os.path.join(base_folder, 'standard_trainer.npy')
    # video_name = os.path.join(base_folder, 'standard_video.avi')
    # run.Video(input1, input2, video_name)

    base_folder = 'pose_diff/Test/core/test_data2'
    graph_numpy = np.load(os.path.join(base_folder, 'graph.npy'))
    recollected_frames = graph_numpy[-1]
    # print(recollected_frames)
    # print('length of video: %d' % len(recollected_frames))
    for idx, part in enumerate(recollected_frames[3:4]):
        # print('%d: %d' % (idx, len(part)))
        input1 = os.path.join(base_folder, 'standard_trainer.npy')
        input2 = os.path.join(base_folder, 'standard_user.npy')

        video_name = os.path.join(base_folder, 'standard_video.avi')
        # for error user
        part2 = np.copy(part)
        for frame in part2:
            alpha = 1
            errors = alpha * np.random.randn(18,2)
            for partt, error in zip(frame, errors):
                partt[0] += round(error[0],2)
                partt[1] += round(error[1],2)

        np.save(input1, part)
        np.save(input2, part2)
        run.Video(input1, input2, video_name)
        test_video(2)

def test_save_docx():
    '''
    Save document

    Todo
        1. Start html to PDF...Done
        2. Start html redering using beautify...Done
    '''
    print("save_docx testing...")
    insert_image_and_pictures()
    print("Done")
