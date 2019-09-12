import numpy as np
import math
from m_seung.coco import AnglePairs,AnglePart

def angle_between_vectors_degrees(u, v):
    """Return the angle between two vectors in any dimension space, in degrees."""
    return np.degrees(math.acos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))))

def Calculate_angle(point_a,point_b,point_c):
    """Calculate the angle of 3 points in latitude/longitude radians space"""
    a = np.radians(np.array(point_a))
    b = np.radians(np.array(point_b))
    c = np.radians(np.array(point_c))
    vec1 = a-b
    vec2 = c-b

    adjust = b[0]
    vec1[1] *= math.cos(adjust)
    vec2[1] *= math.cos(adjust)

    angle = angle_between_vectors_degrees(vec1,vec2)
    angle = round(angle)
    return angle

#리스트 초기화해서 AnglePart자리에 넣기.
def get_angle(trainer,user):
    trainer_angle = []
    user_angle = []
    for a in range(len(trainer)):
        tangle = [None] * 18
        for index, i in enumerate(AnglePairs):
            pointa = trainer[a][i[0]]
            pointa = pointa[:2]
            pointb = trainer[a][i[1]]
            pointb = pointb[:2]
            pointc = trainer[a][i[2]]
            pointc = pointc[:2]
            tangle[AnglePart[index]] = (Calculate_angle(pointa, pointb, pointc))
        trainer_angle.append(tangle)

    for b in range(len(user)):
        uangle = [None] * 18
        for index, j in enumerate(AnglePairs):
            pointa = user[b][j[0]]
            pointa = pointa[:2]
            pointb = user[b][j[1]]
            pointb = pointb[:2]
            pointc = user[b][j[2]]
            pointc = pointc[:2]
            uangle[AnglePart[index]] = (Calculate_angle(pointa, pointb, pointc))
        user_angle.append(uangle)
    return trainer_angle, user_angle