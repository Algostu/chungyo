'''
* Writer : daan
'''
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np
from m_han.parse import load_ps
from m_han.evaluate import evaluate_pose
#list1 = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5]])


standard = np.array([[1,1],[2,2],[1,1],[4,4],[6,6]])
human = np.array([[1,1],[2,5],[6,1],[9,4],[10,6]])
list = [0,1,2,3,4,5]
def create():
    a = np.zeros((5,3))
    for i in range(0,5):
        for j in range(0,2):
            a[i][j]=human[i][j]
            a[i][j + 1] = 255
    return a

def diffangle():
    pose_seq1 = load_ps("skeleton1.npy")
    pose_seq2 = load_ps("skeleton2.npy")
    x, y, z = evaluate_pose(pose_seq1, 'pullup')
    #print(x[0]) #한점에서 프레임당 달라진 각도
    user_x, user_y, user_z = evaluate_pose(pose_seq2, 'pullup')
    i=0

    while True:
        if (user_x[i] == None or user_y[i]==None or x[i]==None or y[i]==None or i == 120):
            break
        if (x[i]+4<user_x[i] or x[i]-4>user_x[i]):
            print("XXXXX")
        elif (y[i]+4<user_y[i] or y[i]-4>user_y[i]):
            print("YYYYY")
        else:
            print("blue")
        i= i+1
    print (i)

def diffpoint():

    a = create()

    for i in range (0,4):
        x,y = standard[i]
        q,w = human[i]
        if(x-1<=q<=x+1):
            pass
        if(x-1>q or x+1<q):
            a[i][2] = 0
        elif (y-1<=w<=y+1):
            pass
        elif (y - 1> w or y + 1 < w):
            a[i][2] = 0


    return a

if __name__ == "__main__":
    pass
