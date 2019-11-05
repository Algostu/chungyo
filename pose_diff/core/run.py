import cv2
import numpy as np
from pose_diff.core.calculate_angle import get_angle
from pose_diff.core.framecut import cut
from pose_diff.core.pose_diffing import diffing_decreasing, diffing_increasing, diffing_angle
from pose_diff.util.screen import Screen


class Video:
    def __init__(self,trainer_npy,user_npy, video_name, exercise=2,diffing='increase',way='round',average=1,apply=True):
        trainer = np.load(trainer_npy)
        user_full = np.load(user_npy)
        usercut = cut().getCut(user_full)
        user_full = np.load(user_npy)

        self.video_name = video_name
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(self.video_name, fourcc, 10, (1280, 720))

        cutframes = []
        scores = []
        gaps = []
        for Ucut in usercut:
            screens = []
            score = []
            user = user_full[Ucut[0]:Ucut[1]+1]
            # user = user_full

            if apply == True:
                if diffing == 'increase':
                    feedback, parts_gap, angle_gap, point_gap, user, trainer = diffing_increasing(trainer, user, exercise, way)
                elif diffing == 'decrease':
                    feedback, parts_gap, angle_gap, point_gap, user, trainer = diffing_decreasing(trainer,user,exercise,way,average)
                else:
                    print(f'You input wrong diffing like {diffing}. Just you can enter "increase", "decrease" ')
            if apply == 'Angle':
                user, score_range = diffing_angle(trainer,user,exercise)

            cutframes.append(user)
            for point, angle in zip(point_gap, angle_gap):
                if point > 100:
                    score_point = 0
                else:
                    score_point = (100 - point) / 2
                if angle > 360:
                    score_angle = 0
                else:
                    score_angle = ((360 - angle) / 360) * 100 / 2

                score.append(score_angle + score_point)
            gaps.append(parts_gap)
            scores.append(score)
            length = len(user)
            user_angle = get_angle(user)
            height = 720
            width = 1280
            # make screen list
            for i in range(length):
                screens.append(
                    Screen(user[i], score[i] ,user_angle[i], feedback[i], height, width))  # 추후 수정, 높이 720, 너비 1024

            for screen in screens:
                # draw_human
                val = screen.draw_human(screen.point,"Video")
                if cv2.waitKey(100) == 27:
                    break
                # display_things
                screen.display_score()
                screen.display_msg()
                # display_things-angle
                angle = screen.get_angle()
                for i in range(0, 18):
                    if angle[i] == None:
                        continue
                    screen.display_angle(i)

                # float screen
                cv2.imshow("imshow", screen.img)
                writer.write(screen.img)
        writer.release()
        cv2.destroyAllWindows()

        graph_numpy = [cutframes, scores, gaps]

        a = []
        b = [[] for i in range(6)]
        c = []
        for i in range(len(graph_numpy[0])):
            a += graph_numpy[1][i]
            for j in range(6):
                b[j] += graph_numpy[2][i][j+2] # left_shoulder
                # b[1] += graph_numpy[2][i][3] # left_elbow
                # b[2] += graph_numpy[2][i][4] # left_writst
                # b[3] += graph_numpy[2][i][5] # left_shoulder
                # b[4] += graph_numpy[2][i][6] # left_elbow
                # b[5] += graph_numpy[2][i][7] # left_writst
            c.append(graph_numpy[0][i])
        temp = [a, *b, c, scores]
        np.save("temp/graph.npy",temp)

    def set_video_name(self,name):
        self.video_name = f'{name}.avi'

class Real_time:
    def __init__(self,npfile):
        user_full = np.load(npfile)
        usercut = cut.getCut(user_full).get_frame_number()
        user_full = np.load(npfile)
        height = 720
        width = 1024
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter('output.avi', fourcc, 10, (1024,720))

        for Ucut in usercut:
            screens = []
            user = user_full[Ucut[0]:Ucut[1] + 1]
            length = int(len(user))
            accuracy = [i + 1 for i in range(length)]
            user_angle = get_angle(user)
            fps = [i + 1 for i in range(length)]
            times = [i + 1 for i in range(length)]
            msg = [i + 1 for i in range(length)]

            # make screen list
            for i in range(length):
                screens.append(
                    Screen(user[i], accuracy[i], user_angle[i], fps[i], times[i], msg[i], height, width))  # 추후 수정, 높이 720, 너비 1024

            for screen in screens:
                # draw_human
                screen.draw_human(screen.point,"Real_time")
                if cv2.waitKey(100) == 27:
                    break

                # display_things
                screen.display_accuracy()
                screen.display_times()
                screen.display_fps()

                # display_things-angle
                angle = screen.get_angle()
                for i in range(0, 18):
                    if angle[i] == None:
                        continue
                    screen.display_angle(i)

                # float screen
                cv2.imshow("imshow", screen.img)
                writer.write(screen.img)
        cv2.destroyAllWindows()

class human_pic:
    def __init__(self,user_npy, video_name):
        thickness = 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        user = user_npy

        self.video_name = video_name
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(self.video_name, fourcc, 10, (1280, 720))

        for a in user:
            screens = []
            screens.append(
                Screen(a, height=720, width=1280))
            for index, screen in enumerate(screens):
                # draw_human
                val = screen.draw_human(screen.point,"Real_time", 1)
                if cv2.waitKey(100) == 27:
                    break
                # display_things
                # cv2.imshow("imshow", screen.img)
                writer.write(screen.img)
        cv2.destroyAllWindows()

def make_skeleton_image(npy,image_name, option=1):
    thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    screen  = Screen(npy, height=720, width=1280)
    screen.draw_human(screen.point,"Real_time")

    location_x, location_y = 80, 80
    location = (location_x, location_y)
    text = f"Find initial pose successfully!"
    text2 = f"If you want to close, please push Esc key."
    cv2.putText(screen.img, text, location, font, fontScale, (255, 255, 255), thickness)
    cv2.putText(screen.img, text2, (80, 120), font, fontScale, (255, 255, 255), thickness)
    cv2.imwrite(image_name, screen.img)
    if option == 2:
        return
    while(True):
        cv2.imshow("Your Initial Pose",screen.img)
        if cv2.waitKey(100) == 27:
            break
    cv2.destroyAllWindows()
