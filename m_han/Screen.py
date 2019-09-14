import cv2
import numpy as np
from m_han.Common import CocoColors, CocoPairs, CocoPairsRender

class Screen():
    def __init__(self):
        pass

    def draw_humans(self,humans, imgcopy=False, frame=0, output_json_dir=None):
        # image = cv2.imread('m_han/test.png', cv2.IMREAD_COLOR)
        npimg = np.zeros((1024,620, 3), np.uint8)
        # print(image.shape)
        image_h, image_w = npimg.shape[:2]
        dc = {"people":[]}
        centers = {}

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi',fourcc, 20.0, (image_w, image_h))

        # for human in humans:
        for n, human in enumerate(humans):
            npimg = np.zeros((1024,620, 3), np.uint8)
            flat = [0.0 for i in range(36)]
            # draw point
            for i in range(18):
                body_part = human[i]
                center = (600-int(body_part[0]), -(int(body_part[1]) - 250))
                centers[i] = center
                # cv2.circle(npimg, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)
                #add x
                flat[i*2] = center[0]
                #add y
                flat[i*2+1] = center[1]
                cv2.circle(npimg, center, 3, CocoColors[i], thickness=3, lineType=8, shift=0)

            test = [(1, 2), (1, 5),(1, 8),(1, 11),(1, 0)]
            # (B, G, R)
            colors = [[128, 128, 0], [128, 128, 0], [0, 128, 128], [0, 128, 128],[64, 64, 64]]
            # draw line
            for pair_order, pair in enumerate(CocoPairsRender[:-4]):
                # npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
                cv2.line(npimg, centers[pair[0]], centers[pair[1]], colors[pair_order%5], 3)

            npimg = np.uint8(255 * npimg)
            out.write(npimg)

            cv2.imshow('analyze and train result', npimg)
            if cv2.waitKey(15) == 27:
                break

        out.release()

        cv2.destroyAllWindows()
        return npimg
