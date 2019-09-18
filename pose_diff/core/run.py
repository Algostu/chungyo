from pose_diff.util.screen import Screen
from pose_diff.core.pose_diff_test import diffing_decreasing, diffing_increasing, diffing_angle
from pose_diff.core.calculate_angle import get_angle

import cv2
import numpy as np

if __name__ == '__main__':
    print("main")

class Video:
    def __init__(self,trainer_npy,user_npy,exercise,diffing,way,average,apply=True):
        trainer = np.load(trainer_npy)
        user = np.load(user_npy)
        # user = np.delete(user, np.s_[::2], 0)
        print(f'user frame {len(user)}')
        print(f'trainer frame {len(trainer)}')
        if apply == True:
            score_range = 100 / len(user)
            if diffing == 'increase':
                user, trainer = diffing_increasing(trainer, user, exercise, way)
            elif diffing == 'decrease':
                user,trainer = diffing_decreasing(trainer,user,exercise,way,average)

            else:
                print(f'You input wrong diffing like {diffing}. Just you can enter "increase", "decrease" ')
        if apply == 'Angle':
            user, score_range = diffing_angle(trainer,user,exercise)

        a = [k for k in range(0, 18)]
        length = int(len(user))
        accuracy = [i + 1 for i in range(length)]
        user_angle = get_angle(user)
        fps = [i + 1 for i in range(length)]
        times = [i + 1 for i in range(length)]
        msg = [i + 1 for i in range(length)]
        height = 536
        width = 953
        screens = []
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
        cv2.destroyAllWindows()

class Real_time:
    def __init__(self,npfile):
        points = np.load(npfile)
        a = [k for k in range(0, 18)]
        length = int(len(points))
        accuracy = [i + 1 for i in range(length)]
        angle = [i + 1 for i in range(length)] #[frame][part][value]
        fps = [i + 1 for i in range(length)]
        times = [i + 1 for i in range(length)]
        msg = [i + 1 for i in range(length)]
        height = 720
        width = 1024
        screens = []

        # make screen list
        for i in range(length):
            screens.append(
                Screen(points[i], accuracy[i], angle[i], fps[i], times[i], msg[i], height, width))  # 추후 수정, 높이 720, 너비 1024
        for screen in screens:
            # draw_human
            screen.draw_human(screen.point,"Real_time")
            if cv2.waitKey(100) == 27:
                break

            # display_things
            screen.display_accuracy()
            screen.display_times()
            screen.display_fps()
            screen.display_msg()
            for i in range(0, 18):
                screen.display_angle(i)
            # float screen
            cv2.imshow("imshow", screen.img)
        cv2.destroyAllWindows()
