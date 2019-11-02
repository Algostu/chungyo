import numpy as np
import matplotlib.pyplot as plt
from pose_diff.util import Method

def test_find_initial_skeleton():
    numpy_array_1 = np.load('pose_diff/Test/util/test_data/init_numpy_1.npy')
    numpy_array_2 = np.load('pose_diff/Test/util/test_data/init_numpy_2.npy')
    stilness = 10
    Method.find_initial_skeleton(numpy_array_1, 'pose_diff/Test/util/test_result/graph.npy', stilness)
    result = np.load('pose_diff/Test/util/test_result/graph.npy')
    print(result)
    stilness_list = result[0]
    height_list = result[1]
    
    f, (ax1, ax2) = plt.subplots(2, 1)
    f.tight_layout()
    ax1.plot(stilness_list, 'b',label ='stilness')
    ax2.plot(height_list, 'g-', label ='height')
    ax1.set_title('stillness')
    ax2.set_title('height')
    ax1.axhline(y=stilness, c='r', ls='--')
    ax1.legend()
    plt.show()
