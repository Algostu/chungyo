import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from pose_diff.util import Method

def test_find_initial_skeleton():
    numpy_array_1 = np.load('pose_diff/Test/util/test_data/init_numpy_1.npy')
    numpy_array_2 = np.load('pose_diff/Test/util/test_data/init_numpy_2.npy')
    stilness = 10
    Method.find_initial_skeleton(numpy_array_1, 'pose_diff/Test/util/test_result/graph.npy', stilness)
    Method.find_initial_skeleton(numpy_array_2, 'pose_diff/Test/util/test_result/graph2.npy', stilness)
    result = [
    np.load('pose_diff/Test/util/test_result/graph.npy'),
    np.load('pose_diff/Test/util/test_result/graph2.npy')
    ]
    for i in range(2):
        stilness_list = result[i][0]
        height_list = result[i][1]
        max_frame_num = 0
        max_height = 0
        for i in range(len(stilness_list)):
            if stilness_list[i] > stilness:
                if max_height < height_list[i]:
                    max_frame_num = i
                    max_height = height_list[i]

        f, (ax1, ax2) = plt.subplots(2, 1)
        f.tight_layout()
        ax1.plot(stilness_list, 'b',label ='stilness')
        ax2.plot(height_list, 'g-', label ='height')
        ax1.set_title('stillness')
        ax2.set_title('height')
        ax2.annotate('max height: %d' % max_frame_num, xy=(max_frame_num, max_height), xytext=(max_frame_num-10, max_height+5),
                    arrowprops=dict(facecolor='black', shrink=0.05))
        ax1.axhline(y=stilness, c='r', ls='--')
        ax1.legend()
        cursor = Cursor(ax1, useblit=True, color='red', linewidth=2)
        plt.show()
