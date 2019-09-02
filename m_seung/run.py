from m_seung.screen import Screen
from m_seung.pose_diff import angle_difference
import cv2
import numpy as np

if __name__ == '__main__':
    img = "image.jpg"
    # points = np.load("skeleton1.npy")
    exercise = 'pullup'
    points = angle_difference(exercise)
    length = int(len(points))
    accuracy = [i+1 for i in range(length)]
    angle = [i + 1 for i in range(length)]
    fps = [i + 1 for i in range(length)]
    times = [i + 1 for i in range(length)]
    msg = [i + 1 for i in range(length)]
    height = 720
    width = 1024
    screens = []
    #make screen list
    for i in range(length):
        screens.append(Screen(points[i],accuracy[i],angle[i],fps[i],times[i],msg[i],height,width)) #추후 수정, 높이 720, 너비 1024

    for screen in screens:
        #draw_human
        screen.draw_human(screen.point)
        if cv2.waitKey(100) == 27:
            break
        #display_things
        screen.display_accuracy()
        screen.display_times()
        screen.display_fps()
        screen.display_msg()
        for i in range(0,18):
            screen.display_angle(i)

        #float screen
        cv2.imshow("imshow", screen.img)
    cv2.destroyAllWindows()

class run:
    def __init__(self,npfile):
        img = "image.jpg"
        points = np.load(npfile)
        exercise = 'pullup'
        # points = angle_difference(exercise)
        length = int(len(points))
        accuracy = [i + 1 for i in range(length)]
        angle = [i + 1 for i in range(length)]
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
<<<<<<< Updated upstream
            screen.draw_human(screen.point)
            if cv2.waitKey(1000) == 27:
=======
            screen.draw_human(screen.point,"Real_time")
            if cv2.waitKey(100) == 27:
>>>>>>> Stashed changes
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
