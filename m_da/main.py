import numpy as np

#list1 = np.array([[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5]])


standard = np.array([[1,1],[2,2],[1,1],[4,4],[6,6]])
human = np.array([[1,1],[2,5],[6,1],[9,4],[10,6]])

def create():
    a = np.zeros((5,3))
    for i in range(0,5):
        for j in range(0,2):
            a[i][j]=human[i][j]
            a[i][j + 1] = 255
    return a

def diff():
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
    print(diff())