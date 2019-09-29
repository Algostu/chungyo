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

    def compare_back(self,avglist,frontavg,front):
        flag = 0
        back = 0
        front = int(front/3) #다시 원래대로 만들어주기

        for i in range(front+10,len(avglist)-1):

            if (avglist[i] == avglist[-1]):
                print(avglist[i],avglist[-1])
                break
            else:

                if (avglist[i] > avglist[i + 1] and avglist[i+1]<avglist[i+2] and avglist[i + 1]<=frontavg+3):
                    print(avglist[i], avglist[i + 1] + 2)
                    break


        #print(avglist[i+1])

        back = (i+1)*3
        print(back)

        print(avglist[i+1])
        return i,avglist[i+1],back

class getCut:
    def __init__(self,frame,exercise_type,axis):
        self.frame = frame
        exercise_type = 2
        axis = 1
        newcompare = cut()
        cutarray = []
        avglist = moment.compare_avg(exercise_type,axis,frame)
        frontavg, self.front = newcompare.compare_front(avglist)
        #cutarray.append(self.front)

        while(True):
            try:
                i, backavg, self.back = newcompare.compare_back(avglist, frontavg, self.front)
                tmp = (self.front,self.back)
                frontavg, self.front = newcompare.two_front(i, avglist, self.back)


            except:
                self.back = len(frame)
                tmp = (self.front, self.back)
                print(self.back)
                break

            cutarray.append(tmp)
        print(cutarray)

    def get_frame_number(self):
        return self.front, self.back

if __name__ == "__main__":
    frames = np.load("/Users/dani/Desktop/Projectfile/pose-difference/data/output/1-2/numpy/result.npy")
    run = getCut(frames,2,1)