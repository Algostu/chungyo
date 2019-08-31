import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np
from m_han.trainer.parse import load_ps
from m_han.trainer.evaluate import evaluate_pose
## 오차범위 가중치 처음과 끝;; 유저의 시간을 트레이너에게 맞추기

def frame_filtering(user,trainer): #frame resizing
   user_frame = len(user)
   trainer_frame = len(trainer)

   if trainer_frame > user_frame:
        recom = "trainer"
        resize = np.zeros(user.shape)
        split = int(trainer_frame / user_frame)
        cnt = 0
        while cnt < trainer_frame:
            resize[cnt] = trainer[cnt]
            cnt = cnt+split

   elif trainer_frame < user_frame:
        recom = "user"
        resize = np.zeros(user.shape)
        split = int(user_frame / trainer_frame)
        cnt = 0
        while cnt < trainer_frame:
            resize[cnt] = user[cnt]
            cnt = cnt + split
   else:
       recom = "no"
       resize = "no"

   return recom, resize

def angle_difference(trainer,user,exercise):
    trainer_x, trainer_y, trainer_z = evaluate_pose(trainer, exercise)
    user_x, user_y, user_z = evaluate_pose(user, exercise)

    angle_np = np.copy(user)

    #Error in RED = 0, Success in GREEN = 1
    if exercise == 'pullup': #The coordinates indicated vary depending on the type of exercise
        i=0                  #pullup assumes necessary body parts as rsholder(x),relbow(y),rwrist(z) : (2,3,4)
        while True:
            if i>len(user):
                break

            if trainer_x[i]+1<user_x[i] or trainer_x[i]-1>user_x[i]:
                angle_np[i][2][2] = 0

            elif trainer_y[i]+1<user_y[i] or trainer_y[i]-1>user_y[i]:
                angle_np[i][3][2] = 0

            elif trainer_z[i]+1<user_z[i] or trainer_z[i]-1>user_z[i]:
                angle_np[i][4][2] = 0
            else:
                angle_np[i][4][2] = 1
            i= i+1
        return angle_np

def point_difference(trainer, user, exercise):

    trainer_x, trainer_y, trainer_z = evaluate_pose(trainer, exercise)
    user_x, user_y, user_z = evaluate_pose(user, exercise)

    point_np = np.copy(user)

    # Error in RED = 0, Success in GREEN = 1
    if exercise == 'pullup':  # The coordinates indicated vary depending on the type of exercise
        i = 0  # pullup assumes necessary body parts as rsholder(x),relbow(y),rwrist(z) : (2,3,4)
        while True:
            if i > len(user):
                break

            if trainer_x[i] + 0.5 < user_x[i] or trainer_x[i] - 0.5 > user_x[i]:
                point_np[i][2][2] = 0

            elif trainer_y[i] + 0.5 < user_y[i] or trainer_y[i] - 0.5 > user_y[i]:
                point_np[i][3][2] = 0

            elif trainer_z[i] + 0.5 < user_z[i] or trainer_z[i] - 0.5 > user_z[i]:
                point_np[i][4][2] = 0
            else:
                point_np[i][4][2] = 1
            i = i + 1
    return point_np

def diffing(trainer_npy,user_npy,exercise):
    user = np.load(user_npy)
    trainer = np.load(trainer_npy)
    recom, resize = frame_filtering(user, trainer)

    if recom == "trainer":
        trainer = resize
        anglenp = angle_difference(trainer,user,exercise)
        pointnp = point_difference(trainer,user,exercise)
        for a,b in zip(anglenp,pointnp):
            for i in range(0,18):
                if a[i][2] == 0 and b[i][2]==0:
                    user[i][2] = 0
    else:
        user = resize
        anglenp = angle_difference(trainer, user, exercise)
        pointnp = point_difference(trainer, user, exercise)
        for a,b in zip(anglenp,pointnp):
            for i in range(0,18):
                if a[i][2] == 0 and b[i][2]==0:
                    user[i][2] = 0

    return user,trainer
