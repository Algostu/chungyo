from pose_diff.util.Common import CocoColors, CocoPairsRender, CocoPart
import cv2
import numpy as np

thickness = 2
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1

class Screen:
    def __init__(self,point,score=0,angle=0,msg=0,height=720,width=1024):
        self.point = point
        self.angle = angle
        self.msg = msg
        self.height = height
        self.width = width
        self.score = score
        # Background 설정
        self.img = np.zeros((self.height, self.width, 3), np.uint8)

    # points: list, ex) points = [(x,y), (x1,y1), ...]
    def draw_human(self,point,form,option=0):
        centers = {}
        colors = {}
        score = []

        for idx, i in enumerate(point):
            body_partx = float(i[0])
            body_party = float(i[1])
            colors[idx] = int(i[2])  # colors list에 i의 color 삽입
            if option == 1:
                center = (int(body_partx), 720-int(body_party))
            else:
                center = (int(body_partx), int(body_party))

            centers[idx] = center
            if center == (0,0): #disable Trash value
                continue
            cv2.circle(self.img, center, 5, CocoColors[idx], thickness=3, lineType=8, shift=0)

        # draw line
        if form == 'Real_time':
            for pair_order, pair in enumerate(CocoPairsRender):
                if centers[pair[0]] == (0,720) or centers[pair[1]] == (0,720): #disable Trash value
                    continue
                cv2.line(self.img, centers[pair[0]], centers[pair[1]], CocoColors[pair_order], 3)
        else:
            for pair in CocoPairsRender:
                # colors 1 : red  , colors 2 : green
                if centers[pair[0]] == (0,0) or centers[pair[1]] == (0,0):  # disable Trash value
                    continue

                if colors[pair[0]] == 1 or colors[pair[1]] == 1:
                    score.append(-1)
                    cv2.line(self.img, centers[pair[0]], centers[pair[1]], (0,0,255) , 3)
                elif colors[pair[0]] == 2 or colors[pair[1]] == 2:
                    score.append(0)
                    cv2.line(self.img, centers[pair[0]], centers[pair[1]], (0,255,0) , 3)
                else:
                    score.append(0)
                    cv2.line(self.img, centers[pair[0]], centers[pair[1]], (255,255,255) , 3)

        val = score.count(-1)
        if val < 5:
            return 0
        else:
            return -1

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

    def display_score(self):
        location_x, location_y = 30, self.height-40
        location = (location_x, location_y)
        text = (f'Score : {round(self.score,2)}')
        cv2.putText(self.img, text, location, font, fontScale, (255, 255, 255), thickness)

    def display_msg(self):
        rlocation = [self.width - 400, self.height - 500]
        llocation = [30, self.height - 500]

        for a in self.msg:
            if a[0] < 5:
                cv2.putText(self.img, a[1], tuple(rlocation), font, fontScale, (255, 255, 255), thickness)
                rlocation[1] = rlocation[1] + 40
            else:
                cv2.putText(self.img, a[1], tuple(llocation), font, fontScale, (255, 255, 255), thickness)
                llocation[1] = llocation[1] + 40



    def display_angle(self,joint):
        # section = CocoPart(joint).name
        coordinate = self.point[joint]
        location_x, location_y = int(coordinate[0]), int(coordinate[1])

        if location_x == 0 and location_y == 0: #disable Trash value
            pass
        else:
            location = (location_x-50, location_y+30)
            text = f'{self.angle[joint]}'
            cv2.putText(self.img, text, location, font, 0.5, (255, 255, 255), 1)

    def get_img(self):
        return self.img

    def get_angle(self):
        return self.angle
