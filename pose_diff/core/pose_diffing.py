import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np
import math
from pose_diff.util.Common import Parts, AnglePart
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
    gap = []
    trainer_angle = get_angle(trainer)
    user_angle = get_angle(user)
    # Error in RED = 1, Success in GREEN = 2
    if exercise == 0:
        print("Exercise type is squat")
        pass
    if exercise == 1:
        print("Exercise type is pull_up")
        pass
    if exercise == 2:
        for pidx, angle in enumerate(angle_np):
            sum_gap = 0
            for idx, part in enumerate(AnglePart):
                if (trainer_angle[pidx][idx] == None or user_angle[pidx][idx] == None):
                    continue
                sum_gap = sum_gap + setting_relative_error(trainer_angle[pidx][idx],user_angle[pidx][idx])
                if setting_relative_error(trainer_angle[pidx][idx],user_angle[pidx][idx]) > margin:
                    angle[idx][2] = 1
                else:
                    angle[idx][2] = 2
            else:
                angle[idx][2] = 0
            gap.append(sum_gap)
    return gap, angle_np

def point_difference(trainer, user, exercise):
    """
    For calculate point diffing. This def to set difference using relative error of points in each axis x, y.
    List parts is stored the difference each parts, and list gap is stored the difference of all points for scoring.
    :param trainer: trainer's loaded npy
    :param user: user's loaded npy
    :param exercise: Thing what you want to diffing.
    :return: parts, gap, point_np
    """
    point_np = np.copy(user)
    margin = 4
    gap = []
    parts= [[] for i in range(18)]
    feedbacks = []
    # Error in RED = 1, Success in GREEN = 2
    if exercise == 0:
        print("Exercise type is Walk")
        pass
    if exercise == 1:
        print("Exercise type is pull_up")
        pass
    if exercise == 2:
        from pose_diff.util.Common import FeedbackParts, PART_NAMES
        for pidx, point in enumerate(point_np): #Frame
            feedback = []
            sum_gap = 0
            for idx, part in enumerate((Parts[exercise])): #Body_parts
                if part == 0.5:
                    difference = (round(trainer[pidx][idx][0]-user[pidx][idx][0],2),round(trainer[pidx][idx][1] - user[pidx][idx][1],2))
                    parts[idx].append(difference)
                    sum_gap = sum_gap + setting_relative_error(trainer[pidx][idx][0],user[pidx][idx][0])
                    if (setting_relative_error(trainer[pidx][idx][0],user[pidx][idx][0])\
                        + setting_relative_error(trainer[pidx][idx][1],user[pidx][idx][1]))/2> margin:

                        if FeedbackParts[exercise][idx] == 0.5:
                            if difference[0] < -30:
                                feedback.append([idx , f'Bend over your {PART_NAMES[idx]}'])
                            elif difference[0] > 30:
                                feedback.append([idx, f'Stretch your {PART_NAMES[idx]}'])
                            if difference[1] < -30:
                                feedback.append([idx, f'Upper your {PART_NAMES[idx]}'])
                            elif difference[1] > 30:
                                feedback.append([idx, f'Lower your {PART_NAMES[idx]}'])

                        point[idx][2] = 1
                    else:
                        point[idx][2] = 2
                else:
                    point[idx][2] = 0
            feedbacks.append(feedback)
            gap.append(sum_gap)
    return feedbacks,parts, gap, point_np

def diffing_decreasing(trainer,user,exercise,way,average):
    recom, resize = frame_decreasing(trainer,user,way,average) #recom : 누가 변화했는지, resize : 변화된 npy
    check_times=0
    if recom == "trainer":
        trainer = resize
        angle_gap, anglenp = angle_difference(trainer,user,exercise)
        feedback, parts_gap, point_gap, pointnp = point_difference(trainer,user,exercise)
        for a,b,c in zip(anglenp,pointnp,user):
            for i in range(0,18):
                if a[i][2] == 1 or b[i][2]==1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1

    elif recom =='user':
        user = resize
        angle_gap, anglenp = angle_difference(trainer, user, exercise)
        feedback, parts_gap, point_gap, pointnp = point_difference(trainer, user, exercise)
        for a, b, c in zip(anglenp, pointnp, user):
            for i in range(0, 18):
                if a[i][2] == 1 or b[i][2] == 1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1

    else :
        angle_gap, anglenp = angle_difference(trainer, user, exercise)
        feedback, parts_gap, point_gap, pointnp = point_difference(trainer, user, exercise)
        for a, b, c in zip(anglenp, pointnp, user):
            for i in range(0, 18):
                if a[i][2] == 1 or b[i][2] == 1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1
    return feedback, parts_gap, angle_gap, point_gap, user, trainer

def diffing_increasing(trainer,user,exercise,way):
    recom, resize = frame_increasing(trainer,user,way)
    check_times = 0
    if recom == "trainer":
        trainer = resize
        angle_gap, anglenp = angle_difference(trainer, user, exercise)
        feedback, parts_gap, point_gap, pointnp = point_difference(trainer, user, exercise)
        for a, b, c in zip(anglenp, pointnp, user):
            for i in range(0, 18):
                if a[i][2] == 1 or b[i][2] == 1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1
    elif recom =='user':
        user = resize
        angle_gap, anglenp = angle_difference(trainer, user, exercise)
        feedback, parts_gap, point_gap, pointnp = point_difference(trainer, user, exercise)
        for a,b,c in zip(anglenp,pointnp,user):
            for i in range(0,18):
                if a[i][2] == 1 or b[i][2]==1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1

    else :
        angle_gap, anglenp = angle_difference(trainer, user, exercise)
        feedback, parts_gap, point_gap, pointnp = point_difference(trainer, user, exercise)
        for a, b, c in zip(anglenp, pointnp, user):
            for i in range(0, 18):
                if a[i][2] == 1 or b[i][2] == 1:
                    c[i][2] = 1
                if a[i][2] == 2 or b[i][2] == 2:
                    c[i][2] = 2
                    check_times = check_times + 1
    return feedback, parts_gap, angle_gap, point_gap, user, trainer

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