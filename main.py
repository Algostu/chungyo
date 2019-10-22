import sys
import os
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui

import os
from pose_diff.DB import DB
import sqlite3
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
view = uic.loadUiType("ui/view.ui")[0]
report = uic.loadUiType("ui/report.ui")[0]
moreinfo = uic.loadUiType("ui/moreinfo.ui")[0]

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
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.connectFunction()

    def connectFunction(self):
        self.home.clicked.connect(self.close)

class WindowFindInitialPose(QMainWindow, find_initial_pose):
    def __init__(self, mode=0, input_id = 0, extraction_id = 0):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.mode = mode
        self.input_id = input_id
        self.extraction_id = extraction_id
        self.connectFunction()

    def connectFunction(self):
        self.next.clicked.connect(self.Next)

    def Next(self):
        if self.mode == 0:
            self.window = WindowReigsterTrainerBetter()
        else:
            self.window = WindowResizeTrainer()
        self.close()

class WindowRegisterTrainer(QMainWindow, register_trainer):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_id
        self.connectFunction()

        self.setuserinfo()

        rows = DB.get_input_list(self.user_id)
        self.input_id_list = list(zip(*rows))[0]
        if rows != None:
            for row in rows:
                self.yourlist.addItem(f'{row[0]}.{row[1]}')

        rows = DB.get_math_info_list(self.user_id)
        self.extraction_id_list = list(zip(*rows))[0]
        if rows != None:
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
        self.target_id = self.input_id_list[index]

        text = f'Creation Time : \n' \
               f'State : Not Analyzed\n' \
               f'\nIf you want to register \n' \
               f'your video, clicked analyze.'
        self.note.setText(text)

    def view(self):
        text = f'Creation Time : \n' \
               f'State : Analyzed\n' \
               f'\nThis item is already\n' \
               f'been analyzed.\n' \
               f'If you want to see this,\n' \
               f'please go to more info.'
        self.note.setText(text)

        index = self.registeredlist.currentRow()
        self.target_type = 2
        self.target_id = self.extraction_id_list[index]

    def setuserinfo(self):
        user = DB.get_user_info(self.user_id)
        text = f'Hello, {user[0][0]} {user[0][1]}'
        self.userinfo.setText(text)

# UC 3
class WindowResizeTrainer(QMainWindow, resize_trainer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.connectFunction()

    def connectFunction(self):
        self.home.clicked.connect(self.close)

class WindowMakeTrainer(QMainWindow, make_trainer):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_id
        self.setuserinfo()
        rows = DB.get_input_list(self.user_id)
        if rows != None:
            self.input_id_list = rows[:]
            for row in rows:
                self.yourlist.addItem(f'{row[0]}.{row[1]}')

        rows = DB.get_user_list('standard')
        if rows != None:
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
        self.extraction_id = self.extraction_id_list[self.comparison.currentRow()]

        text = f'Creation Time : \n' \
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
        self.input_id = self.input_id_list[self.yourlist.currentRow()]

        text = f'Creation Time : \n' \
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
        text = f'Hello, {user[0][0]} {user[0][1]}'
        self.userinfo.setText(text)

# UC 4
class WindowStore(QMainWindow, store):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.connectFunction()

    def connectFunction(self):
        self.next.clicked.connect(self.close)

class WindowView(QMainWindow, view):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.connectFunction()

    def connectFunction(self):
        self.next.clicked.connect(self.close)

class WindowAnalyzeGuide(QMainWindow, analyze_guide):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_id
        self.connectFunction()

    def connectFunction(self):
        self.store.clicked.connect(self.Store)

    def Store(self):
        self.window = WindowStore()
        self.close()

# UC 5
class WindowReport(QMainWindow, report):
    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id =  user_id
        self.connectFunction()

    def connectFunction(self):
        self.export_2.clicked.connect(self.close)

# Start
class WindowStart(QMainWindow, start):
    def __init__(self, user_data):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.user_id = user_data[0]
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
            self.window = WindowMoreInfo()

class WindowMoreInfo(QMainWindow, moreinfo):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.connectFunction()

    def connectFunction(self):
        pass

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
