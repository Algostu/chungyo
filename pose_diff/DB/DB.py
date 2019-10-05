import os
import sqlite3
import shutil
import time
import json
from google_drive_downloader import GoogleDriveDownloader as gdd

def initialize():
    make_db()
    population()

def make_db():
    change_cwd()
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS user_list")
    c.execute("DROP TABLE IF EXISTS user_input_video_list")
    c.execute("DROP TABLE IF EXISTS skeleton_list")
    c.execute("DROP TABLE IF EXISTS numpy_input_list")
    c.execute("DROP TABLE IF EXISTS math_info_extractions")
    c.execute("DROP TABLE IF EXISTS exercise_list")
    c.execute("DROP TABLE IF EXISTS applied_skeleton_list")

    c.execute("""CREATE TABLE IF NOT EXISTS user_list(
    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_type TEXT CHECK( user_type IN ('standard','common')) NOT NULL DEFAULT 'common',
    user_name CHAR(30) NOT NULL,
    weight INTEGER,
    stature INTEGER,
    description VARCHAR(200),
    SEX TEXT CHECK(SEX IN ('men','women')) DEFAULT 'men')""")

    c.execute("""CREATE TABLE IF NOT EXISTS skeleton_list(
    skeleton_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skeleton_location VARCHAR(200),
    FOREIGN KEY(user_id) REFERENCES user_list(user_id) ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS user_input_video_list(
    input_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    input_video_location VARCHAR(200),
    FOREIGN KEY(user_id) REFERENCES user_list(user_id) ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS numpy_input_list(
    sample_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    exercise_id INTEGER,
    sample_location VARCHAR(200),
    FOREIGN KEY(user_id) REFERENCES user_list(user_id) ON DELETE CASCADE,
    FOREIGN KEY(exercise_id) REFERENCES exercise_list(exercise_id) ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS exercise_list(
    exercise_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    exercise_name VARCHAR(200) NOT NULL,
    keypoints_list VARCHAR(200) NOT NULL )""")

    c.execute("""CREATE TABLE IF NOT EXISTS math_info_extractions(
    extraction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    skeleton_id INTEGER,
    exercise_id INTEGER,
    sample_id INTEGER,
    vector_training VARCHAR(200) NOT NULL,
    degreediffloc VARCHAR(200) NOT NULL,
    FOREIGN KEY(skeleton_id) REFERENCES skeleton_list(skeleton_id) ON DELETE CASCADE,
    FOREIGN KEY(exercise_id) REFERENCES exercise_list(exercise_id) ON DELETE CASCADE,
    FOREIGN KEY(sample_id) REFERENCES numpy_input_list(sample_id) ON DELETE CASCADE)""")

    c.execute("""CREATE TABLE IF NOT EXISTS applied_skeleton_list(
    applied_sample_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    skeleton_id INTEGER,
    standard_id INTEGER,
    exercise_id INTEGER NOT NULL,
    result_loc VARCHAR(200) NOT NULL,
    FOREIGN KEY(standard_id) REFERENCES math_info_extractions(extraction_id) ON DELETE CASCADE,
    FOREIGN KEY(skeleton_id) REFERENCES skeleton_list(skeleton_id) ON DELETE CASCADE,
    FOREIGN KEY(exercise_id) REFERENCES exercise_list(exercise_id) ON DELETE CASCADE)""")

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

    for exercise in exercise_info:
        c.execute("""INSERT INTO
        exercise_list (exercise_name, keypoints_list)
        values(?, ?)""", exercise)

    c.execute("""INSERT INTO
    skeleton_list (user_id, skeleton_location)
    values (0, ?)
    """, (os.path.join(base_skeleton_location, 'TESTTRAINER_1.npy'),))

    c.execute("""INSERT INTO
    skeleton_list (user_id, skeleton_location)
    values (1, ?)
    """, (os.path.join(base_skeleton_location, 'TESTTRAINER_2.npy'),))

    c.execute("""INSERT INTO
    skeleton_list (user_id, skeleton_location)
    values (2, ?)
    """, (os.path.join(base_skeleton_location, 'TESTUSER_1.npy'),))

    c.execute("""INSERT INTO
    skeleton_list (user_id, skeleton_location)
    values (3, ?)
    """, (os.path.join(base_skeleton_location, 'TESTUSER_2.npy'),))

    c.execute("""INSERT INTO
    numpy_input_list (user_id, exercise_id, sample_location)
    values (1, 1, ?)""", (os.path.join(base_sample_location, 'side_squat_1-1.npy'),))

    c.execute("""INSERT INTO
    numpy_input_list (user_id, exercise_id, sample_location)
    values (1, 1, ?)""", (os.path.join(base_sample_location, 'side_squat_1-2.npy'),))

    c.execute("""INSERT INTO
    numpy_input_list (user_id, exercise_id, sample_location)
    values (1, 1, ?)""", (os.path.join(base_sample_location, 'side_squat_1-2.npy'),))

    c.execute("""INSERT INTO
    numpy_input_list (user_id, exercise_id, sample_location)
    values (3, 1, ?)""", (os.path.join(base_sample_location, 'side_squat_1.npy'),))

    conn.commit()
    conn.close()

db = './pose_diff/DB/pose_diff.db'
base_root_project_location = 'pose-difference'
base_root_data_location = 'data'
base_skeleton_location = os.path.join('data', 'skeleton_list')
base_input_video_location = os.path.join('data', 'input_video') # user가 유일하게  건들어야 하는 곳, input 또한 video로 제한 했다.
base_sample_location = os.path.join('data', 'sample')
base_math_info_location = os.path.join('data', 'math_info')
exercise_info = [
('squat', json.dumps([0.5 for i in range(18)])),
('pull-up', json.dumps([0.5 for i in range(18)])),
('shoulder-press', json.dumps([0.5 for i in range(18)]))
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

###############
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

def get_user_list(user_type):
    ####################################
    # Basic Info
    # params
    # user_type: 'common'과 'standard' 둘 중 하나의 값을 받는다.
    # How it works
    # user_type에 해당되는 user들의 rows만 return 한다.
    # Return Values
    # [(user_id, user_list)]

    # Feature

    # Todo
    ####################################
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("Select user_id, user_name from user_list where user_type = ?", (user_type,))

    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows

def get_exercise_list():
    ####################################
    # Basic Info
    # params
    #
    # How it works
    # DB에 저장된 Exercise들의 이름과 PK값을 가져온다.
    # Return Values
    # [(exercise_id, exercise_name)]

    # Feature

    # Todo
    ####################################
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("Select exercise_id, exercise_name from exercise_list")

    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows

def get_registered_exercise_for_one_user(user_id, exercise_id):
    ####################################
    # Basic Info
    # params
    # user_id : user_list의 PK, numpy_input_list의 FK이다.
    # exercise_id : exercise_list의 PK, numpy_input_list의 FK이다.
    # How it works
    # user_id와 exercise_id를 통해서 등록된 sample의 fk와 location을 가져온다.
    # Return Values
    # [(sample_id, sample_location)]

    # Feature

    # Todo
    ####################################
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("Select sample_id, sample_location from numpy_input_list where user_id=? and exercise_id=?", (user_id, exercise_id))

    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows

def save_sample(user_id, numpy, file_name, exercise_id):
    ####################################
    # Basic Info
    # params
    # user_id : user_list의 PK, numpy_input_list의 FK이다.
    # exercise_id : exercise_list의 PK, numpy_input_list의 FK이다.
    # numpy : sample에 저장될 numpy array이다.
    # file_name : 파일 이름이다.
    # How it works
    # numpy file을 지정된 장소에 저장해주고 이를 db에 저장한다.
    # Return Values
    # sample_id

    # Feature

    # Todo
    ####################################
    loc = os.path.join(base_sample_location, file_name)
    np.save(loc, numpy)

    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("""Insert into
    numpy_input_list (user_id, exercise_id, sample_location)
    values (?, ?, ?)""", (user_id, exercise_id, loc))

    primary_key = c.lastrowid

    conn.commit()
    conn.close()

    return primary_key

def save_skeleton(user_id, numpy, file_name):
    ####################################
    # Basic Info
    # params
    # user_id : user_list의 PK, numpy_input_list의 FK이다.
    # numpy : sample에 저장될 numpy array이다.
    # file_name : 파일 이름이다.
    # How it works
    # numpy file을 지정된 장소에 저장해주고 이를 db에 저장한다.
    # Return Values
    # skeleton_id

    # Feature

    # Todo
    ####################################
    loc = os.path.join(base_skeleton_location, file_name)
    np.save(loc, numpy)

    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("""Insert into
    skeleton_list (user_id, skeleton_location)
    values (?, ?)""", (user_id, loc))

    primary_key = c.lastrowid

    conn.commit()
    conn.close()

    return primary_key

def save_math_info_extraction(skeleton_id, exercise_id, sample_id, numpys, file_names):
    ####################################
    # Basic Info
    # params
    # numpys : sample에 저장될 numpy array이다.
    # file_names : 파일 이름이다.
    # How it works
    # numpy file을 지정된 장소에 저장해주고 이를 db에 저장한다.
    # Return Values
    # extraction_id

    # Feature

    # Todo
    # file_name과 numpy들을 정의해야한다.
    ####################################
    for file_name, numpy in zip(file_names, numpys):
        loc = os.path.join(base_math_info_location, file_name)
        np.save(loc, numpy)

    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute("""Insert into
    math_info_extractions (skeleton_id, exercise_id, sample_id, )
    values (?, ?, ?, )""", (skeleton_id, exercise_id, sample_id))

    primary_key = c.lastrowid

    conn.commit()
    conn.close()

    return primary_key
