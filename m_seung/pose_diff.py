import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np
# from m_han.trainer.parse import load_ps
# from m_han.trainer.evaluate import evaluate_pose
# from m_han.trainer.pose import PoseSequence
## 오차범위 가중치 처음과 끝;; 유저의 시간을 트레이너에게 맞추기

def frame_filtering(trainer,user): #frame resizing
   user_frame = len(user)
   trainer_frame = len(trainer)

   if trainer_frame > user_frame:
        recom = "trainer"
        resize = np.zeros(user.shape)
        split = trainer_frame / user_frame
        cnt1= 0
        cnt2=0
        while cnt2 < trainer_frame-1:
            resize[cnt1] = trainer[cnt2]
            cnt2 = round(cnt2 + split*cnt1)
            cnt1 = cnt1 + 1

   elif trainer_frame < user_frame:
        recom = "user"
        resize = np.zeros(trainer.shape)
        split = int(user_frame / trainer_frame)
        cnt1 = 0
        cnt2 = 0
        while cnt2 < user_frame-1:
            resize[cnt1] = user[cnt2]
            cnt1 = cnt1 + 1
            cnt2 = cnt2 + split
   else:
       recom = "no"
       resize = "no"

   return recom, resize

def frame_upscaling(trainer,user): #make bigger the fewer frame
    user_frame = len(user)
    trainer_frame = len(trainer)

    if trainer_frame > user_frame:
        recom = "user"
        resize = np.zeros(trainer.shape)
        split = trainer_frame / user_frame
        num=0
        while 1:
            if num == user_frame:
                break
            for i in range(int(round(split*num,1)),int(round(split*(num+1),1))):
                resize[i] = user[num]
            num = num + 1

    elif trainer_frame < user_frame:
        recom = "trainer"
        resize = np.zeros(user.shape)
        split = user_frame / trainer_frame
        num = 0
        while 1:
            for i in range(int(round(split*num,1)),int(round(split*(num+1),1))):
                resize[i] = trainer[num]
            num = num + 1
    else:
        recom = "no"
        resize = "no"

    return recom, resize


def angle_difference(trainer,user,exercise):
    # trainer_x, trainer_y, trainer_z = evaluate_pose(PoseSequence(trainer), exercise)
    # user_x, user_y, user_z = evaluate_pose(PoseSequence(user), exercise)
    #
    angle_np = np.copy(user)
    for i in angle_np:
        for j in i:
            j[2] = 1
    #
    # #Error in RED = 0, Success in GREEN = 1
    # if exercise == 'pullup': #The coordinates indicated vary depending on the type of exercise
    #     i=0                  #pullup assumes necessary body parts as rsholder(x),relbow(y),rwrist(z) : (2,3,4)
    #     while True:
    #         if i>len(user):
    #             break
    #
    #         if trainer_x[i]+1<user_x[i] or trainer_x[i]-1>user_x[i]:
    #             angle_np[i][2][2] = 1
    #
    #         elif trainer_y[i]+1<user_y[i] or trainer_y[i]-1>user_y[i]:
    #             angle_np[i][3][2] = 1
    #
    #         elif trainer_z[i]+1<user_z[i] or trainer_z[i]-1>user_z[i]:
    #             angle_np[i][4][2] = 1
    #         else:
    #             angle_np[i][4][2] = 0
    #         i= i+1
    return angle_np

def point_difference(trainer, user, exercise):
    point_np = np.copy(user)
    # Error in RED = 1, Success in GREEN = 0
    if exercise == 'pullup':  # The coordinates indicated vary depending on the type of exercise
        i = 0  # pullup assumes necessary body parts as rsholder(x),relbow(y),rwrist(z) : (2,3,4)
        margin = 1
        while True:
            # print(f'trainer {trainer[i][2][0]}')
            # print(f'user {user[i][2][0]}')
            if i > len(user)-1:
                break
            if trainer[i][2][0] + margin < user[i][2][0] or trainer[i][2][0] - margin > user[i][2][0]:
                point_np[i][2][2] = 1

            elif trainer[i][3][1] + margin < user[i][3][1] or trainer[i][3][1] - margin > user[i][3][1]:
                point_np[i][3][2] = 1

            elif trainer[i][4][1] + margin > user[i][4][1] or trainer[i][4][1] - margin < user[i][4][1]:
                point_np[i][4][2] = 1
            else:
                point_np[i][2][2] = 0
                point_np[i][3][2] = 0
                point_np[i][4][2] = 0
            i = i + 1

    return point_np

def diffing1(trainer,user,exercise):
    recom, resize = frame_filtering(trainer,user) #recom : 누가 변화했는지, resize : 변화된 npy

    if recom == "trainer":
        trainer = resize
        anglenp = angle_difference(trainer,user,exercise)
        pointnp = point_difference(trainer,user,exercise)
        for a,b in zip(anglenp,pointnp):
            for i in range(0,18):
                if a[i][2] == 1 and b[i][2]==1:
                    user[i][2] = 1

    elif recom =='user':
        user = resize
        anglenp = angle_difference(trainer, user, exercise)
        pointnp = point_difference(trainer, user, exercise)
        for a,b in zip(anglenp,pointnp):
            for i in range(0,18):
                if a[i][2] == 1 and b[i][2]==1:
                    user[i][2] = 1

    else :
        anglenp = angle_difference(trainer, user, exercise)
        pointnp = point_difference(trainer, user, exercise)
        for a, b in zip(anglenp, pointnp):
            for i in range(0, 18):
                if a[i][2] == 1 and b[i][2] == 1:
                    user[i][2] = 1
    return user,trainer

def diffing2(trainer,user,exercise):
    recom, resize = frame_upscaling(trainer,user)

    if recom == "trainer":
        trainer = resize
        anglenp = angle_difference(trainer,user,exercise)
        pointnp = point_difference(trainer,user,exercise)
        for a,b in zip(anglenp,pointnp):
            for i in range(0,18):
                if a[i][2] == 1 and b[i][2]==1:
                    user[i][2] = 1
    elif recom =='user':
        user = resize
        anglenp = angle_difference(trainer, user, exercise)
        pointnp = point_difference(trainer, user, exercise)
        for a,b,c in zip(anglenp,pointnp,user):
            for i in range(0,18):
                if a[i][2] == 1.0 and b[i][2]==1.0:
                    c[i][2] = 1
    else :
        anglenp = angle_difference(trainer, user, exercise)
        pointnp = point_difference(trainer, user, exercise)
        for a, b in zip(anglenp, pointnp):
            for i in range(0, 18):
                if a[i][2] == 1 and b[i][2] == 1:
                    user[i][2] = 1
    return user,trainer

