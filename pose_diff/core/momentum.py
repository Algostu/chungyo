class Momentum:
    def compare_avg(self,part,xy,frames):
        Joints = list(zip(*frames))
        avg =0
        avg_list = []

        leni = len(Joints[part])
        leni=int(leni)

        j = 0
        while(j < leni-3):
            for i in range(0, 3 + j):
                avg += Joints[part][i][xy]  # x:0 y:1
                Joints[part][i][xy] = 0.0
                avg = avg / 3
            avg_list.append(avg)
            j+=3

        return avg_list


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