import cv2
import numpy as np
from pose_diff.core.pose_diffing import point_difference, angle_difference, diffing_increasing
from pose_diff.core.run import Video
from pose_diff.util.Common import CocoColors, CocoPairsRender

# origin_name = 'test_data2/standard_user.npy'
# trained_name = 'test_data2/standard_user.npy'
origin_name = 'test_data2/standard_user.npy'
trained_name = 'test_data2/standard_user.npy'
origin = np.load(origin_name)
cut_origin = origin[:40]
trained = np.load(trained_name)
trained = trained[3:49]

def play_diffing_increasing():
    feedback, parts_gap, angle_gap, point_gap, user, trainer = diffing_increasing(trained,origin,2,'round')
    play_skeleton(user)

def play_point_difference():
    feedback, parts, gap, pointnp = point_difference(trained, origin, 2)
    play_skeleton(pointnp)
    # print(pointnp[0])
    # print(gap)
    return gap

def play_angle_difference():
    gap, anglenp = angle_difference(trained,origin,2)
    play_skeleton(anglenp)
    return gap

def langth():
    print(f'origin length = {len(cut_origin)}')
    print(f'trained length = {len(trained)}')

def draw_human(point,option=0):
    img = np.zeros((720,1024, 3), np.uint8)
    centers = {}
    colors = {}
    for idx, i in enumerate(point):
        body_partx = float(i[0])
        body_party = float(i[1])
        colors[idx] = int(i[2])  # colors list에 i의 color 삽입
        if option == 1:
            center = (int(body_partx), 720-int(body_party))
        else:
            center = (int(body_partx), int(body_party))
        centers[idx] = center
        if center == (0,0) or center == (0,720): #disable Trash value
            continue
        cv2.circle(img, center, 5, CocoColors[idx], thickness=3, lineType=8, shift=0)

    # draw line
    for pair in CocoPairsRender:
        # colors 1 : red  , colors 2 : green
        if centers[pair[0]] == (0,0) or centers[pair[1]] == (0,0)\
                or centers[pair[0]] == (0,720) or centers[pair[1]] == (0,720):  # disable Trash value
            continue
        if colors[pair[0]] == 1 or colors[pair[1]] == 1:
            cv2.line(img, centers[pair[0]], centers[pair[1]], (0,0,255) , 3)
        elif colors[pair[0]] == 2 or colors[pair[1]] == 2:
            cv2.line(img, centers[pair[0]], centers[pair[1]], (0,255,0) , 3)
        else:
            cv2.line(img, centers[pair[0]], centers[pair[1]], (255,255,255) , 3)

    return img

def play_skeleton(point):
    # while(True):
    #     if cv2.waitKey(100) == 27:
    #         break
    #     for a in point:
    #         img = draw_human(a)
    #         cv2.imshow("imshow", img)

    for a in point:
        if cv2.waitKey(100) == 27:
            break
        img = draw_human(a)
        cv2.imshow("imshow", img)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # a = [[(1,2)],[2],[3],[4]]
    # b = [[(3,4)],[2],[3],[4]]
    #
    # a = np.array(a)
    # b = np.array(b)
    # c = np.hstack([a,b])
    # print(a)
    # # print(c)
    #
    # f = [tuple((0,0)) for i in range(18)]
    # f = np.array(f)
    # print(f)

    Video(trained_name, origin_name, 'hello.avi')