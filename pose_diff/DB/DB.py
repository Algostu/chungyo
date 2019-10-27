import os
import sqlite3
import shutil
import time
import json
from google_drive_downloader import GoogleDriveDownloader as gdd

db = './pose_diff/DB/pose_diff.db'
base_root_project_location = 'chungyo'
base_root_data_location = 'data'
base_skeleton_location = os.path.join('data', 'skeleton_list')
base_input_video_location = os.path.join('data', 'input_video') # user가 유일하게  건들어야 하는 곳, input 또한 video로 제한 했다.
base_sample_location = os.path.join('data', 'sample') # applied 또한 같이 저장된다
base_math_info_location = os.path.join('data', 'math_info')
exercise_info = [
('shoulder-press', json.dumps([0.5 for i in range(18)])),
('pull-up', json.dumps([0.5 for i in range(18)])),
('squat', json.dumps([0.5 for i in range(18)]))
] # Bug fix: common에서 central point와 다른 정보들 수정하기
google_drive_link_id = '1o1MwXGC_q2c13fLUqqkgapjdVvLoaBZo'
test_sets = [
    'TESTTRAINER_1', # side squat 1-1,1-2,1-3
    'TESTTRAINER_2',
    'TESTUSER_1', # side squat-1
    'TESTUSER_2'
]

def change_cwd():
    path = os.path.abspath(__file__)
    dirname = os.path.dirname(path)
    while os.path.split(dirname)[1] != base_root_project_location:
        dirname = os.path.dirname(dirname)

    os.chdir(dirname)

def initialize():
    make_db()
    population()

def make_db():
    change_cwd()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT datetime(CURRENT_TIMESTAMP,'localtime')")
    c.execute("DROP TABLE IF EXISTS user_list")
    c.execute("DROP TABLE IF EXISTS input_list")
    c.execute("DROP TABLE IF EXISTS user_input_video_list")
    c.execute("DROP TABLE IF EXISTS skeleton_list")
    c.execute("DROP TABLE IF EXISTS math_info_extractions")
    c.execute("DROP TABLE IF EXISTS exercise_list")
    c.execute("DROP TABLE IF EXISTS applied_skeleton_list")
    c.execute("DROP TABLE IF EXISTS diff_list")

    c.execute("""CREATE TABLE IF NOT EXISTS user_list(
    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_type TEXT CHECK( user_type IN ('standard','common')) NOT NULL DEFAULT 'common',
    user_name CHAR(30) NOT NULL,
    password CHAR(30) NOT NULL,
    weight INTEGER,
    stature INTEGER,
    description VARCHAR(200),
    SEX TEXT CHECK(SEX IN ('men','women')) DEFAULT 'men')""")

    c.execute("""CREATE TABLE IF NOT EXISTS input_list(
    input_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    init_numpy BLOB NOT NULL,
    init_video BLOB NOT NULL,
    exercise_numpy BLOB NOT NULL,
    exercise_video BLOB NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user_list(user_id) ON DELETE CASCADE,
    FOREIGN KEY(exercise_id) REFERENCES exercise_list(exercise_id) ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS skeleton_list(
    skeleton_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    input_id INTEGER NOT NULL,
    skeleton_numpy BLOB,
    graph_numpy BLOB,
    FOREIGN KEY(input_id) REFERENCES input_list(input_id) ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS exercise_list(
    exercise_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    exercise_name VARCHAR(200) NOT NULL,
    keypoints_list VARCHAR(200) NOT NULL )""")

    c.execute("""CREATE TABLE IF NOT EXISTS math_info_extractions(
    extraction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    skeleton_id INTEGER,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    math_info_1 BLOB NOT NULL,
    math_info_2 BLOB NOT NULL,
    FOREIGN KEY(skeleton_id) REFERENCES skeleton_list(skeleton_id) ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS applied_skeleton_list(
    applied_sample_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    skeleton_id INTEGER,
    standard_id INTEGER,
    exercise_id INTEGER NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    exercise_numpy BLOB NOT NULL,
    exercise_video BLOB NOT NULL,
    FOREIGN KEY(standard_id) REFERENCES math_info_extractions(extraction_id) ON DELETE CASCADE,
    FOREIGN KEY(skeleton_id) REFERENCES skeleton_list(skeleton_id) ON DELETE CASCADE,
    FOREIGN KEY(exercise_id) REFERENCES exercise_list(exercise_id) ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS diff_list(
    diff_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    applied_sample_id INTEGER,
    input_id INTEGER,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    video BLOB NOT NULL,
    graph BLBO NOT NULL,
    FOREIGN KEY(applied_sample_id) REFERENCES applied_skeleton_list(applied_sample_id) ON DELETE CASCADE,
    FOREIGN KEY(input_id) REFERENCES input_list(input_id) ON DELETE CASCADE)""")
    for exercise in exercise_info:
        c.execute("""INSERT INTO
        exercise_list (exercise_name, keypoints_list)
        values(?, ?)""", exercise)
    conn.commit()
    conn.close()
def population():
    ###########################
    # 1. data folder 정리
    # 2. TESTUSER, TESTTRAINER 생성 및 기존 데이터를 다운 받는 형식으로 변경
    # 3. exercise table 초기화

    # List of Tables
    # user_list
    # exercise_list
    # input_numpy_list # issue: squat만 적용되어 있다.
    # skeleton_list # issue: skeleton 구하는 algorithm 저장해서 구하기
    # user_input_video_list # video는 public용으로는 공개하지 않는다.
    # math_info_extractions  # issue: math info를 extraction하는 algorithm을 적용해서 구하기
    # applied_skeleton_list # issue: 병훈이의 skeleton을 적용시켜서 구한다.

    # Todo: 데이터 population을 하기 위한 instance 생성하기
    #############################
    # chage current working directory to root directory
    change_cwd()

    # delete 'data' folder if it was made before
    if os.path.exists('data'):
        shutil.rmtree('data')

    time.sleep(1) # Bug Fix: It seems to recreate 'data' folder before it is removed.
    # Another Bug: if 'data' folder is opend, it cannot remove and recreate.

    # create 'data' folder directory
    os.mkdir('data')

    # download test sets and subdirectories
    os.mkdir(base_skeleton_location) # will be removed
    os.mkdir(base_input_video_location)
    os.mkdir(base_sample_location)
    os.mkdir(base_math_info_location)
    download_path = './data/download.zip'
    gdd.download_file_from_google_drive(file_id=google_drive_link_id,
                                        dest_path= download_path,
                                        unzip=True)
    os.remove(download_path)

    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("""INSERT INTO
    user_list (user_type, user_name, weight, stature, description, SEX)
    values('standard', 'TESTTRAINER_1', 80, 180, 'made for test and first use', 'men')""") # Issue: weight, stature 단위

    c.execute("""INSERT INTO
    user_list (user_type, user_name, weight, stature, description, SEX)
    values('standard', 'TESTTRAINER_2', 65, 165, 'made for test and first use', 'women')""")

    c.execute("""INSERT INTO
    user_list (user_type, user_name, weight, stature, description, SEX)
    values('common', 'TESTUSER_1', 80, 180, 'made for test and first use', 'men')""")

    c.execute("""INSERT INTO
    user_list (user_type, user_name, weight, stature, description, SEX)
    values('common', 'TESTUSER_2', 65, 165, 'made for test and first use', 'women')""")

    c.execute("""INSERT INTO
    numpy_input_list (user_id, exercise_id, sample_location)
    values (1, 1, ?)""", (os.path.join(base_sample_location, 'side_squat_1-1.npy'),))

    c.execute("""INSERT INTO
    skeleton_list (user_id, sample_id, skeleton_location)
    values (0, ?, ?)
    """, (c.lastrowid, os.path.join(base_skeleton_location, 'TESTTRAINER_1.npy'),))

    c.execute("""INSERT INTO
    numpy_input_list (user_id, exercise_id, sample_location)
    values (1, 1, ?)""", (os.path.join(base_sample_location, 'side_squat_1-2.npy'),))

    c.execute("""INSERT INTO
    skeleton_list (user_id, sample_id, skeleton_location)
    values (1, ?, ?)
    """, (c.lastrowid, os.path.join(base_skeleton_location, 'TESTTRAINER_2.npy'),))

    c.execute("""INSERT INTO
    numpy_input_list (user_id, exercise_id, sample_location)
    values (1, 1, ?)""", (os.path.join(base_sample_location, 'side_squat_1-2.npy'),))

    c.execute("""INSERT INTO
    skeleton_list (user_id, sample_id, skeleton_location)
    values (2, ?, ?)
    """, (c.lastrowid, os.path.join(base_skeleton_location, 'TESTUSER_1.npy'),))

    c.execute("""INSERT INTO
    numpy_input_list (user_id, exercise_id, sample_location)
    values (3, 1, ?)""", (os.path.join(base_sample_location, 'side_squat_1.npy'),))

    c.execute("""INSERT INTO
    skeleton_list (user_id, sample_id, skeleton_location)
    values (3, ?, ?)
    """, (c.lastrowid, os.path.join(base_skeleton_location, 'TESTUSER_2.npy'),))


    conn.commit()
    conn.close()

# Login
def checkUnique(user_name):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        input = (user_name,)
        c.execute("""SELECT user_id
        from user_list
        where user_name = ? """, input)

        rows = c.fetchone()
        conn.commit()
        conn.close()

        if rows != None:
            return False
        else:
            return True

def create_user(user_type, user_name, weight=None, stature=None, description=None, sex=None):
                ####################################
                # Basic Info
                # params
                # user_list column들 모두를 받지만 None으로 설정한 값도 있다.
                # How it works
                # user_list에 New User를 등록한다.
                # Return Values
                # 등록한 user의 user_id (PK of user_list)

                # Feature

                # Todo
                ####################################
                conn = sqlite3.connect(db)
                c = conn.cursor()

                c.execute("""INSERT INTO
                user_list (user_type, user_name, weight, stature, description, SEX)
                values(?, ?, ?, ?, ?, ?)""", (user_type, user_name, weight, stature, description, sex))
                # example) values ('standard', 'TESTTRAINER_1', 80, 180, 'made for test and first use', 'men')
                primary_key = c.lastrowid

                conn.commit()
                conn.close()

                return primary_key

# UC 1
def get_exercise_names():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute('Select exercise_name from exercise_list')
    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def read_from_input_list(input_id, base_folder):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from input_list where input_id = ?"""
        cursor.execute(sql_fetch_blob_query, (input_id,))
        record = cursor.fetchall()
        for row in record:
            init_numpy  = os.path.join(base_folder, 'init_numpy.npy')
            init_video  = os.path.join(base_folder, 'init_video.avi')
            exercise_numpy  = os.path.join(base_folder, 'exercise_numpy.npy')
            exercise_video  = os.path.join(base_folder, 'exercise_video.avi')

            print("Storing User numpy and video on disk \n")
            writeTofile(row[4], init_numpy) # N
            writeTofile(row[5], init_video)
            writeTofile(row[6], exercise_numpy)
            writeTofile(row[7], exercise_video)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def insert_input_list(user_id, exercise_id, init_numpy, init_video, exercise_numpy, exercise_video):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """INSERT INTO input_list
                                  (user_id, exercise_id, init_numpy, init_video, exercise_numpy, exercise_video) VALUES (?, ?, ?, ?, ?, ?)"""

        init_numpy = convertToBinaryData(init_numpy)
        init_video = convertToBinaryData(init_video)
        exercise_numpy = convertToBinaryData(exercise_numpy)
        exercise_video = convertToBinaryData(exercise_video)
        # Convert data into tuple format
        data_tuple = (user_id, exercise_id, init_numpy, init_video, exercise_numpy, exercise_video)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Video and Numpy files inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")
# Usage - store blob data into table
# file_naming - ./temp/column_name+적절한 확장자
# Store file in temp
# insert_input_list(1, 0, "./temp/init_numpy.py", "./temp/init_video.avi", "./temp/exercise_numpy.py", "./temp/exercise_video.avi")
# delete temp folder

# Usage - read blob data from table
# make temp folder
# readBlobData(1, 1, 'temp')

# UC 2,3
def get_input_list(user_id):
    """
    Get Rows in input_list
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("""SELECT
    input_list.input_id,
    exercise_list.exercise_name,
    input_list.create_time
    FROM
    input_list
    LEFT JOIN exercise_list ON input_list.exercise_id = exercise_list.exercise_id
    WHERE
    input_list.user_id = ?""", (user_id,))

    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows # UC 2,3 공통 (Scene 1)

def get_user_info(user_id):
    """
    Basic Info
    params
        user_id:에 해당하는 user의 정보를 불러온다.
    How it works
        user_id 해당되는user의 정보를 return 한다.
    Return Values
        [(user_name, user_type)]
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("Select user_type, user_name from user_list where user_id = ?", (user_id,))

    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows # UC 2,3 공통 (Scene 1)

def get_user_list(user_type):
    """
    Basic Info
    params
        user_type: 'common'과 'standard' 둘 중 하나의 값을 받는다.
    How it works
        user_type에 해당되는 user들의 rows만 return 한다.
    Return Values
        [(user_id, user_list)]
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("Select user_id, user_name from user_list where user_type = ?", (user_type,))

    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows # UC 3 (Scene 1)

def get_math_info_list(user_id):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = """SELECT
    math_info_extractions.extraction_id,
    exercise_list.exercise_name,
    math_info_extractions.create_time
    FROM
    math_info_extractions
    LEFT JOIN skeleton_list ON math_info_extractions.skeleton_id = skeleton_list.skeleton_id
    LEFT JOIN input_list ON input_list.input_id = skeleton_list.input_id
    LEFT JOIN exercise_list ON input_list.exercise_id = exercise_list.exercise_id
    WHERE
    input_list.user_id = ?"""
    c.execute(sql, (user_id,))

    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows # UC 2,3 공통 (Scene 1)

# * 개발 대상 : 개발 완료
def save_skeleton(input_id, skeleton_numpy, graph_numpy):
    """
    skeleton을 저장한다.

    params
        user_id : user_list의 PK, numpy_input_list의 FK이다.
        skeleton_numpy : [init_skeleton, frame_num]형식으로 저장된 파일 이름이다.
        graph_numpy : graph_numpy가 하나로 저장된 파일 이름이다.
    How it works
        skeleton_numpy와 graph_nump를 Blob 형식으로 저장한다.
    Return Values
        skeleton_id
    """
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """Insert into
        skeleton_list (input_id, skeleton_numpy, graph_numpy)
        values (?, ?, ?)"""
        skeleton_numpy = convertToBinaryData(skeleton_numpy)
        graph_numpy = convertToBinaryData(graph_numpy)
        # Convert data into tuple format
        data_tuple = (input_id, skeleton_numpy, graph_numpy)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        primary_key = cursor.lastrowid
        sqliteConnection.commit()
        print("Numpy files inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed") # UC 2,3 공통 (Scene 2)
            return primary_key # UC 2,3 공통 (Scene 2)

# * 개발 대상 : 개발 완료
def load_skeleton(skeleton_id, base_folder):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from skeleton_list where skeleton_id = ?"""
        cursor.execute(sql_fetch_blob_query, (skeleton_id,))
        record = cursor.fetchall()
        for row in record:
            skeleton_numpy  = os.path.join(base_folder, 'skeleton.npy')
            graph_numpy  = os.path.join(base_folder, 'graph.npy')

            print("Storing skeleton and graph numpy on disk \n")
            writeTofile(row[2], skeleton_numpy)
            writeTofile(row[3], graph_numpy)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed") # UC 2,3 공통 (Scene 3)

# * 개발 대상 : 개발 완료
def save_math_info_extraction(skeleton_id, math_info_1, math_info_2):
    """
    math_info를 저장한다.

    params
        skeleton_id : 저장할 skeleton_id
        math_info_1 : 파일 이름 1
        math_info_1 : 파일 이름 2
    How it works
        math_info_1, math_info_2를 blob형식으로 저장한다.
        저장된 파일 삭제 x
    Return Values
        extraction_id
    """
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """Insert into
        math_info_extractions (skeleton_id, math_info_1, math_info_2)
        values (?, ?, ?)"""
        math_info_1 = convertToBinaryData(math_info_1)
        math_info_2 = convertToBinaryData(math_info_2)
        # Convert data into tuple format
        data_tuple = (skeleton_id, math_info_1, math_info_2)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        primary_key = cursor.lastrowid
        sqliteConnection.commit()
        print("Math Info numpy and video inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed") # UC 2,3 공통 (Scene 2)
            return primary_key # UC 2 (Scene 3)

# * 개발 대상 : 개발 완료
def load_math_info_extraction(extraction_id, base_folder):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from math_info_extractions where extraction_id = ?"""
        cursor.execute(sql_fetch_blob_query, (extraction_id,))
        record = cursor.fetchall()
        for row in record:
            math_info_npy  = os.path.join(base_folder, 'math_info.npy')
            math_info_avi  = os.path.join(base_folder, 'math_info.avi')

            print("Storing math info numpy and video on disk \n")
            writeTofile(row[3], math_info_npy)
            writeTofile(row[4], math_info_avi)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

# * 개발 대상 : 개발 완료
def save_applied_sample(skeleton_id, standard_id, exercise_id, exercise_numpy, exercise_video):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """Insert into
        applied_skeleton_list (skeleton_id, standard_id, exercise_id, exercise_numpy, exercise_video)
        values (?, ?, ?, ?, ?)"""
        exercise_numpy = convertToBinaryData(exercise_numpy)
        exercise_video = convertToBinaryData(exercise_video)
        # Convert data into tuple format
        data_tuple = (skeleton_id, standard_id, exercise_id, exercise_numpy, exercise_video)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        primary_key = cursor.lastrowid
        sqliteConnection.commit()
        print("Applied numpy and video inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")
            return primary_key  # UC 3 (Scene 3)

# * 개발 대상 : 개발 완료
def get_exercise_id(input_id):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """Select exercise_id from
        input_list where
        input_list.input_id = ?"""
        data_tuple = (input_id,)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        rows = cursor.fetchall()
        sqliteConnection.commit()
        print("Load exercise id from a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")
            return rows # UC 3 (Scene 3) # UC 3 (Scene 3)

# UC 4, 5
def load_applied_skeleton_list(user_id):
    """
    Return Value
        (applied_sample_id, trainer_name, exercise_name)
    """

    tables = []
    conn = sqlite3.connect(db)
    c = conn.cursor()
    sql = """SELECT
    applied_sample_id,
    user_list.user_name,
    exercise_list.exercise_name
    FROM
    applied_skeleton_list
    LEFT JOIN exercise_list ON exercise_list.exercise_id = applied_skeleton_list.exercise_id
    LEFT JOIN skeleton_list ON applied_skeleton_list.skeleton_id = skeleton_list.skeleton_id
    LEFT JOIN input_list ON skeleton_list.input_id = input_list.input_id
    LEFT JOIN user_list ON input_list.user_id = user_list.user_id
    where
    user_list.user_id = ?"""

    params = (user_id,)
    c.execute(sql, params)
    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows

def load_applied_skeleton_file(applied_sample_id, base_folder):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from applied_skeleton_list where applied_sample_id = ?"""
        cursor.execute(sql_fetch_blob_query, (applied_sample_id,))
        record = cursor.fetchall()
        for row in record:
            upgraded_numpy  = os.path.join(base_folder, 'upgraded.npy')
            upgraded_video  = os.path.join(base_folder, 'upgraded.avi')

            print("Storing User numpy and video on disk \n")
            writeTofile(row[5], upgraded_numpy)
            writeTofile(row[6], upgraded_video)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def save_diff(applied_sample_id, input_id, video, graph):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """Insert into
        diff_list (applied_sample_id, input_id, video, graph)
        values (?, ?, ?, ?)"""
        video = convertToBinaryData(video)
        graph = convertToBinaryData(graph)
        # Convert data into tuple format
        data_tuple = (applied_sample_id, input_id, video, graph)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        primary_key = cursor.lastrowid
        sqliteConnection.commit()
        print("diffing video inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")

# * 개발 대상
def load_diff(diff_id, base_folder):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from applied_skeleton_list where diff_id = ?"""
        cursor.execute(sql_fetch_blob_query, (diff_id,))
        record = cursor.fetchall()
        for row in record:
            video  = os.path.join(base_folder, 'diff.avi')
            numpy  = os.path.join(base_folder, 'graph.npy')

            print("Storing User numpy and video on disk \n")
            writeTofile(row[4], video)
            writeTofile(row[5], numpy)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

# MoreInfo
def load_data_list(user_id):
    data_list = []
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_load_query = []
        data_tuple = (user_id,)
        sqlite_load_query = [
        """Select
        skeleton_list.skeleton_id,
        exercise_list.exercise_name
        from
        input_list
        left join exercise_list on exercise_list.exercise_id = input_list.exercise_id
        left join skeleton_list on skeleton_list.input_id = input_list.input_id
        WHERE
        input_list.user_id = ?""",

        """Select
        applied_skeleton_list.applied_sample_id,
        exercise_list.exercise_name
        from
        applied_skeleton_list
        left join exercise_list on exercise_list.exercise_id = applied_skeleton_list.exercise_id
        left join skeleton_list on skeleton_list.skeleton_id = applied_skeleton_list.skeleton_id
        left join input_list on input_list.input_id = skeleton_list.input_id
        WHERE
        input_list.user_id = ?""",

        """Select
        diff_list.diff_id,
        exercise_list.exercise_name
        from
        diff_list
        left join input_list on input_list.input_id = diff_list.input_id
        left join exercise_list on exercise_list.exercise_id = input_list.exercise_id
        WHERE
        input_list.user_id = ?""",

        """Select
        math_info_extractions.extraction_id,
        exercise_list.exercise_name
        from
        math_info_extractions
        left join skeleton_list on skeleton_list.skeleton_id = math_info_extractions.skeleton_id
        left join input_list on input_list.input_id = skeleton_list.input_id
        left join exercise_list on exercise_list.exercise_id = input_list.exercise_id
        WHERE
        input_list.user_id = ?"""
        ]

        for query in sqlite_load_query:
            cursor.execute(query, data_tuple)
            data_list.append(cursor.fetchall())
        sqliteConnection.commit()
        print("load data list successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to load data list from a table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")
            return data_list


# ETC
def get_exercise_list(exercise_id):
    """
    exercise_id로 exercise_name을 가져온다

    params
        exercise_id : exercise_list 의 PK
    How it works
        DB에 저장된 Exercise들의 이름과 PK값을 가져온다.
    Return Values
        [(exercise_id, exercise_name)]
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("Select exercise_id, exercise_name from exercise_list where exercise_id = ?", (exercise_id,))

    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows

if __name__ == '__main__':
    make_db()
