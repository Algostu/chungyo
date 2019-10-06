from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import sys, time, cv2, numpy as np

class ResultWindow(QWidget):
    def __init__(self, numpy, numpy_title, video1, video2, title, title2, title3):
        super().__init__()
        self.setWindowTitle("Pose Difference")
        self.titlemsg = title
        self.titlemsg2 = title2
        self.titlemsg3 = title3
        self.video1 = video1
        self.video2 = video2
        self.numpy = numpy
        self.numpy_title = numpy_title
        # top, left, width, height = 100, 50, 1300, 700
        self.setGeometry(25, 50, 640*2 + 600, 580)
        self.initUI()

    def initUI(self):
        self.cpt = cv2.VideoCapture(self.video1)
        self.cpt1 = cv2.VideoCapture(self.video2)
        self.fps = 24

        self.cnt = 0

        self.frame = QLabel(self)
        self.frame.resize(640, 480)
        self.frame.setScaledContents(True)
        self.frame.move(5,55)

        self.title = QLabel(self)
        self.title.resize(640,40)
        self.title.move(5, 5)
        self.title.setText(self.titlemsg)
        font = QFont()
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)

        self.frame2 = QLabel(self)
        self.frame2.resize(640, 480)
        self.frame2.setScaledContents(True)
        self.frame2.move(5+640+5, 55)

        self.title2 = QLabel(self)
        self.title2.resize(640,40)
        self.title2.move(5+640+5, 5)
        self.title2.setText(self.titlemsg2)
        font = QFont()
        font.setPointSize(20)
        self.title2.setFont(font)
        self.title2.setAlignment(Qt.AlignCenter)

        self.btn_on = QPushButton("시작", self)
        self.btn_on.resize(100, 25)
        self.btn_on.move(5, 540)
        self.btn_on.clicked.connect(self.start)

        self.btn_off = QPushButton("멈춤", self)
        self.btn_off.resize(100, 25)
        self.btn_off.move(5+100+5, 540)
        self.btn_off.clicked.connect(self.stop)

        self.prt = QLabel(self)
        self.prt.resize(200,25)
        self.prt.move(5+105+105, 540)

        self.sldr = QSlider(Qt.Horizontal, self)
        self.sldr.resize(100, 25)
        self.sldr.move(5+105+105+200, 540)
        self.sldr.setMinimum(1)
        self.sldr.setMaximum(60)
        self.sldr.setValue(24)
        self.sldr.valueChanged.connect(self.setFps)

        self.list = QListWidget(self)
        self.list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list.resize(570, 480)
        self.list.move(5+640*2+5+5, 55)

        self.title3 = QLabel(self)
        self.title3.resize(570,40)
        self.title3.move(5+640*2+5+5, 5)
        self.title3.setText(self.titlemsg3)
        font = QFont()
        font.setPointSize(20)
        self.title3.setFont(font)
        self.title3.setAlignment(Qt.AlignCenter)

        mcanvases = [FigureCanvas(Figure(figsize=(5, 3))) for i in range(len(self.numpy))]
        self.axes = []
        i = 0
        for mcanvase in mcanvases:
            itemN = QListWidgetItem()
            itemN.setSizeHint(QSize(500, 300))
            self.list.addItem(itemN)
            self.list.setItemWidget(itemN, mcanvase)
            self.axes.append(mcanvase.figure.subplots())
            self.axes[i].set(title = self.numpy_title[i])
            i += 1

        self._timer = mcanvases[0].new_timer(
            1000/self.fps, [(self._update_canvas, (), {})])

        self.show()

    def setFps(self):
        self.fps = self.sldr.value()
        self.prt.setText('fps가' +str(self.fps) + '로 변경되었습니다')
        self.timer.stop()
        self.timer.start(1000/self.fps)
        self._timer.stop()
        self._timer.start(1000/self.fps)

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 / self.fps)
        self._timer.start()

    def nextFrameSlot(self):
        if self.cpt.isOpened():
            _, cam = self.cpt.read()
            cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
            img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            self.frame.setPixmap(pix)
        if self.cpt1.isOpened():
            _, cam1 = self.cpt1.read()
            cam1 = cv2.cvtColor(cam1, cv2.COLOR_BGR2RGB)
            img = QImage(cam1, cam1.shape[1], cam1.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)
            self.frame2.setPixmap(pix)

    def stop(self):
        self.timer.stop()
        self._timer.stop()

    def _update_canvas(self):
        for i in range(len(self.axes)):
            self.axes[i].clear()
            self.axes[i].set(title = self.numpy_title[i])
            self.axes[i].plot(self.numpy[i][self.cnt:self.cnt+50])
            self.axes[i].figure.canvas.draw()
        self.cnt += 1

#############
def debugger(video='result.mp4', video2='result2.mp4', file_name=['result.npy'], plot_title = ['Test Graph', "Test Graph2", "Test Graph3"], title='비교 대상 1', title1 = '비교 대상 2', title2 = '그래프'):
    app = QApplication(sys.argv)
    # numpy_array = [np.load(name) for name in file_name]
    frames = np.load(file_name[0])
    joints = list(zip(*frames))
    xs1, ys, cs = list(zip(*joints[2]))
    xs2, ys, cs = list(zip(*joints[3]))
    xs3, ys, cs = list(zip(*joints[4]))
    numpy_array = [xs1, xs2, xs3]
    window = ResultWindow(numpy_array, plot_title, video, video2, title, title1, title2)
    window.show()
    app.exec()
    window.cpt.release()

if __name__ == "__main__":
    debugger()
