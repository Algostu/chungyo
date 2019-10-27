from pose_diff.util.screen import Screen
from pose_diff.core.pose_diffing import diffing_decreasing, diffing_increasing, diffing_angle
from pose_diff.core.calculate_angle import get_angle
from pose_diff.core.framecut import cut
import cv2
import numpy as np

class Video:
    def __init__(self,trainer_npy,user_npy, video_name, exercise=2,diffing='increase',way='round',average=1,apply=True):
        trainer = np.load(trainer_npy)
        user_full = np.load(user_npy)
        usercut = cut().getCut(user_full)
        user_full = np.load(user_npy)

        self.video_name = video_name
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(self.video_name, fourcc, 10, (1280, 720))

        score = 0
        index = 0

        for Ucut in usercut:
            screens = []
            user = user_full[Ucut[0]:Ucut[1]+1]
            if apply == True:
                if diffing == 'increase':
                    user, trainer = diffing_increasing(trainer, user, exercise, way)
                elif diffing == 'decrease':
                    user,trainer = diffing_decreasing(trainer,user,exercise,way,average)
                else:
                    print(f'You input wrong diffing like {diffing}. Just you can enter "increase", "decrease" ')
            if apply == 'Angle':
                user, score_range = diffing_angle(trainer,user,exercise)
            cnt = len(usercut)
            length = len(user)
            user_angle = get_angle(user)
            msg = [i + 1 for i in range(length)]
            height = 720
            width = 1280
            score_range = (100/cnt)/length


            # make screen list
            for i in range(length):
                screens.append(
                    Screen(user[i], user_angle[i], msg[i], height, width))  # 추후 수정, 높이 720, 너비 1024

            for screen in screens:
                # draw_human
                val = screen.draw_human(screen.point,"Video")
                if cv2.waitKey(100) == 27:
                    break
                # display_things
                index = index + 1
                screen.display_index(index)

                # display things-score
                if val == -1:
                    screen.display_score(score)
                else:
                    score = score + score_range
                    screen.display_score(score)

          # display_things-angle
                angle = screen.get_angle()
                for i in range(0, 18):
                    if angle[i] == None:
                        continue
                    screen.display_angle(i)

                # float screen
                # cv2.imshow("imshow", screen.img)
                writer.write(screen.img)
        cv2.destroyAllWindows()

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

def make_skeleton_image(npy,image_name):
    screen  = Screen(npy, height=720, width=1280)
    screen.draw_human(screen.point,"Real_time")
    cv2.imwrite(image_name, screen.img)
    while(1):
        cv2.imshow("SKEf",screen.img)
        if cv2.waitKey(100) == 27:
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    a = './../../temp/upgraded.npy'
    b = "./../../temp/exercise_numpy.npy"
    Video(a,b,'hi')
