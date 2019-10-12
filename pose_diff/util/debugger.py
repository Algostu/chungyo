import os
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.cm as cm

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
# debug_live_multiple_line()
# Annotate with text

class Debugger():
    def debug_live_multiple_line(self, funct, data, title, labels, line_type):
        ######################
        # Need to Update *
        ######################
        if self.line_type == None:
            self.line_type = ['b-', 'g--', 'ro', 'y^']

    def animate_multiple(self, i):
        idx = 0
        for key, value in self.graph_data.items():
            vectors = list(zip(*value))
            column = idx % self.column
            ax = None
            ax = self.axes[column]
            ax.clear()
            if self.graph_type[idx] == 1:
                ax.plot(list(vectors[0]), list(vectors[1]), 'b-')
            else:
                colors = cm.rainbow(np.linspace(0, 1, len(vectors[1])))
                shape = np.linspace(0, 100, len(vectors[1]))
                ax.scatter(list(vectors[0]), list(vectors[1]), c = colors, s = shape)
            ax.set(title=key, xlabel = self.labels[idx][0], ylabel = self.labels[idx][1])
            idx +=1

    def animate(self, i):
        idx = 0
        ax = self.axes
        ax.clear()
        colors = cm.rainbow(np.linspace(0, 1, len(self.graph_data.keys())))
        for key, value in self.graph_data.items():
            vectors = list(zip(*value))
            shape = np.linspace(0, 100, 10)
            # ax.scatter(list(vectors[0][i:i+self.len]), list(vectors[1][i:i+self.len]), c = [colors[idx]], s = shape, label=key,
            #    alpha=0.3, edgecolors='none')
            ax.plot(vectors[0][i:i+self.len], vectors[1][i:i+self.len], label = key)
            ax.set(xlim=(min(vectors[0]), max(vectors[0])), ylim=(min(vectors[1]), max(vectors[1])))
            idx +=1
        ax.legend()
        ax.grid(True)

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
            self.labels = [('x%d Value' % (s+1,), 'y%d Value' % (s+1,)) for s in range(len(data))]

        if self.graph_type == None:
            self.graph_type = [2 for i in range(len(data))]

        style.use('fivethirtyeight')
        self.column = len(self.graph_data)
        self.row = 1
        self.fig, self.axes = plt.subplots(self.row, self.column)
        width = self.column * 3
        height = self.row * 8
        self.fig.set_size_inches(width, height)
        plt.suptitle(title)

        for func in list(funct):
            t= threading.Thread(target=func[0], args=func[1:])
            t.daemon=True
            t.start()

        ani = animation.FuncAnimation(self.fig, self.animate_multiple, interval=1000)
        plt.show()

    def debug_data_live(self, data, len, title='Data Analysis Live'):
        self.len = len
        self.graph_data = data
        style.use('fivethirtyeight')
        self.fig, self.axes = plt.subplots(1, 1)
        self.fig.set_size_inches(10, 7.5)
        plt.suptitle(title)
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()

# 여러점을 변화시킴
def make_line(data, test_opt=False):
    for i in range(10000):
        xs = np.random.randint(0, len(data), 10)
        for x in xs:
            data[x] = (x, x)
        if test_opt == True:
            time.sleep(0.5)

def debug_make_line(ex_type, set_num, joint_list):
    ##############################
    # Sample debug_live_multiple_plot Debugger Usage
    # Used for make_line
    # Params
    # ex_type : exercise number, int
    # set_num : set number, int
    # required_joints : target joints number list, recommend maximum 3, list
    ##############################
    sets = []
    ex_title, test_sets = Data.load_testSet(ex_type)
    idx = 0
    for test_set in test_sets:
        sets.append({})
        joints = list(zip(*test_set))
        for joint in joint_list:
            sets[idx][Common.PART_NAMES[joint]] = list(joints[joint])
        idx += 1

    fuct_with_args = [(make_line, data, True) for data in list(sets[set_num].values())]
    debug = Debugger()
    debug.debug_live_multiple_plot(fuct_with_args, sets[set_num], ex_title)

def debug_cal_blank(ex_type, set_num, joint_list):
    ##############################
    # Sample debug_live_multiple_plot Debugger Usage
    # Used for cal_blank
    # Params
    # ex_type : exercise number, int
    # set_num : set number, int
    # required_joints : target joints number list, recommend maximum 3, list
    ##############################
    sets = []
    ex_title, test_sets = Data.load_testSet(ex_type)
    idx = 0
    for test_set in test_sets:
        sets.append({})
        joints = list(zip(*test_set))
        for joint in joint_list:
            sets[idx][Common.PART_NAMES[joint]] = list(joints[joint])
        idx += 1

    fuct_with_args = [(Common.filter_outlier, data, 3, True) for data in list(sets[set_num].values())]
    debug = Debugger()
    debug.debug_live_multiple_plot(fuct_with_args, sets[set_num], ex_title)

def debug_data_live(ex_type, set_num, joint_list, len):
    ##############################
    # Sample debug_data_live Debugger Usage
    # Used for test data coordinates
    # Params
    # ex_type : exercise number, int
    # set_num : set number, int
    # joint_list : target joints number list, recommend maximum 3, list
    # len : tracking length, int
    ##############################
    sets = []
    ex_title, test_sets = Data.load_testSet(ex_type)
    idx = 0
    for test_set in test_sets:
        sets.append({})
        joints = list(zip(*test_set))
        for joint in joint_list:
            sets[idx][Common.PART_NAMES[joint]] = list(joints[joint])
        idx += 1
    debugger = Debugger()
    debugger.debug_data_live(sets[set_num], len)

if __name__=="__main__":
    # debug_data_live(4, 1, [1,2,3], 30)
    debug_make_line(3, 1, [1,2,3])
    # debug_cal_blank(3, 0, [0,1,2])
