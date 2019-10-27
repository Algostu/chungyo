import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np
import math
from pose_diff.util.Common import Parts
from pose_diff.core.calculate_angle import get_angle

def setting_relative_error(trainer_val,user_val):
    return float(abs(trainer_val-user_val)/trainer_val * 100)

def average_frames_decreasing(frame, resize, split, cnt1, cnt2, way): #cnt2가 0부터 끝까지 split만큼 증가
    aver = np.zeros((18,3))
    if way == 'round':
        for i in range(cnt2,round(cnt2 + split * cnt1)):
            if i == len(frame):
                break
            aver = aver + frame[i]
        resize[cnt1] = aver
        return resize

    elif way == 'round_up':
        for i in range(cnt2,math.ceil(cnt2 + split * cnt1)):
            if i == len(frame):
                break
            aver = aver + frame[i]
        resize[cnt1] = aver
        return resize

    elif way == 'round_down':
        for i in range(cnt2,math.floor(cnt2 + split * cnt1)):
            if i == len(frame):
                break
            aver = aver + frame[i]
        resize[cnt1] = aver
        return resize

    else:
        print(f'Wrong way, there are three ways. rounding, round_up, round_down')
        sys.exit

def frame_decreasing(trainer,user,way,average): #frame resizing

    user_frame = len(user)
    trainer_frame = len(trainer)

    if trainer_frame > user_frame:
        recom = "trainer"
        resize = np.zeros(user.shape)
        split = trainer_frame / user_frame
        cnt1=0
        cnt2=0
        while cnt2 < trainer_frame-1:
            if way == 'round':
                if average == 1:
                    cnt1 = cnt1 + 1
                    resize = average_frames_decreasing(trainer, resize, split, cnt1, cnt2,way)
                    cnt2 = round(cnt2 + split * cnt1)
                elif average ==0:
                    cnt2 = round(cnt2 + split * cnt1)
                    resize[cnt1] = trainer[cnt2]
                    cnt1 = cnt1 + 1
                else:
                    print(f'average must be 1 or 0, 1 is application and 0 is non application. \nyou enter the average as {average}')

            elif way == 'round_up':
                if average == 1:
                    cnt1 = cnt1 + 1
                    resize = average_frames_decreasing(trainer, resize, split, cnt1, cnt2, way)
                    cnt2 = math.ceil(cnt2 + split * cnt1)
                elif average == 0:
                    split = math.ceil(split)
                    cnt2 = cnt2 + split*cnt1
                    resize[cnt1] = trainer[cnt2]
                    cnt1 = cnt1 + 1
                else:
                    print(f'average must be 1 or 0, 1 is application and 0 is non application. \nyou enter the average as {average}')

            elif way == 'round_down':
                if average == 1:
                    cnt1 = cnt1 + 1
                    resize = average_frames_decreasing(trainer, resize, split, cnt1, cnt2, way)
                    cnt2 = math.floor(cnt2 + split * cnt1)
                elif average == 0:
                    split = math.floor(split)
                    cnt2 = cnt2 + split * cnt1
                    resize[cnt1] = trainer[cnt2]
                    cnt1 = cnt1 + 1
                else:
                    print(f'average must be 1 or 0, 1 is application and 0 is non application. \nyou enter the average as {average}')
            else:
                print(f'Wrong way, there are three ways. rounding, round_up, round_down')

    elif trainer_frame < user_frame:
        recom = "user"
        resize = np.zeros(trainer.shape)
        split = user_frame / trainer_frame
        cnt1 = 0
        cnt2 = 0
        while cnt2 < user_frame-1:
            if way == 'round':
                if average == 1:
                    cnt1 = cnt1 + 1
                    resize = average_frames_decreasing(user, resize, split, cnt1, cnt2,way)
                    cnt2 = round(cnt2 + split * cnt1)
                elif average ==0:
                    cnt2 = round(cnt2 + split * cnt1)
                    resize[cnt1] = user[cnt2]
                    cnt1 = cnt1 + 1
                else:
                    print(f'average must be 1 or 0, 1 is application and 0 is non application. \nyou enter the average as {average}')

            elif way == 'round_up':
                if average == 1:
                    cnt1 = cnt1 + 1
                    resize = average_frames_decreasing()(user, resize, split, cnt1, cnt2, way)
                    cnt2 = math.ceil(cnt2 + split * cnt1)
                elif average == 0:
                    split = math.ceil(split)
                    cnt2 = cnt2 + split*cnt1
                    resize[cnt1] = user[cnt2]
                    cnt1 = cnt1 + 1
                else:
                    print(f'average must be 1 or 0, 1 is application and 0 is non application. \nyou enter the average as {average}')

            elif way == 'round_down':
                if average == 1:
                    cnt1 = cnt1 + 1
                    resize = average_frames_decreasing()(user, resize, split, cnt1, cnt2, way)
                    cnt2 = math.floor(cnt2 + split * cnt1)
                elif average == 0:
                    split = math.floor(split)
                    cnt2 = cnt2 + split * cnt1
                    resize[cnt1] = user[cnt2]
                    cnt1 = cnt1 + 1
                else:
                    print(f'average must be 1 or 0, 1 is application and 0 is non application. \nyou enter the average as {average}')
            else:
                print(f'Wrong way, there are three ways. rounding, round_up, round_down')
    else:
       recom = "no"
       resize = "no"
    return recom, resize

def frame_increasing(trainer,user,way): #make bigger the fewer frame
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
            if way =='round':
                for i in range(round(split * num), round(split * (num + 1))):
                    resize[i] = user[num]
                num = num + 1
            elif way =='round_up':
                for i in range(math.ceil(split * num), math.ceil(split * (num + 1))):
                    resize[i] = user[num]
                num = num + 1
            elif way == 'round_down':
                for i in range(math.floor(split * num), math.floor(split * (num + 1))):
                    resize[i] = user[num]
                num = num + 1
            else:
                print(f'Wrong way, there are three ways. rounding, round_up, round_down')

    elif trainer_frame < user_frame:
        recom = "trainer"
        resize = np.zeros(user.shape)
        split = user_frame / trainer_frame
        num = 0
        while 1:
            if num == trainer_frame:
                break
            if way =='round':
                for i in range(round(split * num), round(split * (num + 1))):
                    resize[i] = trainer[num]
                num = num + 1
            elif way =='round_up':
                for i in range(math.ceil(split * num), math.ceil(split * (num + 1))):
                    resize[i] = trainer[num]
                num = num + 1
            elif way == 'round_down':
                for i in range(math.floor(split * num), math.floor(split * (num + 1))):
                    resize[i] = trainer[num]
                num = num + 1
            else:
                print(f'Wrong way, there are three ways. rounding, round_up, round_down')
    else:
        recom = "no"
        resize = "no"
    return recom, resize

def angle_difference(trainer,user,exercise):
    angle_np = np.copy(user)
    margin = 10
    trainer_angle = get_angle(trainer)
    user_angle = get_angle(user)
    # Error in RED = 1, Success in GREEN = 2
    if exercise == 0:
        print("Exercise type is squat")
        pass
    if exercise == 1:
        print("Exercise type is shoulder_press")
        pass
    if exercise == 2:
        i = 0
        while True:
            if i > len(user) - 1:
                break
            for idx, part in enumerate(Parts[exercise]):
                if part >= 0.5:
                    if (trainer_angle[i][idx] == None or user_angle[i][idx] == None):
                        continue
                    if setting_relative_error(trainer_angle[i][idx],user_angle[i][idx]) < margin:
                        angle_np[i][idx][2] = 1
                    else:
                        angle_np[i][idx][2] = 2
                else:
                    angle_np[i][idx][2] = 0
            i = i+1
    return angle_np

def point_difference(trainer, user, exercise):
    point_np = np.copy(user)
    margin = 10
    gap = []
    # Error in RED = 1, Success in GREEN = 2
    if exercise == 0:
        print("Exercise type is Walk")
        pass
    if exercise == 1:
        print("Exercise type is shoulder_press")
        pass
    if exercise == 2:
        i = 0
        while True:
            sum_gap = 0
            if i > len(user) - 1:
                break
            for idx, part in enumerate(Parts[exercise]):
                if part >= 0.5:
                    if trainer[i][idx][0] == 0:
                        continue
                    sum_gap = sum_gap + setting_relative_error(trainer[i][idx][0],user[i][idx][0])
                    if setting_relative_error(trainer[i][idx][0],user[i][idx][0]) > margin:
                        point_np[i][idx][2] = 1
                    else:
                        point_np[i][idx][2] = 2
                else:
                    point_np[i][idx][2] = 0
            i = i + 1
            gap.append(sum_gap)
    return gap, point_np

def diffing_decreasing(trainer,user,exercise,way,average):
    recom, resize = frame_decreasing(trainer,user,way,average) #recom : 누가 변화했는지, resize : 변화된 npy
    check_times=0
    if recom == "trainer":
        trainer = resize
        anglenp = angle_difference(trainer,user,exercise)
        gap, pointnp = point_difference(trainer,user,exercise)
        for a,b,c in zip(anglenp,pointnp,user):
            for i in range(0,18):
                if a[i][2] == 1 or b[i][2]==1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1

    elif recom =='user':
        user = resize
        anglenp = angle_difference(trainer, user, exercise)
        gap, pointnp = point_difference(trainer, user, exercise)
        for a, b, c in zip(anglenp, pointnp, user):
            for i in range(0, 18):
                if a[i][2] == 1 or b[i][2] == 1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1

    else :
        anglenp = angle_difference(trainer, user, exercise)
        gap, pointnp = point_difference(trainer, user, exercise)
        for a, b, c in zip(anglenp, pointnp, user):
            for i in range(0, 18):
                if a[i][2] == 1 or b[i][2] == 1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1
    return gap, user, trainer

def diffing_increasing(trainer,user,exercise,way):
    recom, resize = frame_increasing(trainer,user,way)
    check_times = 0
    if recom == "trainer":
        trainer = resize
        anglenp = angle_difference(trainer,user,exercise)
        gap, pointnp = point_difference(trainer,user,exercise)
        for a, b, c in zip(anglenp, pointnp, user):
            for i in range(0, 18):
                if a[i][2] == 1 or b[i][2] == 1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1
    elif recom =='user':
        user = resize
        anglenp = angle_difference(trainer, user, exercise)
        gap, pointnp = point_difference(trainer, user, exercise)
        for a,b,c in zip(anglenp,pointnp,user):
            for i in range(0,18):
                if a[i][2] == 1 or b[i][2]==1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1

    else :
        anglenp = angle_difference(trainer, user, exercise)
        gap, pointnp = point_difference(trainer, user, exercise)
        for a, b, c in zip(anglenp, pointnp, user):
            for i in range(0, 18):
                if a[i][2] == 1 or b[i][2] == 1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1
    return gap, user,trainer

# it works well when user frame is more bigger than trainer frame
def diffing_angle(trainer, user, exercise):
    trainer_angle = get_angle(trainer)
    user_angle = get_angle(user)
    margin = 1

    #for scoring
    cnt = 0
    for idx, part in enumerate(Parts[exercise]):
        if part > 0.5:
            cnt = cnt + 1
    score_range = 100 / len(user_angle) * cnt

    rearrange_user = []
    rearrange_trainer = []
    for i in range(0,18):
        rearrange_user.append([x[i] for x in user_angle if x[i] is not None])
    for i in range(0,18):
        rearrange_trainer.append((x[i] for x in trainer_angle if x[i] is not None))

    for i in range(0,18):
        for idx, a in enumerate(rearrange_user[i]):
            for b in rearrange_trainer[i]:
                if a < b+margin and b - margin < a:
                    user[idx][i][2] = 0
                    break
    return user, score_range