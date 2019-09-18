import numpy as np
import math
from pose_diff.util.Common import AnglePairs,AnglePart

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
    angle = round(angle,2)
    return angle


def get_angle(npyfile):
    """Using AnglePairs in coco, input the angle data in list of body part."""
    angle = []
    for b in range(len(npyfile)):
        uangle = [None] * 18
        for index, j in enumerate(AnglePairs):
            pointa = npyfile[b][j[0]]
            pointa = pointa[:2]
            pointb = npyfile[b][j[1]]
            pointb = pointb[:2]
            pointc = npyfile[b][j[2]]
            pointc = pointc[:2]
            uangle[AnglePart[index]] = (Calculate_angle(pointa, pointb, pointc))
        angle.append(uangle)
    return angle