import numpy as np
from pprint import pprint as pp
class Momentum:
    def compare_avg(self,part,xy,frames):
        Joints = list(zip(*frames))
        #print(Joints[part][1][1])
        avg =0
        avg_list = []

        leni = len(Joints[part])
        print(leni)
        leni=int(leni)
        print(leni)
        flag = 1
        j = 0
        # print(Joints[part])
        while(j < leni-3):

            for i in range(0, 3 + j):
                # print(Joints[part][i][1])

                avg += Joints[part][i][xy]  # x:0 y:1
                Joints[part][i][xy] = 0.0
                avg = avg / 3
            avg_list.append(avg)

            j+=3
        # pp(Joints[part])

        print(avg_list)
        return avg_list







#
# Nose = 0
# Neck = 1
# RShoulder = 2
# RElbow = 3
# RWrist = 4
# LShoulder = 5
# LElbow = 6
# LWrist = 7
# RHip = 8
# RKnee = 9
# RAnkle = 10
# LHip = 11
# LKnee = 12
# LAnkle = 13
# REye = 14
# LEye = 15
# REar = 16
# LEar = 17
# Background = 18
#

if __name__ == "__main__":
    test_class = Momentum()

    # result = test_class.compare_avg(2,1)

    #result2 = test_class.get_momentum(2, 9) #kneesfor x
