import numpy as np
from pprint import pprint as pp
import pandas as pd
import matplotlib.pyplot as plt
#remove
class Momentum:
    def get_momentum(self,video_number,part,pyhsics_num):
        if video_number == 1:
            frames = np.load("/Users/dani/Desktop/Projectfile/pose-difference/data/output/1-3-3/numpy/result.npy")  # 풀업
        elif video_number == 2:
            frames = np.load("/Users/dani/Desktop/Projectfile/pose-difference/data/output/1-3-3/numpy/result.npy")  # 풀업

        exercise_list=[]

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
                delta_xy_list.append(pow(pow(vx_list[i],2)+pow(vy_list[i],2),0.5))

        xy_list = []
        vxy_list= []
        for i in range(len(x_list)):
            xy_list.append([x_list[i],y_list[i]])
            vxy_list.append([vx_list[i],vy_list[i]])

        if pyhsics_num == 1:
            exercise_list = x_list
        elif pyhsics_num == 2:
            exercise_list = y_list
        elif pyhsics_num == 3:
            exercise_list = vx_list
        elif pyhsics_num == 4:
            exercise_list = vy_list
        elif pyhsics_num == 5:
            exercise_list = ax_list
        elif pyhsics_num == 6:
            exercise_list = ay_list
        elif pyhsics_num==7:
            exercise_list=xy_list
        elif pyhsics_num==8:
            exercise_list=vxy_list
        elif pyhsics_num == 9:
            exercise_list = delta_xy_list

        if pyhsics_num == 1:
            input = x_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif pyhsics_num == 2:
            input = y_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            #plt.show()
        elif pyhsics_num == 3:
            input = vx_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif pyhsics_num == 4:
            input = vy_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif pyhsics_num == 5:
            input = ax_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif pyhsics_num == 6:
            input = ay_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()
        elif pyhsics_num == 9:
            input = delta_xy_list
            s1 = pd.Series([y for y in input], index=z_list)
            a = s1.plot(kind='bar')
            plt.show()

        else:
            pass

        return exercise_list


if __name__ == "__main__":
    test_class = Momentum()
    result=test_class.get_momentum(1,9,2)
    pp(result)