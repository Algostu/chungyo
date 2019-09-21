from m_da.fastdiff import Momentum
from pprint import pprint as pp


class compare:
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
    result = test_class.get_momentum(1, 2, 9)
    print(result)
    test = compare()
    user_result2 = test.sub(result)

    #print(user_result2)

    result2 = test_class.get_momentum(2, 2, 9)
    standard_result2 = test.sub(result2)
    print(result2)
    #print(standard_result2)
    i = 0
    j= len(user_result2)

    #print(result2)

    for i in range (0,j):
        if(standard_result2[0]<=user_result2[i]):
            result = test.front_cut(i, result)
            print(result)
            break

    if (len(standard_result2) > len(user_result2)):
        result = test.back_cut(len(standard_result2),result)
    print(result)


