import pymysql

class saveuser:
    def userinformation(self):

        userinformation = []
        userinformation.append(str(input("user name: ")))
        userinformation.append(str(input("user type(standard,common): ")))
        userinformation.append(int(input("user weight: ")))
        userinformation.append(int(input("user stature: ")))
        userinformation.append(str(input("user description: ")))
        userinformation.append(str(input("user SEX(man or women): ")))

        print(userinformation)
        sql = """insert into User_list(name,type,weight,Stature,description,SEX)
                 values (%s, %s, %s, %s, %s, %s)"""
        curs.execute(sql,(userinformation))
        conn.commit()

        sql = "select * from User_list WHERE name = %s"
        curs.execute(sql, (userinformation[0]))
        self.skeleton_list() #call

    def skeleton_list(self):
        skeleton_list = []
        skeleton_list.append(int(input("skeleton_ID: ")))
        skeleton_list.append(str(input("input_id: ")))
        skeleton_list.append(str(input("skeleton_location: ")))
        

        print(skeleton_list)

        sql = """insert into Skeleton_list(Skeleton_ID,input_id,Skeleton_location)
                         values (%s, %s, %s)"""
        curs.execute(sql, (skeleton_list))
        conn.commit()
        sql = "select * from Skeleton_list WHERE Skeleton_ID = %s"
        curs.execute(sql, (skeleton_list[0]))

        self.saveinputvideo(skeleton_list[1])#call


    def saveinputvideo(self,inputid):
        saveinput=[]
        saveinput.append(inputid)
        saveinput.append(str(input("input_video_location: ")))
        print(saveinput)

        sql = """insert into User_input_Video_list(input_id,input_video_location)
                                 values (%s, %s)"""
        curs.execute(sql, (saveinput))
        conn.commit()
        sql = "select * from Skeleton_list WHERE Skeleton_ID = %s"
        curs.execute(sql, (saveinput[0]))



if __name__=="__main__":
    S = saveuser()
    conn = pymysql.connect(host='127.0.0.1', user='dani', password='dani030', db='pose', charset='utf8')
    curs = conn.cursor()
    S.userinformation()
    conn.close()