from pose_diff.core.fastgraphdiff import Momentum
from pose_diff.util.Common import Parts
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




if __name__ == "__main__":
    newcompare = cut()
    avglist = moment.compare_avg(2, 1)
    frontavg, front = newcompare.compare_front(avglist)
    back = newcompare.compare_back(avglist, frontavg)

