from screen import Screen
import cv2
import numpy as np

if __name__ == '__main__':
    img = "image.jpg"
    points = np.load("skeleton.npy")
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
        screen.display_angle(3)
        #float screen
        cv2.imshow("imshow", screen.img)
    cv2.destroyAllWindows()
