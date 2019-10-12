from pose_diff.core.momentum import Momentum
moment = Momentum()

class cut:
    def compare_front(self,avglist):
        for i in range(0,len(avglist)-1):
            if(avglist[i]<avglist[i+1]):
                break

        front = (i+1)*3
        return avglist[i+1],front

    def two_front(self,i,avglist,back):
        return avglist[i+2],back+1

    def compare_back(self,avglist,frontavg,front):
        front = int(front/3) #다시 원래대로 만들어주기

        for i in range(front+10,len(avglist)-1):
            if (avglist[i] == avglist[-1]):
                break
            else:
                if (avglist[i] > avglist[i + 1] and avglist[i+1]<avglist[i+2] and avglist[i + 1]<=frontavg+3):
                    break
        back = (i+1)*3
        return i,avglist[i+1],back

    def getCut(self, frame,exercise_type=2,axis=1):
        cutarray  = []
        avglist = moment.compare_avg(exercise_type, axis, frame)
        frontavg, front = self.compare_front(avglist)
        while (True):
            try:
                i, backavg, back = self.compare_back(avglist, frontavg, front)
                tmp = (front, back)
                frontavg, front = self.two_front(i, avglist, back)

            except:
                back = len(frame)
                tmp = (front,back)
                break
            cutarray.append(tmp)

        return cutarray
