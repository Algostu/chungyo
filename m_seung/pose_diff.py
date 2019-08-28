import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np
from m_han.parse import load_ps
from m_han.evaluate import evaluate_pose
## 오차범위 가중치 처음과 끝;; 유저의 시간을 트레이너에게 맞추기

def frame_filtering():
    pass

def angle_difference(exercise):
    trainer = load_ps("skeleton1.npy")
    user = load_ps("skeleton2.npy")
    trainer_x, trainer_y, trainer_z = evaluate_pose(trainer, exercise)
    user_x, user_y, user_z = evaluate_pose(user, exercise)

    user_np = np.load("skeleton2.npy")

    #Error in RED = 0, Success in GREEN = 1
    if exercise == 'pullup': #The coordinates indicated vary depending on the type of exercise
        i=0                  #pullup assumes necessary body parts as rsholder(x),relbow(y),rwrist(z) : (2,3,4)
        while True:
            if (user_x[i] == None or user_y[i]==None or trainer_x[i]==None or trainer_y[i]==None or i==120): #frame_filtering이 완성되면 i==120 대체
                break

            if (trainer_x[i]+1<user_x[i] or trainer_x[i]-1>user_x[i]):
                user_np[i][2][2] = 0

            elif (trainer_y[i]+1<user_y[i] or trainer_y[i]-1>user_y[i]):
                user_np[i][3][2] = 0

            elif (trainer_z[i]+1<user_z[i] or trainer_z[i]-1>user_z[i]):
                user_np[i][4][2] = 0
            else:
                user_np[i][4][2] = 1
            i= i+1
        return user_np

def point_difference():
    pass