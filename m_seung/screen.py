import coco as Coco
from coco import CocoPart
import cv2
import numpy as np

if __name__ == '__main__':
    print("main.py")

thickness = 1
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.6

class Screen:
    def __init__(self,point,accuracy,angle,fps,times,msg,height,width):
        self.point = point
        self.accuracy = accuracy
        self.angle = angle
        self.fps = fps
        self.times = times
        self.msg = msg
        self.height = height
        self.width = width
        self.img = np.zeros((self.height, self.width, 3), np.uint8)  # 현재는 그냥 검은 bg.
        pass

    # points: list, ex) points = [(x,y), (x1,y1), ...]
    def draw_human(self,point):
        centers = {}
        colors = {}
        num = 0
        for i in point:
            body_partx = float(i[0])
            body_party = float(i[1])
            colors[num] = int(i[2])  # colors list에 i의 color 삽입
            center = (int(body_partx*0.001*self.width), int(body_party*0.001*self.height))
            centers[num] = center
            if center == (0,0): #disable Trash value
                num = num + 1
                continue
            cv2.circle(self.img, center, 10, Coco.CocoColors[num], thickness=3, lineType=8, shift=0)
            num = num + 1

        # draw line
        for pair_order, pair in enumerate(Coco.CocoPairsRender):
            # colors 1 : Green  , colors 0 : Red
            if centers[pair[0]] == (0,0) or centers[pair[1]] == (0,0): #disable Trash value
                continue
            # if colors[pair_order] == 1:
            #     cv2.line(self.img, centers[pair[0]], centers[pair[1]], (0,255,0) , 3)
            # elif colors[pair_order] == 0:
            #     cv2.line(self.img, centers[pair[0]], centers[pair[1]], (0,0,255) , 3)
            # else:
            #     cv2.line(self.img, centers[pair[0]], centers[pair[1]], (255,255,255) , 3)

            cv2.line(self.img, centers[pair[0]], centers[pair[1]], Coco.CocoColors[pair_order], 3)

    def display_accuracy(self):
        location_x, location_y = self.width - 140, 30
        location = (location_x, location_y)
        text = str.format("accuracy %d" % (self.accuracy))
        cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def display_fps(self):
        location_x, location_y = self.width - 140, 60
        location = (location_x, location_y)
        text = str.format("fps %d" % (self.fps))
        cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def display_times(self):
        location_x, location_y = self.width - 140, 90
        location = (location_x, location_y)
        text = str.format("times %d" % (self.times))
        cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def display_msg(self):
        location_x, location_y = 30, self.height-40
        location = (location_x, location_y)
        text = str.format("MSG_LINE : Try Harder!")
        cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def display_angle(self,joint):
        section = CocoPart(joint).name
        coordinate = self.point[joint]
        location_x, location_y = int(coordinate[0]*0.001*self.width), int(coordinate[1]*0.001*self.height)

        if location_x == 0 and location_y == 0: #disable Trash value
            pass
        else:
            location = (location_x-50, location_y+30)
            text = str.format("%s %d" % (section, self.angle))
            cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def get_img(self):
        return self.img