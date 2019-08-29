import math
import numpy as np
from pprint import pprint as pp

class Common():
    def __init__(self):
        self.PART_NAMES = ['nose', 'neck',  'rshoulder', 'relbow', 'rwrist', 'lshoulder', 'lelbow', 'lwrist', 'rhip', 'rknee', 'rankle', 'lhip', 'lknee', 'lankle', 'reye', 'leye', 'rear', 'lear']
        # 각 부위별 인식률
        self.initial_parts = [0.6 for i in range(18)]
        # 전체 인식률 (한 프레임)
        self.accuracy = .75
        # 전체 인식률 (동영상 전체)
        self.agv_accuracy = 0.8
        # ex_parts 와 ex_pairs는 동일한 같은 점 집합으로 생성해야 한다.
        self.ex_parts = [
        [],
        [],
        [],
        [0.5, 0.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0] # walk
        ]
        self.ex_pairs = [
        [],
        [],
        [],
        CocoPairs[:-6]
        ]
        # 어떤 운동이던지 간에 중심점을 Neck으로 설정한다.
        self.ex_center = [ 1, 1, 1, 1]

    def apply_vector(self, ex_type, length, vector):
        parts = self.ex_parts[ex_type][:]
        pairs = self.ex_pairs[ex_type][:]
        length = length[0]
        frames_len = len(vector)
        frames = []
        # print(length)
        basic_length = []
        for pair in pairs:
            basic_length.append(self.distance(length[pair[0]], length[pair[1]]))
        # pp(basic_length)

        n = 0
        for i in range(frames_len-200):
            frames.append([(0, 0, 0) for i in range(18)])
            # neck (x, y, 0)신뢰도는 0으로 고정
            frames[i][1] = tuple(vector[i][0])
            # rshoulder
            if parts[2] > 0:
                # n += 1
                frames[i][2] = self.calc_coordinates(frames[i][1], tuple(vector[i][1]), basic_length[0])

            # lshoulder
            if parts[5] > 0:
                # n += 1
                frames[i][5] = self.calc_coordinates(frames[i][1], tuple(vector[i][2]), basic_length[1])

            # rhip
            if parts[8] > 0:
                # n += 1
                frames[i][8] = self.calc_coordinates(frames[i][1], tuple(vector[i][7]), basic_length[6])

            # lhip
            if parts[11] > 0:
                # n += 1
                frames[i][11] = self.calc_coordinates(frames[i][1], tuple(vector[i][10]), basic_length[9])

            # nose
            if parts[0] > 0:
                # n += 1
                frames[i][0] = self.calc_coordinates(frames[i][1], tuple(vector[i][13]), basic_length[12])

            # relbow
            if parts[3] > 0:
                # n += 1
                frames[i][3] = self.calc_coordinates(frames[i][2], tuple(vector[i][3]), basic_length[2])

            # rwrist
            if parts[4] > 0:
                # n += 1
                frames[i][4] = self.calc_coordinates(frames[i][3], tuple(vector[i][4]), basic_length[3])

            # lelbow
            if parts[6] > 0:
                # n += 1
                frames[i][6] = self.calc_coordinates(frames[i][5], tuple(vector[i][5]), basic_length[4])

            # lwrist
            if parts[7] > 0:
                # n += 1
                frames[i][7] = self.calc_coordinates(frames[i][6], tuple(vector[i][6]), basic_length[5])

            # rknee
            if parts[9] > 0:
                # n += 1
                frames[i][9] = self.calc_coordinates(frames[i][8], tuple(vector[i][8]), basic_length[7])

            # rankle
            if parts[10] > 0:
                # n += 1
                frames[i][10] = self.calc_coordinates(frames[i][9], tuple(vector[i][9]), basic_length[8])

            # lknee
            if parts[12] > 0:
                # n += 1
                frames[i][12] = self.calc_coordinates(frames[i][11], tuple(vector[i][11]), basic_length[10])

            # lankle
            if parts[13] > 0:
                # n += 1
                frames[i][13] = self.calc_coordinates(frames[i][12], tuple(vector[i][12]), basic_length[11])



        # print('rshoulder : %d' % n)
        # pp(frames)

        return frames

    def calc_coordinates(self, starting_point, norm_vector_and_size, fixed):
        point = starting_point[:2]
        # print(point)
        vector = (norm_vector_and_size[0], norm_vector_and_size[1])
        size = norm_vector_and_size[2]
        coor = tuple(np.add(point, np.multiply(vector, size*fixed))) + (0.0,)
        # print(coor)
        return coor

    # 동영상의 인식률을 판단하는 프로그램
    # 단, 운동별로 있어야 하는 부분이 다르다.
    # 각도와 길이또한 판단해야 한다.
    # 처음 서있는 자세라 해도 모든 것을 다 인식할 필요는 없다.
    def check_accuracy(self, frames, exercise_type, exit_flags):
        if exercise_type == -1:
            required_parts = self.initial_parts[:]
            avg_acc = self.accuracy
        elif exercise_type > 0:
            required_parts = self.ex_parts[exercise_type][:]
            avg_acc = self.accuracy
        else:
            raise MyException('exercise_type are between 0 and 5')

        accuracy = []
        accurate_frame = []
        accurate_frame_num = []
        field_len = len(required_parts)
        for idx, frame in enumerate(frames):
            accuracy.append(0)
            for part_idx, part_accuracy in enumerate(required_parts):
                # 양쪽을 비교하는게 정상이나... 일단 전체 비교만 한다고 가정한다.
                if frame[part_idx][2] > part_accuracy:
                    accuracy[idx] += 1
            accuracy[idx] /= field_len
            # print("accuracy %d # : %f" % (idx, accuracy[idx]))
            if accuracy[idx] >= avg_acc:
                if exit_flags == 1:
                    print("Found Target Frame")
                    print("Found Target Frame Number is #%d" % idx)
                    return accuracy[idx], [frame]
                else:
                    accurate_frame_num.append(1)
                    accurate_frame.append(frame)
            else:
                accurate_frame.append(0)
                accurate_frame_num.append(0)

        avg_accuracy = self.average(accuracy)
        print("This frames accuracy is %f" % avg_accuracy)

        return avg_accuracy, [accurate_frame, accurate_frame_num]

    def average(self, list):
        sum = 0
        for item in list:
            sum += item
        return sum/len(list)

    # angle 추가하기 + 운동별로 다르게 하기
    def calculate_trainer(self, ex_type, static_skeleton, dynamic_skeleton, dynamic_num):
        target_pairs = self.ex_pairs[ex_type][:]
        pairs_len = len(target_pairs)

        body_measurements = []
        body_movement_length = [[] for i in range(pairs_len)]
        body_movement_vector = [[] for i in range(pairs_len)]

        for idx,pairs in enumerate(target_pairs):
            body_measurements.append(self.distance(static_skeleton[pairs[0]-1], static_skeleton[pairs[1]-1]))
            fixed_len = body_measurements[idx]
            # for debug
            # m_num = 0
            # n_num = 0
            # nm_num = 0
            # vector와 length
            for index, value in enumerate(dynamic_num)  :
                if value == 1:
                    tuple = [dynamic_skeleton[index][pairs[0]], dynamic_skeleton[index][pairs[1]]]
                    if tuple[0][2] > 0 and  tuple[1][2]> 0:
                        body_movement_length[idx].append(self.distance(tuple[0], tuple[1])/fixed_len)
                        body_movement_vector[idx].append(self.norm_vector(tuple[0], tuple[1]))
                        # print(body_movement_length[idx][index])
                        # print(self.degree(body_movement_vector[idx][index]))
                        # m_num += 1
                    else:
                        body_movement_length[idx].append(0)
                        body_movement_vector[idx].append(0)
                        # n_num += 1
                else:
                    body_movement_length[idx].append(0)
                    body_movement_vector[idx].append(0)
                    # n_num += 1
            self.cal_blank(body_movement_length[idx], 1)
            self.cal_blank(body_movement_vector[idx], 2)
            # print('결과==============')
            # for index, ratio in enumerate(body_movement_length[idx]):
            #     print("%d 번째 ratio : %f" % (index, ratio))
            # print('채워진것 : %d' % m_num)
            # print('안채워진것 : %d' % n_num)
            # print('다시 채운것 : %d' % nm_num)

        frames_len_1 = len(body_movement_length[0])
        frames_len_2 = len(body_movement_vector[0])
        for i in range(pairs_len):
            if frames_len_1 != len(body_movement_length[i]):
                print("%d : length numbers are not same" % i)
                frames_len_1 = len(body_movement_length[i])
                print(frames_len_1)
            if frames_len_2 != len(body_movement_vector[i]):
                print("%d : vector numbers are not same" % i)
                frames_len_2 = len(body_movement_vector[i])
                print(frames_len_2)

        if frames_len_1 == frames_len_2:
            frame_len = frames_len_1

        # center (x, y)
        centers = []
        cento = self.ex_center[ex_type]
        for i in range(frame_len):
            if dynamic_num[i] == 1:
                centers.append((dynamic_skeleton[i][cento][0], dynamic_skeleton[i][cento][1]))
            else:
                centers.append(0)

        self.cal_blank(centers, 3)
        # pp(centers)
        print(len(centers))
        # x, y, length
        final_orders = []
        for i in range(frame_len):
            final_orders.append([])
            final_orders[i].append((centers[i][0], centers[i][1], 0))
            for j in range(pairs_len):
                final_orders[i].append((body_movement_vector[j][i][0], body_movement_vector[j][i][1], body_movement_length[j][i]))
        # pp(final_orders)
        keypoints = np.array(final_orders)

        return keypoints

    def cal_blank(self, array, option):
        first = 1 if array[0] == 0 else 0
        last = 1 if array[-1] == 0 else 0
        if first == 1 or last == 1:
            i = 0
            while first == 1 or last == 1:
                if first == 1 and array[i] != 0:
                    first = array[i]
                    for index in range(i):
                        array[index] = first

                if last == 1 and array[-(i+1)] != 0:
                    last = array[-(i+1)]
                    for index in range(i):
                        array[-(index+1)] = last
                i+=1
        last_value = 0
        last_index = 0
        for index, ratio in enumerate(array):
            if ratio == 0:
                if last_index == 0:
                    last_index = index
            else:
                if last_index != 0:
                    #print("%d번째 Ratio : %f" % (index, ratio))
                    n = index - last_index
                    if option == 1:
                        reg_add = (ratio - last_value) / (index - last_index + 1)
                    elif option == 2:
                        reg_add = self.diff_degree(ratio, last_value) / (index - last_index + 1)
                    else:
                        reg_add = tuple(np.divide(np.subtract(ratio, last_value), index - last_index + 1))

                    for i in range(n):
                        if option == 1:
                            array[last_index+i] = last_value + reg_add * (i + 1)
                        elif option == 2:
                            deg = self.degree(last_value)
                            array[last_index+i] = self.coordinates(deg + reg_add * (i + 1))
                        else:
                            array[last_index+i] = tuple(np.add(last_value, np.multiply(reg_add, i+1)))
                    last_index = 0
                    last_value = ratio
                else:
                    #print("%d번째 Ratio : %f" % (index, ratio))
                    last_value = ratio
        # for index, ratio in enumerate(array):
        #     print("%d 번째 ratio : <%f, %f>" % (index, ratio[0], ratio[1]))

    def distance(self, joint_1, joint_2):
        x_diff = math.pow(joint_1[0]-joint_2[0], 2)
        y_diff = math.pow(joint_1[1]-joint_2[1], 2)
        dist = math.sqrt(x_diff + y_diff)
        # print(dist)
        return dist

    def norm_vector(self, joint_1, joint_2):
        dist = self.distance(joint_1, joint_2)
        vec_x = (joint_1[0] - joint_2[0]) / dist
        vec_y = (joint_1[1] - joint_2[1]) / dist
        return (vec_x, vec_y)

    def diff_degree(self, joint_1, joint_2):
        deg_1 = self.degree(joint_1)
        deg_2 = self.degree(joint_2)
        diff = deg_2 - deg_1
        return diff

    def coordinates(self, degree):
        x = np.cos(degree)
        y = np.sin(degree)
        return (x, y)

    def degree(self, joint):
        # deg1 = np.degrees(np.arccos(joint[0]))
        # deg2 = np.degrees(np.arcsin(joint[1]))
        # if deg1 <= 90.0:
        #     if deg2 > 0:
        #         deg = deg1
        #     else:
        #         deg = deg2
        # else:
        #     if deg2> 0:
        #         deg = deg1
        #     else:
        #         deg = -math.pi-deg2
        if joint[1] > 0 :
            deg = np.degrees(np.arccos(joint[0]))
        else:
            deg = np.degrees(2.0*math.pi - np.arccos(joint[0]))

        return deg


CocoColors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]

CocoPairs = [
    (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (1, 11),
    (11, 12), (12, 13), (1, 0), (0, 14), (14, 16), (0, 15), (15, 17), (2, 16), (5, 17)
]   # = 19
CocoPairsRender = CocoPairs[:-2]

class MyException(Exception):
    pass

if __name__=='__main__':
    c = Common()
    print(c.average([1,23,45,51]))
