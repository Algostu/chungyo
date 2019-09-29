from pose_diff.core.fastgraphdiff import Momentum
moment = Momentum()

class cut:
    def compare_front(self,avglist):

        front = 0

        for i in range(0,len(avglist)-1):
            if(avglist[i]+1<avglist[i+1]):
                break

        #print(avglist[i + 1])
        front = (i+1)*3
        print(front)
        return avglist[i+1],front

    def compare_back(self,avglist,frontavg):

        back = 0

        for i in range(0,len(avglist)-1):
            if (avglist[i] > avglist[i + 1]+2 and avglist[i + 1]+2<frontavg):
                break
        #print(avglist[i+1])
        back = (i+1)*3
        print(back)
        return back

class getCut:
    def __init__(self,frame,exercise_type,axis):
        self.frame = frame
        exercise_type = 2
        axis = 1
        newcompare = cut()
        avglist = moment.compare_avg(exercise_type,axis,frame)
        frontavg, self.front = newcompare.compare_front(avglist)
        self.back = newcompare.compare_back(avglist, frontavg)

    def get_frame_number(self):
        return self.front, self.back