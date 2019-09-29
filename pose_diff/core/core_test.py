import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import  numpy as np
import cv2

from pose_diff.util.Common import CocoColors, CocoPairsRender

class Testclass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.score = 100

    def set_score(self):
        self.score = self.score - 1

class Video:
    def __init__(self,user):
        height = 536
        width = 953
        self.img = np.zeros((height, width, 3), np.uint8)
        centers = {}
        colors = {}
        num = 0
        for i in user:
            body_partx = float(i[0])
            body_party = float(i[1])
            colors[num] = int(i[2])  # colors list에 i의 color 삽입
            center = (int(body_partx * 0.1* width), 300 - int(body_party * 0.1* height))

            centers[num] = center
            if center == (0, 300):  # disable Trash value
                num = num + 1
                continue
            cv2.circle(self.img, center, 5, CocoColors[num], thickness=3, lineType=8, shift=0)
            num = num + 1

        for pair_order, pair in enumerate(CocoPairsRender):
            if centers[pair[0]] == (0, 300) or centers[pair[1]] == (0, 300):  # disable Trash value
                continue
            cv2.line(self.img, centers[pair[0]], centers[pair[1]], CocoColors[pair_order], 3)
#Todo make Video file in screen.py
if __name__ == '__main__':
    # user_dir = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/user/IU/walk/trained_skeleton.npy'
    # trainer_dir = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/user/IU/walk/trained_skeleton.npy'
    user_dir = 'C:/Users/Rhcsky/Desktop/SW_developer/pose-difference/data/output/1-2/numpy/result.npy'
    user = np.load(user_dir)
    video  = []
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter('output.avi',fourcc,10,(5000,5000))
    for i in user:
        Video(i)
        if cv2.waitKey(100) == 27:
            break
        cv2.imshow("imshow", Video(i).img)
        writer.write(Video(i).img)
    cv2.destroyAllWindows()
