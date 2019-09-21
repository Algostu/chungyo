import numpy as np
from pprint import pprint as pp
import pandas as pd
import matplotlib.pyplot as plt
class Momentum:


    def get_momentum(self,video_number,part,graph_num):
        # print("확인하고 싶은 영상,시작점,끝점=확인하고싶은지점",부위(그래프 출력시 사용),출력하고 싶은 물리량,그래프 출력여부(1:2d(x,t) 2:2d(y,t) 3:3d(x,y,t))
        # video_number, start, end = input().split()
        if video_number == 1:
            frames = np.load("skeleton1.npy")  # 풀업
        elif video_number == 2:
            frames = np.load("skeleton2.npy")  # 풀업
        #18개의 부위의 각각의 값(x,y)들을 리스트(2*18)에 각각 넣은 후 위치,평균속도,순간속도,운동량 순으로 넣음

        x_list = []
        y_list = []
        vx_list=[0]
        vy_list=[0]
        ax_list=[]
        ay_list=[]
        delta_xy_list=[0]
        z_list = [i for i in range(len(frames) - 1)] #frame

        for i in range(len(z_list)):
            x_list.append(frames[i][part][1])
            y_list.append(frames[i][part][2])
            if i==0 and i==1:
                pass
            else:
                ax_list.append(frames[i - 2][part][1] + frames[i][part][1] - (frames[i-1][part][1]) - (frames[i-1][part][1]))
                ay_list.append(frames[i - 2][part][2] + frames[i][part][2] - (frames[i-1][part][2]) - (frames[i-1][part][1]))
            if i==0:
                pass
            else:
                vx_list.append(frames[i][part][1]-frames[i-1][part][1])
                vy_list.append(frames[i][part][2]-frames[i-1][part][2])
                delta_xy_list.append(pow(pow(vx_list[i], 2) + pow(vy_list[i], 2), 0.5))

        xy_list = []

        for i in range(len(x_list)):
            xy_list.append([x_list[i],y_list[i]])

        if graph_num==1:
            input=x_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif graph_num==2:
            input = y_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif graph_num == 3:
            input = vx_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif graph_num == 4:
            input = vy_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif graph_num == 5:
            input = ax_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif graph_num == 6:
            input = ay_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif graph_num == 7:
            input = delta_xy_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()

        else:
            pass

        return




if __name__ == "__main__":
    test_class = Momentum()
    result=test_class.get_momentum(1,2,7)
    pp(result)