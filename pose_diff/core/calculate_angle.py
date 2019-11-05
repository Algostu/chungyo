import math

import numpy as np
from pose_diff.util.Common import AnglePairs, AnglePart


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
            pointaa = pointa[:2]
            pointb = npyfile[b][j[1]]
            pointbb = pointb[:2]
            pointc = npyfile[b][j[2]]
            pointcc = pointc[:2]
            uangle[AnglePart[index]] = (Calculate_angle(pointaa, pointbb, pointcc))
        angle.append(uangle)
    return angle

def get_angle_part(part,video_name):  #video를 skeleton1.npy라 가정한다.
    # body=[]
    # body=('Neck','RShoulder','RElbow','RWrist','LShoulder','LElbow',
    #       'LWrist','RHip','RKnee','RAnkle','LHip','LKnee','LAnkle','REye','LEye','REar','LEar','Background')
    parts=[]
    frame = np.load(video_name)
    if part==1: #left arm
        parts=[0,4,5]
    elif part==2: #left elbow
        parts=[4,5,6]
    elif part==3: # R arm-
        parts=[0,1,2]
    else : # R elbow  part==4 라고 가정
        parts=[1,2,3]


    angle=[]
    for i in range(len(frame)):
        result_angle=Calculate_angle(
        [frame[i][parts[0]][0],frame[i][parts[0]][1]],[frame[i][parts[1]][0],frame[i][parts[1]][1]],[frame[i][parts[2]][0],frame[i][parts[2]][1]])
        if (frame[i][parts[1]][0] - frame[i][parts[0]][0]) == 0:
            continue
        if ((frame[i][parts[1]][1] - frame[i][parts[0]][1]) / (frame[i][parts[1]][0] - frame[i][parts[0]][0])) * (frame[i][parts[2]][0] - frame[i][parts[0]][0]) + frame[i][parts[0]][1] < frame[i][parts[2]][1]:
            result_angle = 360 - result_angle
        angle.append(result_angle)

    return angle
