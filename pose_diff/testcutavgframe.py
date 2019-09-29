from pose_diff.core.fastgraphdiff import Momentum
import numpy as np
moment = Momentum()

class cut:
    def compare_front(self,avglist):

        for i in range(0,len(avglist)-1):
            if(avglist[i]<avglist[i+1]):
                break

        #print(avglist[i + 1])
        front = (i+1)*3
        print(front)
        print(avglist[i+2])
        return avglist[i+1],front

    def two_front(self,i,avglist,back):

        print(back+1)
        print(avglist[i+2])
        return avglist[i+2],back+1

    def gap_cut(self,gap,frame):
        print(gap)

    def compare_back(self,avglist,frontavg,front,frame):
        tmp = []
        back = 0
        front = int(front/3) #다시 원래대로 만들어주기

        for i in range(front,len(avglist)-1):
            if (avglist[i] > avglist[i + 1]+2 and avglist[i+1]<avglist[i+2] and avglist[i + 1]<=frontavg):
                print(avglist[i], avglist[i + 1] + 2)
                break
        #print(avglist[i+1])
        back = (i+1)*3
        gap = back - front
        until = int(len(frame)/gap)
        print(until)
        print(back)

        print(avglist[i+1])
        tmp.append(front)
        tmp.append(back)

        for z in range(1, until):
            tmp.append(back+(gap*z))

        print(tmp)
        print(avglist[36])
        print(avglist[69])
        print(avglist[108])

        return i,avglist[i+1],back

class getCut:
    def __init__(self,frame,exercise_type,axis):
        self.frame = frame
        exercise_type = 2
        axis = 1
        newcompare = cut()
        avglist = moment.compare_avg(exercise_type,axis,frame)
        frontavg, self.front = newcompare.compare_front(avglist)
        i,backavg, self.back = newcompare.compare_back(avglist, frontavg,self.front,frame)
        gap = self.back- self.front
        print(gap)



    def get_frame_number(self):
        return self.front, self.back

if __name__ == "__main__":
    frames = np.load("/Users/dani/Desktop/Projectfile/pose-difference/data/output/1-2/numpy/result.npy")
    run = getCut(frames,2,1)