import sys
import cv2
import shutil
import os
import time
import sqlite3
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

from pose_diff.DB import DB
from pose_diff.core import run
from function_main import main_function

signin = uic.loadUiType("ui/signin.ui")[0]
signup = uic.loadUiType("ui/signup.ui")[0]
start = uic.loadUiType("ui/start.ui")[0]
upload_video = uic.loadUiType("ui/upload_video.ui")[0]
register_trainer = uic.loadUiType("ui/register_trainer.ui")[0]
find_initial_pose = uic.loadUiType("ui/find_initial_pose.ui")[0]
register_trainer_better = uic.loadUiType("ui/register_trainer_better.ui")[0]
make_trainer = uic.loadUiType("ui/make_trainer.ui")[0]
resize_trainer = uic.loadUiType("ui/resize_trainer.ui")[0]
analyze_guide = uic.loadUiType("ui/analyze_guide.ui")[0]
store = uic.loadUiType("ui/store.ui")[0]
report = uic.loadUiType("ui/report.ui")[0]
moreinfo = uic.loadUiType("ui/moreinfo.ui")[0]
loading = uic.loadUiType("ui/loading.ui")[0]
success = uic.loadUiType("ui/success.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, signin) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.signup.clicked.connect(self.PopupSignUp)
        self.login.clicked.connect(self.Login)
        self.password.returnPressed.connect(self.Login)

    def Login(self):
        conn = sqlite3.connect('./pose_diff/DB/pose_diff.db')
        c = conn.cursor()
        input_id = self.username.text()
        input_pw = self.password.text()
        c.execute('SELECT user_id, user_name, user_type from user_list where user_name=? and password=?', (input_id,input_pw))
        rows = c.fetchone()
        conn.commit()
        conn.close()

        if rows != None:
            self.window = WindowStart(rows)
            self.close()

        else:
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    def PopupSignUp(self):
        self.window = WindowSignUp()
        self.window.show()

# UC 1
class WindowUploadVideo(QMainWindow, upload_video):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(26)
        self.user_id = user_id
        self.comboBox.clear()
        for name in DB.get_exercise_names():
            self.comboBox.addItems(name)
        self.show()
        self.connectFunction()

    def connectFunction(self):
        self.upload.clicked.connect(self.Upload)
        self.browse_init.clicked.connect(lambda: self.openFileDialog(0))
        self.browse_ex.clicked.connect(lambda: self.openFileDialog(1))

    def Upload(self):
        if self.address_init.toPlainText() == "" and self.address_ex.toPlainText()=="":
            QMessageBox.warning(
                self, 'Error', "You should select file or Enter Video Info")
        else:
            args = (
            self.address_init.toPlainText(),
            self.address_ex.toPlainText(),
            self.user_id,
            self.comboBox.currentIndex() + 1
            )
            main_function(1, *args)
            self.close()

    def openFileDialog(self, x):
        fname = QFileDialog.getOpenFileName(self)
        if x == 0:
            self.address_init.setText(str(fname[0]))
        else:
            self.address_ex.setText(str(fname[0]))

# UC 2
class WindowReigsterTrainerBetter(QMainWindow, register_trainer_better):
    def __init__(self, skeleton_id, input_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.skeleton_id = skeleton_id
        self.input_id = input_id
        self.connectFunction()
        args = (self.skeleton_id, self.input_id)
        main_function(3, *args)
        self.graph()
        self.Video()

    def graph(self):
        self.graph_title = ['left_elbow', 'right_elbow', 'left_knee', 'right_knee']
        self.graph_list.setFlow(QListWidget.LeftToRight)
        self.graph_list.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.numpy = np.load('temp/graph.npy')
        mcanvases = [FigureCanvas(Figure(figsize=(5, 3))) for i in range(len(self.numpy))]
        self.axes = []
        for idx, mcanvase in enumerate(mcanvases):
            itemN = QListWidgetItem()
            itemN.setSizeHint(QSize(380, 380))
            self.graph_list.addItem(itemN)
            self.graph_list.setItemWidget(itemN, mcanvase)
            self.axes.append(mcanvase.figure.subplots())
            self.axes[idx].set(title = self.graph_title[idx])

    def Video(self):
        self.origin_label.setScaledContents(True)
        self.copy_label.setScaledContents(True)
        self.cpt = cv2.VideoCapture('temp/exercise_video.avi')
        self.cpt2 = cv2.VideoCapture('temp/math_info.avi')
        self.frequency = 0.3
        self.cnt = 0
        self.start()

    def start(self):
        cam = 1
        cam2 = 1
        index = 0
        while self.cpt.isOpened() and cam is not None and cam2 is not None:
            # Video
            _, cam = self.cpt.read()
            _, cam2 = self.cpt2.read()
            if cam is not None and cam2 is not None:
                cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
                cam2 = cv2.cvtColor(cam2, cv2.COLOR_BGR2RGB)
                img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
                img2 = QImage(cam2, cam2.shape[1], cam2.shape[0], QImage.Format_RGB888)
                pix = QPixmap.fromImage(img)
                pix2 = QPixmap.fromImage(img2)
                self.origin_label.setPixmap(pix)
                self.copy_label.setPixmap(pix2)

                cv2.waitKey(100)

            # graph
            for i in range(len(self.axes)):
                self.axes[i].clear()
                self.axes[i].set(title = self.graph_title[i], )
                if index < 50:
                    self.axes[i].plot(self.numpy[i][0:index])
                else:
                    self.axes[i].plot(self.numpy[i][index - 50:index])
                self.axes[i].figure.canvas.draw()

            index += 1
        self.cpt.release()
        self.cpt2.release()

    def connectFunction(self):
        self.home.clicked.connect(self.back_home)

    def back_home(self):
        self.cpt.release()
        self.cpt2.release()
        self.close()

class WindowFindInitialPose(QMainWindow, find_initial_pose):
    def __init__(self, mode=0, input_id = 0, extraction_id = 0):
        super().__init__()
        self.setupUi(self)
        self.mode = mode
        self.input_id = input_id
        self.extraction_id = extraction_id
        self.show()
        self.connectFunction()
        self.isSkipped = False

        args = (input_id,)
        self.skeleton, self.found_num, self.skeleton_id = main_function(2, *args)
        if self.found_num == -1:
            QMessageBox.warning(
                self, 'Error', "You should select file or Enter Video Info")
            self.close()

        self.graph()
        self.Video()

    def graph(self):
        self.graph_title = ['left_elbow', 'right_elbow', 'left_knee', 'right_knee']
        self.graph_list.setFlow(QListWidget.LeftToRight)
        self.graph_list.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.numpy = np.load('temp/graph.npy')
        mcanvases = [FigureCanvas(Figure(figsize=(5, 3))) for i in range(len(self.numpy))]
        self.axes = []
        for idx, mcanvase in enumerate(mcanvases):
            itemN = QListWidgetItem()
            itemN.setSizeHint(QSize(380, 380))
            self.graph_list.addItem(itemN)
            self.graph_list.setItemWidget(itemN, mcanvase)
            self.axes.append(mcanvase.figure.subplots())
            self.axes[idx].set(title = self.graph_title[idx])

    def Video(self):
        self.origin_label.setScaledContents(True)
        self.copy_label.setScaledContents(True)
        self.cpt = cv2.VideoCapture('temp/init_video.avi')
        self.frequency = 0.3
        self.cnt = 0
        self.start()

    def start(self):
        cam = 1
        index = 0
        while self.cpt.isOpened() and cam is not None:
            # Video
            _, cam = self.cpt.read()
            if cam is not None:
                cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
                img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
                pix = QPixmap.fromImage(img)
                pix2 = QPixmap.fromImage(img)
                self.origin_label.setPixmap(pix)
                if index < self.found_num:
                    self.copy_label.setPixmap(pix2)
                else:
                    self.found_label.setStyleSheet('color:green')
                    self.found_label.setText('Complete Analyze')
                    self.copy_label.setStyleSheet("border: 7px inset green;")
                cv2.waitKey(100)

            # graph
            for i in range(len(self.axes)):
                self.axes[i].clear()
                self.axes[i].set(title = self.graph_title[i], )
                if index < 50:
                    self.axes[i].plot(self.numpy[i][0:index])
                else:
                    self.axes[i].plot(self.numpy[i][index-50:index])
                self.axes[i].figure.canvas.draw()

            index += 1
        if self.isSkipped != True:
            run.make_skeleton_image(self.skeleton, 'temp/skeleton.png')
        self.cpt.release()

    def connectFunction(self):
        self.next.clicked.connect(self.Next)

    def Next(self):
        self.cpt.release()
        self.isSkipped = True
        self.close()
        if self.mode == 0:
            self.window = WindowReigsterTrainerBetter(self.skeleton_id, self.input_id)
        else:
            self.window = WindowResizeTrainer(self.skeleton_id, self.extraction_id, self.input_id)

class WindowRegisterTrainer(QMainWindow, register_trainer):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_id
        self.connectFunction()

        self.setuserinfo()

        rows = DB.get_input_list(self.user_id)
        if rows != []:
            for row in rows:
                self.yourlist.addItem(f'{row[0]}.{row[1]}')
            self.input_id_list = rows[:]

        rows = DB.get_math_info_list(self.user_id)
        if rows != []:
            self.extraction_id_list = rows[:]
            for row in rows:
                self.registeredlist.addItem(f'{row[0]}.{row[1]}')
        self.target_type = 0
        self.target_id = 0

    def connectFunction(self):
        self.pushButton.clicked.connect(self.next)
        self.yourlist.itemClicked.connect(self.analyze)
        self.registeredlist.itemClicked.connect(self.view)

    def next(self):
        if self.target_type in (0, 2):
            QMessageBox.warning(
                self, 'Error', "You should select which item you want to analyze")
        else:
            self.window = WindowFindInitialPose(mode=0, input_id=self.target_id)
            self.close()

    def analyze(self):
        index = self.yourlist.currentRow()
        self.target_type = 1
        self.target_id = self.input_id_list[index][0]

        text = f'Creation Time : {self.input_id_list[index][2]}\n' \
               f'State : Not Analyzed\n' \
               f'\nIf you want to register \n' \
               f'your video, clicked analyze.'
        self.note.setText(text)

    def view(self):
        index = self.registeredlist.currentRow()
        self.target_type = 2
        self.target_id = self.extraction_id_list[index][0]
        text = f'Creation Time : {self.extraction_id_list[index][2]}\n' \
               f'State : Analyzed\n' \
               f'\nThis item is already\n' \
               f'been analyzed.\n' \
               f'If you want to see this,\n' \
               f'please go to more info.'
        self.note.setText(text)

    def setuserinfo(self):
        user = DB.get_user_info(self.user_id)
        if user[0][0] == 'standard':
            text = f'Hello, Trainer {user[0][1]}'
        else:
            text = f'Hello, {user[0][1]}'
        self.userinfo.setText(text)

# UC 3
class WindowResizeTrainer(QMainWindow, resize_trainer):
    def __init__(self, skeleton_id, extraction_id, input_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.skeleton_id = skeleton_id
        self.extraction_id = extraction_id
        self.connectFunction()
        args = (self.skeleton_id, self.extraction_id, input_id)
        main_function(4, *args)
        self.graph()
        self.Video()
        QMessageBox.about(self,"Chungyo","Finish resize the trainer skeleton to your shape!!\nPlease click 'HOME' button and return main page.")

    def graph(self):
        self.graph_title = ['left_elbow', 'right_elbow', 'left_knee', 'right_knee']
        self.graph_list.setFlow(QListWidget.LeftToRight)
        self.graph_list.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.numpy = np.load('temp/graph.npy')
        mcanvases = [FigureCanvas(Figure(figsize=(5, 3))) for i in range(len(self.numpy))]
        self.axes = []
        for idx, mcanvase in enumerate(mcanvases):
            itemN = QListWidgetItem()
            itemN.setSizeHint(QSize(380, 380))
            self.graph_list.addItem(itemN)
            self.graph_list.setItemWidget(itemN, mcanvase)
            self.axes.append(mcanvase.figure.subplots())
            self.axes[idx].set(title = self.graph_title[idx])

    def Video(self):
        self.origin_label.setScaledContents(True)
        self.copy_label.setScaledContents(True)
        self.cpt = cv2.VideoCapture('temp/math_info.avi')
        self.cpt2 = cv2.VideoCapture('temp/resized.avi')
        self.frequency = 0.3
        self.cnt = 0
        self.start()

    def start(self):
        cam = 1
        cam2 = 1
        index = 0
        while self.cpt.isOpened() and cam is not None and cam2 is not None:
            # Video
            _, cam = self.cpt.read()
            _, cam2 = self.cpt2.read()
            if cam is not None and cam2 is not None:
                cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
                cam2 = cv2.cvtColor(cam2, cv2.COLOR_BGR2RGB)
                img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
                img2 = QImage(cam2, cam2.shape[1], cam2.shape[0], QImage.Format_RGB888)
                pix = QPixmap.fromImage(img)
                pix2 = QPixmap.fromImage(img2)
                self.origin_label.setPixmap(pix)
                self.copy_label.setPixmap(pix2)

                cv2.waitKey(100)

            # graph
            for i in range(len(self.axes)):
                self.axes[i].clear()
                self.axes[i].set(title = self.graph_title[i], )
                if index < 50:
                    self.axes[i].plot(self.numpy[i][0:index])
                else:
                    self.axes[i].plot(self.numpy[i][index - 50:index])
                self.axes[i].figure.canvas.draw()

            index += 1
        self.cpt.release()
        self.cpt2.release()

    def connectFunction(self):
        self.home.clicked.connect(self.back_home)

    def back_home(self):
        self.cpt.release()
        self.cpt2.release()
        self.close()

class WindowMakeTrainer(QMainWindow, make_trainer):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_id
        self.setuserinfo()

        self.yourlist.clear()
        self.comboBox.clear()
        self.comparison.clear()

        rows = DB.get_input_list(self.user_id)
        if rows != []:
            self.input_id_list = rows[:]
            for row in rows:
                self.yourlist.addItem(f'{row[0]}.{row[1]}')

        rows = DB.get_user_list('standard')
        if rows != []:
            self.trainer_id_list = list(zip(*rows))[0]
            for row in rows:
                self.comboBox.addItem(f'{row[1]}')

            # 무조건 트레이너 한명은 있다고 가정한다.
            rows = DB.get_math_info_list(self.trainer_id_list[0])
            if rows != None:
                self.extraction_id_list = rows[:]
                for row in rows:
                    self.comparison.addItem(f'{row[0]}.{row[1]}')

        self.extraction_id = 0
        self.input_id = 0

        self.connectFunction()

    def connectFunction(self):
        self.analyze.clicked.connect(self.next)
        self.yourlist.itemClicked.connect(self.set_input_id)
        self.comboBox.currentIndexChanged.connect(self.change_extraction_list)
        self.comparison.itemClicked.connect(self.set_extraction_id)

    def set_extraction_id(self):
        index = self.comparison.currentRow()
        self.extraction_id = self.extraction_id_list[index]

        text = f'Creation Time : {self.extraction_id_list[index][2]}\n' \
               f'State : Made\n' \
               f'\nYou can make your own' \
               f'Personal Trainer!,\n' \
               f'If you choose exercise,\n' \
               f'please clicked analyze.'
        self.note.setText(text)

    def change_extraction_list(self, idx):
        trainer_id = self.trainer_id_list[idx]
        self.comparison.clear()
        rows = DB.get_math_info_list(trainer_id)
        self.extraction_id_list = rows
        if rows != None:
            for row in rows:
                self.comparison.addItem(f'{row[0]}.{row[1]}')

    def set_input_id(self):
        index = self.yourlist.currentRow()
        self.input_id = self.input_id_list[index]

        text = f'Creation Time : {self.input_id_list[index][2]}\n' \
               f'State : Not Made\n' \
               f'\nIf you want to make your' \
               f'Personal Trainer,\n' \
               f'after the choice comparison\n' \
               f'clicked analyze.'
        self.note.setText(text)

    def next(self):
        if self.input_id != 0 and self.extraction_id != 0:
            if self.input_id[1] != self.extraction_id[1]:
                QMessageBox.warning(
                    self, 'Error', "You should select sample based on same exercise")
            else:
                self.window = WindowFindInitialPose(1, self.input_id[0], self.extraction_id[0])
                self.close()
        else:
            QMessageBox.warning(
                self, 'Error', "You should select both of input and comparison")

    def setuserinfo(self):
        user = DB.get_user_info(self.user_id)
        if user[0][0] == 'standard':
            text = f'Hello, Trainer {user[0][1]}'
        else:
            text = f'Hello, {user[0][1]}'
        self.userinfo.setText(text)

# UC 4
class WindowStore(QMainWindow, store):
    def __init__(self, input_id, sample_id):
        super().__init__()
        self.setupUi(self)
        self.m_movie_gif = QMovie("ui/image/loading.gif")
        self.m_movie_gif.setSpeed(350)
        self.frame.setMovie(self.m_movie_gif)
        self.frame.setAlignment(Qt.AlignCenter)
        self.m_movie_gif.start()
        self.bar_msg.setText("Loading...")
        self.show()
        self.connectFunction()
        args = (input_id, sample_id)
        main_function(6, *args)
        self.bar_msg.setText("Progress")
        self.Video()
        QMessageBox.about(self,"Cungyo","Your exercise is stored in our data base.\nPlease click 'NEXT' button and finish your analyze.")

    def Video(self):
        self.frame.setScaledContents(True)
        self.cpt = cv2.VideoCapture('temp/output.avi')
        self.fps = 60
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.start()

    def start(self):
        cam = 1
        index = 0
        length = int(self.cpt.get(cv2.CAP_PROP_FRAME_COUNT))
        while self.cpt.isOpened() and cam is not None:
            # Video
            _, cam = self.cpt.read()
            if cam is not None:
                cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
                img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
                pix = QPixmap.fromImage(img)
                self.frame.setPixmap(pix)
                cv2.waitKey(int((1/self.fps) * 1000))

            # progressBar
            self.progressBar.setValue(int(index/length * 100))

            index += 1
        self.cpt.release()

    def connectFunction(self):
        self.next.clicked.connect(self.close)

class WindowAnalyzeGuide(QMainWindow, analyze_guide):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_id
        self.connectFunction()
        rows = DB.get_input_list(self.user_id)
        if rows != []:
            self.input_id_list = rows[:]
            for row in rows:
                self.user.addItem(f'{row[0]}.{row[1]}')

        rows = DB.load_applied_skeleton_list(self.user_id)
        if rows != []:
            self.applied_trainer_list = rows[:]
            for row in rows:
                self.applied_trainer.addItem(f'{row[0]}.{row[1]}-{row[2]}')
        self.input_id = 0
        self.target_id = 0

    def connectFunction(self):
        self.store.clicked.connect(self.Store)
        self.user.itemClicked.connect(self.change_input_id)
        self.applied_trainer.itemClicked.connect(self.change_target_id)

    def change_input_id(self):
        index = self.user.currentRow()
        self.input_id = self.input_id_list[index]

    def change_target_id(self):
        index = self.applied_trainer.currentRow()
        self.target_id = self.applied_trainer_list[index]

    def Store(self):
        if self.input_id !=0 and self.target_id !=0:
            if self.input_id[1] == self.target_id[2]:
                self.window = WindowStore(self.input_id[0], self.target_id[0])
                self.close()
            else:
                QMessageBox.warning(
                    self, 'Error', "You should select same exercise")
        else:
            QMessageBox.warning(
                self, 'Error', "You should select Both")

# UC 5
class WindowReport(QMainWindow, report):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id =  user_id
        self.connectFunction()
        rows = DB.get_input_list(self.user_id)
        if rows != []:
            self.input_id_list = rows[:]
            for row in rows:
                self.user.addItem(f'{row[0]}.{row[1]}')

        rows = DB.load_applied_skeleton_list(self.user_id)
        if rows != []:
            self.applied_trainer_list = rows[:]
            for row in rows:
                self.applied_trainer.addItem(f'{row[0]}.{row[1]}-{row[2]}')
        self.input_id = 0
        self.target_id = 0

    def connectFunction(self):
        self.export_2.clicked.connect(self.Store)
        self.user.itemClicked.connect(self.change_input_id)
        self.applied_trainer.itemClicked.connect(self.change_target_id)

    def change_input_id(self):
        index = self.user.currentRow()
        self.input_id = self.input_id_list[index]

    def change_target_id(self):
        index = self.applied_trainer.currentRow()
        self.target_id = self.applied_trainer_list[index]

    def Store(self):
        if self.input_id !=0 and self.target_id !=0:
            if self.input_id[1] == self.target_id[2]:

                args = [
                self.input_id[0],
                self.target_id[0]
                ]
                main_function(8, *args)
                self.close()
                self.window = SuccessWindow()

            else:
                QMessageBox.warning(
                    self, 'Error', "You should select same exercise")
        else:
            QMessageBox.warning(
                self, 'Error', "You should select Both")


# Start
class WindowStart(QMainWindow, start):
    def __init__(self, user_data):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_data[0]
        self.user_name = user_data[1]
        self.username.appendPlainText(user_data[1])
        self.usertype.appendPlainText(user_data[2])

        self.connectFunction()

    def connectFunction(self):
        self.upload.clicked.connect(lambda: self.changePage(0))
        self.register_2.clicked.connect(lambda: self.changePage(1))
        self.make.clicked.connect(lambda: self.changePage(2))
        self.analyze_guide.clicked.connect(lambda: self.changePage(3))
        self.comment.clicked.connect(lambda: self.changePage(4))
        self.moreinfo.clicked.connect(lambda: self.changePage(5))

    def changePage(self, x):
        if x == 0:
            self.window = WindowUploadVideo(self.user_id)
        elif x == 1:
            if self.usertype.toPlainText() == 'common':
                QMessageBox.warning(
                    self, 'Error', "Your should log-in as Trainer to use this function")
            else:
                self.window = WindowRegisterTrainer(self.user_id)
        elif x == 2:
            self.window = WindowMakeTrainer(self.user_id)
        elif x == 3:
            self.window = WindowAnalyzeGuide(self.user_id)
        elif x == 4:
            self.window = WindowReport(self.user_id)
        elif x == 5 :
            self.window = WindowMoreInfo(self.user_id, self.user_name)

class WindowMoreInfo(QMainWindow, moreinfo):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.user_id = user_id

        use_cases = [
        'find intial_pose',
        'applied skeleton',
        'diffing',
        'improved recognition ratio'
        ]
        self.ucs.clear()
        self.ucs.addItems(use_cases)
        self.graph_file = ""
        self.origin_file = ""
        self.copy_file = ""
        self.cpt = None
        self.cpt2 = None
        self.paly = True
        self.datas = []
        self.graph_titles = [
        ['left_elbow', 'right_elbow', 'left_knee', 'right_knee'],
        ['left_elbow', 'right_elbow', 'left_knee', 'right_knee'],
        ['score', 'left_shoulder', 'left_elbow', 'left_wrist', 'right_shoulder', 'right_elbow', 'right_wrist'],
        ['left_elbow', 'right_elbow', 'left_knee', 'right_knee']
        ]
        self.connectFunction()

    def connectFunction(self):
        self.ucs.currentIndexChanged.connect(self.change_ucs)
        self.start_button.clicked.connect(self.loading)

    def loading(self):
        if self.cpt != None or self.cpt2 != None:
            self.cpt.release()
            self.cpt2.release()
        self.play = False
        index = self.ucs.currentIndex()
        datas = self.data[self.ids.currentIndex()]
        self.graph_title = self.graph_titles[index]
        base_folder = 'temp'
        if os.path.exists(base_folder):
            shutil.rmtree(base_folder)
        time.sleep(1)
        os.mkdir(base_folder)

        if index == 0:
            # file load
            DB.read_from_input_list(datas[2], base_folder)
            DB.load_skeleton(datas[0], base_folder)
            # video
            self.origin_file = 'temp/init_video.avi'
            self.copy_file = 'temp/init_video.avi'

        elif index == 1:
            # file load
            DB.load_skeleton(datas[3], base_folder) # N
            DB.load_math_info_extraction(datas[2], base_folder)
            DB.load_applied_skeleton_file(datas[0], base_folder)
            # video
            self.origin_file = 'temp/math_info.avi'
            self.copy_file = 'temp/upgraded.avi'

        elif index == 2:
            # file load
            DB.read_from_input_list(datas[2], base_folder)
            DB.load_diff(datas[0], base_folder)
            # video
            self.origin_file = 'temp/exercise_video.avi'
            self.copy_file = 'temp/diff.avi'

        elif index == 3:
            # file load
            DB.load_skeleton(datas[3], base_folder) # N
            DB.read_from_input_list(datas[2], base_folder)
            DB.load_math_info_extraction(datas[0], base_folder)
            # video
            self.origin_file = 'temp/exercise_video.avi'
            self.copy_file = 'temp/math_info.avi'

        self.graph()
        self.Video()

    def change_ucs(self, i):
        self.ids.clear()
        self.data = []
        for row in DB.load_data_list(self.user_id, i):
            self.ids.addItem(str(row[0]) + "-" + row[1])
            self.data.append(row)

    def graph(self):
        self.graph_list.clear()
        self.graph_list.setFlow(QListWidget.LeftToRight)
        self.graph_list.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.numpy = np.load('temp/graph.npy')
        if self.ucs.currentIndex() == 2:
            self.numpy = self.numpy[:-1]
        mcanvases = [FigureCanvas(Figure(figsize=(5, 3))) for i in range(len(self.numpy))]
        self.axes = []
        for idx, mcanvase in enumerate(mcanvases):
            itemN = QListWidgetItem()
            itemN.setSizeHint(QSize(380, 380))
            self.graph_list.addItem(itemN)
            self.graph_list.setItemWidget(itemN, mcanvase)
            self.axes.append(mcanvase.figure.subplots())
            self.axes[idx].set(title = self.graph_title[idx])

    def Video(self):
        self.origin_label.setScaledContents(True)
        self.copy_label.setScaledContents(True)
        self.cpt = cv2.VideoCapture(self.origin_file)
        self.cpt2 = cv2.VideoCapture(self.copy_file)
        self.fps = 60
        self.cnt = 0
        self.start()

    def start(self):
        cam = 1
        cam2 = 1
        index = 0
        ucs = self.ucs.currentIndex()
        self.play = True
        while self.play == True and self.cpt.isOpened() and cam is not None and cam2 is not None:
            # Video
            _, cam = self.cpt.read()
            _, cam2 = self.cpt2.read()
            if cam is not None and cam2 is not None:
                cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
                cam2 = cv2.cvtColor(cam2, cv2.COLOR_BGR2RGB)
                img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
                img2 = QImage(cam2, cam2.shape[1], cam2.shape[0], QImage.Format_RGB888)
                pix = QPixmap.fromImage(img)
                pix2 = QPixmap.fromImage(img2)
                self.origin_label.setPixmap(pix)
                self.copy_label.setPixmap(pix2)

                cv2.waitKey(int((1/self.fps) * 1000))

            # graph
            if ucs == 2:
                # score 부분
                average_score = average_score = sum(self.numpy[0]) / len(self.numpy[0])
                self.axes[0].clear()
                self.axes[0].set_ylim([0, 100])
                self.axes[0].axhline(y = average_score, c='r', ls='--', label='avergae score: %d' % average_score)
                self.axes[0].set(title = self.graph_title[0], )
                self.axes[0].legend()
                if index < 50:
                    self.axes[0].plot(self.numpy[0][0:index])
                else:
                    self.axes[0].plot(self.numpy[0][index - 50:index])
                self.axes[0].figure.canvas.draw()

                for i in range(1, len(self.axes)):
                    self.axes[i].clear()
                    self.axes[i].set(title = self.graph_title[i], )
                    xs, ys = list(zip(*self.numpy[i]))[0], list(zip(*self.numpy[i]))[1]
                    x_max = max([abs(x) for x in xs])
                    y_max = max([abs(y)for y in ys])
                    self.axes[i].set_xlim([-x_max, x_max])
                    self.axes[i].set_ylim([-y_max, y_max])
                    self.axes[i].grid(True)
                    self.axes[i].axhline(y=0, c='black', ls='--')
                    self.axes[i].axvline(x=0, c='black', ls='--')
                    if index < 50:
                        self.axes[i].scatter(xs[0:50], ys[0:50])
                    else:
                        self.axes[i].scatter(xs[0:index], ys[0:index])
                    self.axes[i].figure.canvas.draw()
            else:
                for i in range(len(self.axes)):
                    self.axes[i].clear()
                    self.axes[i].set(title = self.graph_title[i], )
                    if index < 50:
                        self.axes[i].plot(self.numpy[i][0:index])
                    else:
                        self.axes[i].plot(self.numpy[i][index - 50:index])
                    self.axes[i].figure.canvas.draw()

            index += 1
        self.cpt.release()
        self.cpt2.release()



class WindowSignUp(QMainWindow, signup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.conditions = [False, False, False, False]
        self.connectFunction()

    def connectFunction(self):
        self.username.textChanged.connect(self.checkUnique)
        self.password.textChanged.connect(lambda: self.setChangedMSGG(0))
        self.confirm_password.textChanged.connect(lambda: self.setChangedMSGG(1))
        self.slider_age.valueChanged.connect(lambda: self.setChangedMSGG(3))
        self.slider_stature.valueChanged.connect(lambda: self.setChangedMSGG(3))
        self.slider_weight.valueChanged.connect(lambda: self.setChangedMSGG(3))
        self.already.clicked.connect(self.close)
        self.sign_up.clicked.connect(self.signup)
        self.agree_term.toggled.connect(self.agree)

    def agree(self):
        self.conditions[3] = not self.conditions[3]

    def checkUnique(self):
        is_unique = DB.checkUnique(self.username.text())

        if is_unique==False:
            self.user_unique.setText("Duplicated!")
            self.user_unique.setStyleSheet('color: red')
            self.conditions[0]=False
        else:
            self.user_unique.setText("Unique!")
            self.user_unique.setStyleSheet('color: green')
            self.conditions[0]=True

    def setChangedMSGG(self,type):
        if type==0:
            org_password = self.password.text()
            ch_password = self.confirm_password.text()

            if org_password == ch_password:
                self.confirm.setText("Same")
                self.confirm.setStyleSheet("color:green")
                self.conditions[2] = True
            else:
                self.confirm.setText("Different")
                self.confirm.setStyleSheet("color:red")
                self.conditions[2] = False

            if len(org_password) <9 and len(org_password) >3 and org_password.isdigit():
                self.origin.setText("Ok")
                self.origin.setStyleSheet('color: green')
                self.conditions[1] = True
            else:
                self.origin.setText("password should be digit whose length is in 4~8.")
                self.origin.setStyleSheet('color: red')
                self.conditions[1] = False
        elif type==1:
            org_password = self.password.text()
            ch_password = self.confirm_password.text()

            if org_password == ch_password:
                self.confirm.setText("Same")
                self.confirm.setStyleSheet("color:green")
                self.conditions[2] = True
            else:
                self.confirm.setText("Different")
                self.confirm.setStyleSheet("color:red")
                self.conditions[2] = False
        elif type==3:
            self.age_label.setText( str(self.slider_age.value()) )
            self.stature_label.setText( str(self.slider_stature.value()) )
            self.weight_label.setText( str(self.slider_weight.value()) )

        return True

    def signup(self):
        if all(self.conditions):
            conn = sqlite3.connect('./pose_diff/DB/pose_diff.db')
            c = conn.cursor()

            input_name = self.username.text()
            input_pw = self.password.text()
            stature = self.stature_label.text()
            weight = self.weight_label.text()
            user_type = str(self.user_type.currentText())
            sex = str(self.sex.currentText())

            c.execute('''INSERT INTO user_list(user_type, user_name, password, weight, stature, SEX) VALUES (?, ?, ?, ?, ?, ?)''', (user_type, input_name,input_pw, weight, stature, sex))

            conn.commit()
            conn.close()
            self.close()
        else:
            QMessageBox.warning(
                self, 'Error', "Enter Again")

class LoadingWindow(QWidget,loading):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.m_movie_gif = QMovie("loading.gif")
        self.m_movie_gif.setSpeed(350)
        self.frame.setMovie(self.m_movie_gif)
        self.frame.setAlignment(Qt.AlignCenter)
        self.m_movie_gif.start()

class SuccessWindow(QMainWindow,success):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.out.clicked.connect(self.close)

if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
