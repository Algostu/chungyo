from pose_diff.core.fastgraphdiff import Momentum
from pose_diff.util.Common import Parts

class compare:
    def import_parts(selfs,i,Parts):
        matrix = [[0 for col in range(10)] for row in range(10)]

        for j in range(0,18):
            if(Parts[i][j]>0):
                result = test_class.get_momentum(1, j, 9)
                tmp.append

    def sub(self,result):
        #print("result")
        #pp(result)
        tmp = []
        i=0
        resultlen = len(result)
        for i in range (0,resultlen-1):
            tmp.append(result[i+1]-result[i])
        return tmp
        #pp(tmp)
        #print("hi")

    def front_cut(self,i,feedback):

        i = i*2
        #print(feedback)
        tmp=[]
        k = len(feedback)-i
        for i in range(i,k):
            tmp.append(feedback[i])
        return tmp
    def back_cut(self,lenstandard,feedback):
        j = len(feedback)
        for i in range (lenstandard,j):
            feedback.remove(feedback[i])

        return feedback



if __name__ == "__main__":
    test_class = Momentum()
    test = compare()
    print(Parts[0])
    result = test.import_parts(1,Parts,9)

    result = test_class.get_momentum(1, 2, 9)
    #print(result)
    user_result2 = test.sub(result)

    #print(user_result2)

    result2 = test_class.get_momentum(2, 2, 9)
    standard_result2 = test.sub(result2)
    #print(result2)
    #print(standard_result2)
    i = 0
    j= len(user_result2)

    #print(result2)

    for i in range (0,j):
        if(standard_result2[0]<=user_result2[i]):
            result = test.front_cut(i, result)
            #print(result)
            break

    if (len(standard_result2) > len(user_result2)):
        result = test.back_cut(len(standard_result2),result)
    #print(result)


