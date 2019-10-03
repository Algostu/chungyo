from pose_diff.core.momentum import Momentum
from pose_diff.util.Common import Parts
moment = Momentum()

class compare():
    def usertypelen(self,usertype):

        tmp = moment.get_momentum(usertype,2,9)

        return len(tmp)



    def import_parts(self,exersisenum,usertype,Parts):
        leni = self.usertypelen(usertype)

        matrix = [[0 for col in range(leni)] for row in range(18)]
        print(Parts)
        for i in range (0,18):
            if (Parts[exersisenum][i]>0):
                matrix[i]=moment.get_momentum(usertype,i,9)

        return matrix




    def front_cut(self,user,standard):
        count = 0
        flag = 0
        user_len = self.usertypelen(1)
        standard_len= self.usertypelen(1)
        tmp = [[0 for col in range(user_len)] for row in range(18)]
        for j in range(1, 100):

            count = 0
            for i in range(0, 18):
                if (user[i][j] == 0 and standard[i][j] == 0):
                    break
                if(user[i][j]>=standard[i][j] or user[i][j]+0.4>=standard[i][j]):
                    count += 1
                    #print(user[i][j],"vs",standard[i][j])

            if (count > 10):

                k = len(user) - i
                for i in range(j, k):
                    tmp.append(user[i])
                    break
                return tmp




if __name__ == "__main__":

    newcompare = compare()
    matrix1 = newcompare.import_parts(0,1,Parts)
    matrix2 = newcompare.import_parts(0,2, Parts)

    print(matrix1)
    print(matrix2)

    cut_matrix = newcompare.front_cut(matrix1,matrix2)
    print(cut_matrix)