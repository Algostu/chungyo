import pymysql

# MySQL Connection 연결
conn = pymysql.connect(host='127.0.0.1', user='dani', password='dani030', db='pose', charset='utf8')

# Connection 으로부터 Cursor 생성
curs = conn.cursor()

# SQL문 실행


#fetchone은 호출당 한 row 가져옴.
sql = """insert into User_list(name,type,weight,Stature,description,SEX)
         values (%s, %s, %s, %s, %s, %s)"""
curs.execute(sql, ('jung', 'standard', 39, 153, 'dreamcometrue', 'women'))
curs.execute(sql, ('junDg', 'standard', 39, 153, 'dreamcometrue', 'women'))
curs.execute(sql, ('juDDng', 'standard', 39, 153, 'dreamcometrue', 'women'))
conn.commit()



sql = "select * from User_list"
curs.execute(sql)

rows = curs.fetchall()
print(rows)  # 전체 rows

print("\nmmmmm\n")
sql = "select id from User_list WHERE name = 'jung'"
curs.execute(sql)

rows = curs.fetchall()
print(rows)


#################
print("\nmmmmm\n")
sql = "select * from User_list WHERE name = 'jung'"
curs.execute(sql)

rows = curs.fetchall()
print(rows)
# Connection 닫기
conn.close()