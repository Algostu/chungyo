from pose_diff.util.Common import CocoColors, CocoPairsRender, CocoPart
import cv2
import numpy as np

thickness = 1
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.6

# 동영상으로 저장할 수 있는 옵션 생성
class Screen:
    def __init__(self,point,accuracy=None,angle=None,fps=None,times=None,msg=None,height=None,width=None):
        self.point = point
        self.accuracy = accuracy
        self.angle = angle
        self.fps = fps
        self.times = times
        self.msg = msg
        self.height = height
        self.width = width
        # Background 설정
        self.img = np.zeros((self.height, self.width, 3), np.uint8)

        pass

    # points: list, ex) points = [(x,y), (x1,y1), ...]
    def draw_human(self,point,form):
        centers = {}
        colors = {}
        num = 0
        for i in point:
            body_partx = float(i[0])
            body_party = float(i[1])
            colors[num] = int(i[2])  # colors list에 i의 color 삽입
            center = (int(body_partx*0.002*self.width), 300-int(body_party*0.002*self.height))

            centers[num] = center
            if center == (0,300): #disable Trash value
                num = num + 1
                continue
            cv2.circle(self.img, center, 5, CocoColors[num], thickness=3, lineType=8, shift=0)
            num = num + 1

        # draw line
        if form == 'Real_time':
            for pair_order, pair in enumerate(CocoPairsRender):
                if centers[pair[0]] == (0,300) or centers[pair[1]] == (0,300): #disable Trash value
                    continue
                cv2.line(self.img, centers[pair[0]], centers[pair[1]], CocoColors[pair_order], 3)
        else:
            for pair in CocoPairsRender:
                # colors 1 : red  , colors 0 : green
                if centers[pair[0]] == (0, 300) or centers[pair[1]] == (0, 300):  # disable Trash value
                    continue

                if colors[pair[0]] == 1 and colors[pair[1]] == 1:
                    cv2.line(self.img, centers[pair[0]], centers[pair[1]], (0,0,255) , 3)
                elif colors[pair[0]] == 0 and colors[pair[1]] == 0:
                    cv2.line(self.img, centers[pair[0]], centers[pair[1]], (0,255,0) , 3)
                else:
                    cv2.line(self.img, centers[pair[0]], centers[pair[1]], (255,255,255) , 3)
        for a in colors:
            if a == 1:
                return -1
            else:
                return 0

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

    def display_score(self,score):
        location_x, location_y = 30, self.height-40
        location = (location_x, location_y)
        text = (f'Score : {round(score,2)}')
        cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def display_index(self,index):
        location_x, location_y = 30, self.height-80
        location = (location_x, location_y)
        text = f'Frame {index}'
        cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def display_angle(self,joint):
        section = CocoPart(joint).name
        coordinate = self.point[joint]
        location_x, location_y = int(coordinate[0]*0.002*self.width), 300-int(coordinate[1]*0.002*self.height)

        if location_x == 0 and location_y == 0: #disable Trash value
            pass
        else:
            location = (location_x-50, location_y+30)
            # text = f'{section} {self.angle[joint]}'
            text = f'{self.angle[joint]}'
            cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def get_img(self):
        return self.img

    def get_angle(self):
        return self.angle
