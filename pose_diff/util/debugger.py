import os
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

from pprint import pprint as pp
# from pose_diff.util import Common, Data
import Common, Data

# Function Explanation
#
# 2D plot, scatter 방식으로 그래프를 그린다.
#
# plot은 그래프의 선의 종류와 색깔을 정한다.
# scatter 방식은 점의 크기와 색깔을 정한다.

# Todo
# animate_multiple()
# debug_live_multiple_line()
# debug_live_multiple_plot()
# test_function_1()
# 여러점의 움직임을 본다.

class Debugger():
    def animate_multiple(self, i):
        print(i)
        for idx, value in enumerate(list(self.graph_data.values())):
            vectors = list(zip(*value))
            row = idx // self.column
            column = idx % self.column
            if self.row > 1:
                self.axes[row][column].clear()
                self.axes[row][column].plot(list(vectors[0])[i:i+20], list(vectors[1])[i:i+20], 'b-')
            else :
                self.axes[column].clear()
                self.axes[column].plot(list(vectors[0])[i:i+20], list(vectors[1])[i:i+20], 'b-')
            # Todo : plot_title, labels, graph_type, line_type

    def debug_live_multiple_line(self, funct, data, title, labels, line_type):
        if self.line_type == None:
            self.line_type = ['b-', 'g--', 'ro', 'y^']

    def debug_live_multiple_plot(self, funct, data, title=None, labels=None, graph_type=None):

        # Parameter
        #
        # funct : ((functionName, *args)*N)
        # data : live로 표시되어야될 데이터, plot title을 위해서 dict형태로 받는다.
        # labels : xlabel, ylabel에 대한 정보를 받는다. 단위 기입 필수 default = [('x Value %s' % (s,), 'y Value %d' % (s,)) for s in range(len(data))]
        # graph_type : plot = 1, scatter = 2, default = 1
        # line_type : ['color', 'shape'] * max_line_num, default = ['b-', 'g--', 'ro', 'y^']

        self.graph_data = data
        self.labels = labels
        self.graph_type = graph_type

        if title == None:
            title = 'debug graph'

        if self.labels == None:
            lebels = [('x%d Value' % (s,), 'y%d Value' % (s,)) for s in range(len(data))]

        if self.graph_type == None:
            self.graph_type = [1 for i in range(len(data))]

        style.use('fivethirtyeight')
        self.column = 5
        self.row = len(list(self.graph_data.keys())) // self.column + 1
        self.fig, self.axes = plt.subplots(self.row, self.column)
        width = self.column * 3
        height = self.row * 4
        self.fig.set_size_inches(width, height)
        plt.suptitle(title)
        plt.tight_layout()

        for func in list(funct):
            t= threading.Thread(target=func[0], args=func[1:])
            t.daemon=True
            t.start()

        ani = animation.FuncAnimation(self.fig, self.animate_multiple, interval=1000)
        plt.show()

# 여러점을 변화시킴
def test_function_1(data, test_opt=False):
    for i in range(10000):
        if test_opt == True:
            time.sleep(1)

if __name__ == "__main__":
    sets = []
    test_sets = Data.load_testSet(4)
    for test_set in test_sets:
        sets.append({str(idx) : list(value) for idx, value in enumerate(list(zip(*test_set))[:-15])})

    fuct_with_args = [(test_function_1, data, True) for data in list(sets[0].values())]
    debug = Debugger()
    debug.debug_live_multiple_plot(fuct_with_args, sets[0], "Squat")
