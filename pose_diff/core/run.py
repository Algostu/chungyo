from pose_diff.util.screen import Screen
from pose_diff.core.pose_diffing import diffing_decreasing, diffing_increasing, diffing_angle
from pose_diff.core.calculate_angle import get_angle
from pose_diff.core.framecut import cut
import cv2
import numpy as np

class Video:
    def __init__(self,trainer_npy,user_npy,exercise=3,diffing='increase',way='round',average=1,apply=True):
        trainer_full = np.load(trainer_npy)
        user_full = np.load(user_npy)
        usercut = cut.getCut(user_full).get_frame_number()
        trainercut = cut.getCut(trainer_full).get_frame_number()
        trainer_full = np.load(trainer_npy)
        user_full = np.load(user_npy)
        trainer = trainer_full[trainercut[0][0]:trainercut[0][1]]

        self.video_name = 'output.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(self.video_name, fourcc, 10, (1280, 720))

        for Ucut in usercut:
            screens = []
            print(f'UCTU  === {Ucut}')
            user = user_full[Ucut[0]:Ucut[1]+1]
            print(len(user))
            if apply == True:
                if diffing == 'increase':
                    user, trainer = diffing_increasing(trainer, user, exercise, way)
                elif diffing == 'decrease':
                    user,trainer = diffing_decreasing(trainer,user,exercise,way,average)
                else:
                    print(f'You input wrong diffing like {diffing}. Just you can enter "increase", "decrease" ')
                score_range = 100 / len(user)
            if apply == 'Angle':
                user, score_range = diffing_angle(trainer,user,exercise)

            length = len(user)
            accuracy = [i + 1 for i in range(length)]
            user_angle = get_angle(user)
            fps = [i + 1 for i in range(length)]
            times = [i + 1 for i in range(length)]
            msg = [i + 1 for i in range(length)]
            height = 720
            width = 1280
            score = 0

            # make screen list
            for i in range(length):
                screens.append(
                    Screen(user[i], accuracy[i], user_angle[i], fps[i], times[i], msg[i], height, width))  # 추후 수정, 높이 720, 너비 1024

            for index, screen in enumerate(screens):
                # draw_human
                val = screen.draw_human(screen.point,"Video")
                if cv2.waitKey(100) == 27:
                    break
                # display_things
                screen.display_accuracy()
                screen.display_times()
                screen.display_fps()
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
                cv2.imshow("imshow", screen.img)
                writer.write(screen.img)
        cv2.destroyAllWindows()

    def set_video_name(self,name):
        self.video_name = f'{name}.avi'


class Real_time:
    def __init__(self,npfile):
        user_full = np.load(npfile)
        usercut = getCut(user_full).get_frame_number()
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
                print(i)
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
