def regist_info(self):
    if self.user_info.user_type == 'u':
        name = os.path.join('data', 'user', self.user_info.user_id)
    else:
        name = os.path.join('data', 'trainer', self.user_info.user_id)
    res = self.db.create_user(name)
    if res==True:
        print('Done')
    else:
        print('Fail')
        raise MyException('create_user() fail, because this user already exist!')

def regist_skeleton(self, input_type):
    # User와 Trainer따로 구분하는 부분
    input = ""
    output = ""
    if self.user_info.user_type == 'u':
        # 파일이름은 정해진대로 사용한다.
        type = 'user'
        path = os.path.join(self.user_base_folder, self.user_info.user_id)
    else:
        type = 'trainer'
        path = os.path.join(self.trainer_base_folder, self.user_info.user_id)

    # User가 존재하는지 확인하는 부분
    res = self.check_exists(self.user_info.user_type, self.user_info.user_id)
    if res == True:
        print("Done")
    else:
        print("Fail")
        raise MyException("This user does not exist!")

    # input과 output을 정하는 부분
    for file in os.listdir(path):
        if os.path.splitext(file)[0] == self.initial:
            input = os.path.join(path, os.path.basename(file))

    output = os.path.join(path, self.skeleton)
    output_folder = output+'.npy'
    base = os.path.join(path, 'base')
    if os.path.isdir(base) == False:
        os.mkdir(base)

    if input == "" and input_type == None:
        raise MyException("initial_video file does not exist")

    # self.pose_estimation.check_procedure_list([0,0,0,0,0])
    if input_type != None:
        res = self.pose_estimation.parse_picture(self.user_info.user_id, path, os.path.join(base, 'initial_skeleton'))
        if res == True:
            print("Done")
            print("Successfully stored initial_skeleton.npy into /data/%s/%s/base folder" % (type, self.user_info.user_id))
            return True
        else:
            raise MyException('parse_picture failed for some reason')

    if os.path.isfile(output_folder) == False:
        res = self.pose_estimation.parse_video(self.user_info.user_id, input, output)
        if res == True:
            print("Done")

    res = self.pose_estimation.find_initial_skeleton(output_folder, base)
    if res == True:
        print('Done')
        print("Successfully stored skeleton.json into /data/%s/%s/ folder" % (type, self.user_info.user_id))
    else:
        print("Fail")
        raise MyException('estimate_video failed for some reason')

def train_user_skeleton(self):
    # 동영상이 저장되어있는 Path와 운동별로 저장할 폴더를 설정
    ex_type = self.user_info.preferred_exercise_type
    exercise = self.ex[ex_type]
    tr_type = self.user_info.preferred_trainer
    traier = self.trainer_list[tr_type]

    path_user = os.path.join(self.user_base_folder, self.user_info.user_id)
    path_trainer = os.path.join(self.trainer_base_folder, traier)

    # user
    print('Check target folder exist...', end=' ')
    res = os.path.isdir(path_user)
    if res == True:
        print("Done")
    else:
        print("Fail")
        raise MyException("This user does not exist!")

    # input
    print('Check if user skeletons are analized...', end=' ')
    skeleton = os.path.join(path_user, 'base')
    res = os.path.isdir(skeleton)
    if res == True:
        input_skeleton = os.path.join(skeleton, 'initial_skeleton.npy')
        print("Done")
    else:
        print("Fail")
        raise MyException("This trainer have not registered yet")

    print('Check sample vector exist...', end=' ')
    input_vector = os.path.join(path_trainer, exercise, 'vector.npy')
    res = os.path.isfile(input_vector)
    if res == True:
        print("Done")
    else:
        print("Fail")
        raise MyException("This trainer has not upload target exercise")

    # output
    output = os.path.join(path_user, exercise)
    if os.path.isdir(output) == False:
        os.mkdir(output)
    output_coordinates = os.path.join(output, self.trained_skeleton)

    res = self.pose_estimation.train_exercise(ex_type, input_skeleton, input_vector, output_coordinates)
    if res == True:
        print('Done')
        print("Successfully stored trainded_skeleton.npy into /data/%s/%s/%s folder" % (self.user_info.user_type, self.user_info.user_id, exercise))
    else:
        print("Fail")
        raise MyException('analyze_exercise failed for some reason')

def analysis_trainer_skeleton(self):
    # 동영상이 저장되어있는 Path와 운동별로 저장할 폴더를 설정
    ex_type = self.user_info.preferred_exercise_type
    exercise = self.ex[ex_type]
    path = os.path.join(self.trainer_base_folder, self.user_info.user_id)
    base = os.path.join(path, exercise)
    # print("Debug Base Folder loc : ", base)

    # user
    print('Check target folder exist...', end=' ')
    res = os.path.isdir(path)
    if res == True:
        print("Done")
    else:
        print("Fail")
        raise MyException("This user does not exist!")

    # input
    print('Check if trainer skeletons are analized...', end=' ')
    skeleton = os.path.join(path, 'base')
    res = os.path.isdir(skeleton)
    if res == True:
        input_skeleton = os.path.join(skeleton, 'initial_skeleton.npy')
        print("Done")
    else:
        print("Fail")
        raise MyException("This trainer have not registered yet")
    input_video= ""
    for file in os.listdir(path):
        if os.path.splitext(file)[0] == exercise:
            input_video = os.path.join(path, os.path.basename(file))
    if input_video == "":
        raise MyException("%s video file does not exist" % exercise)

    # output
    if os.path.isdir(base) == False:
        os.mkdir(base)
    output_skeleton = os.path.join(base, self.skeleton)
    output_vector = os.path.join(base, self.vector)

    print('Target exercise are analized before..?', end = ' ')
    if os.path.isfile(output_skeleton+'.npy') == False:
        print("Nope")
        res = self.pose_estimation.parse_video(self.user_info.user_id, input_video, output_skeleton)
        if res == True:
            print("Done")
            print("Successfully stored skeleton.npy into /data/%s/%s/%s folder" % (self.user_info.user_type, self.user_info.user_id, exercise))
        else:
            print("Fail")
            raise MyException('parse_video failed for some reason')
    else:
        print('Yes!')

    res = self.pose_estimation.analyze_exercise(ex_type, input_skeleton, output_skeleton+'.npy', output_vector)
    if res == True:
        print('Done')
        print("Successfully stored vector.npy into /data/%s/%s/%s folder" % (self.user_info.user_type, self.user_info.user_id, exercise))
    else:
        print("Fail")
        raise MyException('analyze_exercise failed for some reason')
