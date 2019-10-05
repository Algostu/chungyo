############################################
# Basic Info
# 공통적으로 쓰이는 함수와 데이터들의 집합

# Feature
#

# Todo
# DB와 Common의 Exercise 정보가 서로 겹친다. 즉, DB에서 Common에 있는 정보를 가져가든, Common에서 DB에 있는 정보를 가져가든 방식을 바꿔야한다.
############################################

import math
import numpy as np
import enum
import matplotlib.pyplot as plt
import math

def check_accuracy(frames, exercise_type):
    ############################################
    # Basic Info
    # 인식률을 판단한다.
    # front와 side로 나눠서 진행한다.
    # side의 경우 둘중 하나만 인식이 잘되도 통과한다.

    # Feature
    #

    # Todo
    # Test function을 여러개 만들어서 여러 test 결과를 만들어야 한다.
    ############################################
    if exercise_type >= 0 and exercise_type < 4:
        view = View[exercise_type-1]
        norm_acc = Accuracys[exercise_type-1]
        required_parts = Parts[exercise_type-1][:]
        avg_acc = Accuracys[exercise_type-1]
        required_parts_len = len(list(filter(lambda x: x >= ACC_CRE, required_parts)))
        accuracy = [ 0 for i in range(len(required_parts))]
        frame_len = len(frames)
        avg_accuracy = 0
    else:
        raise MyException('exercise_type are between 1 and 3')

    for idx, frame in enumerate(frames):
        for part_idx, part_accuracy in enumerate(required_parts):
            if frame[part_idx][2] > part_accuracy:
                accuracy[part_idx] += 1
            else:
                accuracy[part_idx] += 0

    if view == 'side':
        required_parts_len = required_parts_len / 2 + 1
        avg_accuracy = [0, 0]
        left = [0, 1, 2, 3, 4, 8, 9, 10]
        right = [0, 1, 5, 6, 7, 11, 12, 13]
        for idx, acc, need in zip(range(len(required_parts)), accuracy, required_parts):
            if need >= ACC_CRE:
                agv_acc = acc/frame_len
                if idx in left:
                    avg_accuracy[0] += agv_acc
                else:
                    avg_accuracy[1] += agv_acc
        avg_accuracy[0] /= required_parts_len
        avg_accuracy[1] /= required_parts_len
        avg = max(avg_accuracy)
        if avg >= norm_acc:
            return True, avg
        else:
            return False, avg
    else:
        for acc, need in zip(accuracy, required_parts):
            if need >= ACC_CRE:
                agv_acc = acc/frame_len
                avg_accuracy += agv_acc

        avg_accuracy /= required_parts_len
        if avg_accuracy >= norm_acc:
            return True, avg_accuracy
        else:
            return False, avg_accuracy

def get_math_info(ex_type, static_skeleton, dynamic_skeleton):
    vectors = VectorPairs[ex_type-1]
    parts = PartPairs[ex_type-1]
    target_pairs = Pairs[ex_type-1][:]
    pairs_len = len(target_pairs)

    body_measurements = []
    body_movement_length = [[] for i in range(pairs_len)]
    body_movement_vector = [[] for i in range(pairs_len)]
    body_movement_angle = [[] for i in range(pairs_len)]

    # calculate vector, length
    for idx,  pairs in enumerate(target_pairs):
        body_measurements.append(distance(static_skeleton[pairs[0]], static_skeleton[pairs[1]]))
        fixed_len = body_measurements[idx]

        for index in range(len(dynamic_skeleton)):
            tuple = [dynamic_skeleton[index][pairs[0]], dynamic_skeleton[index][pairs[1]]]
            if tuple[0][2] > 0 and  tuple[1][2]> 0:
                body_movement_length[idx].append(distance(tuple[0], tuple[1])/fixed_len)
                body_movement_vector[idx].append(norm_vector(tuple[0], tuple[1]))
            else:
                body_movement_length[idx].append(0)
                body_movement_vector[idx].append(0)

        fill_blank_circle(body_movement_length[idx], 1)
        fill_blank_circle(body_movement_vector[idx], 2)

    # filter noise
    # Bug : 구동이 되는지 확인하고 고쳐야 한다.
    # Issue : 플러스 마이너스가 바뀌었을것이다.
    # get_angle을 통해서 구하게 되면 바뀐 각도가 적용이 안된다.
    for vector, part in zip(vectors, parts):
        angles = [get_angle((0,0), b, b+c) for b, c in zip(body_movement_vector[vector[0]], body_movement_vector[vector[1]])]
        filter_noise(body_movement_length[vector[1]])
        noises = filter_noise(angles)
        body_movement_vector[vector[1]] = [(cos(get_angle((1,0),(0,0), a)-noise), sin(get_angle((1,0),(0,0), a)-noise)) for a, noise in zip(body_movement_vector[vector[1]], noises)]

    # check length of vectors and lengths
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

    # calculate center points
    centers = []
    cento = Centers[ex_type-1]

    for i in range(frame_len):
        if  dynamic_skeleton[i][cento][2] > 0:
            centers.append((dynamic_skeleton[i][cento][0], dynamic_skeleton[i][cento][1]))
        else:
            centers.append(0)

    fill_blank_straight(centers)

    # summerize
    final_orders = []
    for i in range(frame_len):
        final_orders.append([])
        final_orders[i].append((centers[i][0], centers[i][1], 0))
        for j in range(pairs_len):
            final_orders[i].append((body_movement_vector[j][i][0], body_movement_vector[j][i][1], body_movement_length[j][i]))

    keypoints = np.array(final_orders)

    return keypoints

def fill_blank_circle(array, option):
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
                    reg_add = diff_degree(ratio, last_value) / (index - last_index + 1)
                else:
                    reg_add = tuple(np.divide(np.subtract(ratio, last_value), index - last_index + 1))

                for i in range(n):
                    if option == 1:
                        array[last_index+i] = last_value + reg_add * (i + 1)
                    elif option == 2:
                        deg = degree(last_value)
                        array[last_index+i] = coordinates(deg + reg_add * (i + 1))
                    else:
                        array[last_index+i] = tuple(np.add(last_value, np.multiply(reg_add, i+1)))
                last_index = 0
                last_value = ratio
            else:
                #print("%d번째 Ratio : %f" % (index, ratio))
                last_value = ratio

def fill_blank_straight(array, test_opt = False, title='Test filter_outlier'):
    ######################################################
    # Params
    # array : target array, 2차원 배열
    # test_opt : figure를 출력 및 저장 하고 싶을 경우 사용
    # title : figure의 title을 정할때 사용

    # How it works
    # 신뢰도가 0.5 보다 낮을 경우 주변 점들을 이용해서 유추한 점을 사용한다.
    # 유추한 점의 신뢰도는 주변 점의 신뢰도도 대체된다.
    # 신뢰도가 0에 가까운 점들을 filtering하는데 효과적이다.
    # 평균 신뢰도가 0.5 아래인 경우에는 사용할 수 없는 방법이다. 따라서 아래와 같은 방법을 제시한다.
    # 신뢰도의 기준을 신뢰도의 median과 average를 이용해서 둘중 하나라도 0.5 아래인경우 더 낮은 값을 기준으로 outlier를 제거한다.
    # 추가로 0.5는 인위적인 값이다. 이러한 값을 정하기 위해서는 실제 outlier가 제거된 비율이 가장 높은 경우를 여러 테스트를 통해서 정해야한다.

    # Feature
    # Test Mode가 지원되서 실제로 얼마만큼의 공백이 채워졌는지를 알 수 있다.
    # fill_blank_circle는 원운동인 반면 이건 직선 운동을 채운다.

    # Todo
    # 1. 0.5
    # confidence score를 얼마만큼 믿을 수 있는지 확인할 수 있는 방법
    ########################################################
    credit = ACC_CRE
    import statistics
    norm = min(credit, statistics.median(list(zip(*array))[2]), sum([element[2] for element in array])/len(array))
    if test_opt == True:
        median = [statistics.median(list(zip(*array))[2])]
        maxs = [max(list(zip(*array))[2])]
        mins = [min(list(zip(*array))[2])]
        avg_accuracy = [sum([element[2] for element in array])/len(array)]
        import matplotlib.pyplot as plt
        plt.figure(figsize=(16,12))
        plt.plot(list(zip(*array))[2], label = "Before filter_outlier")
        plt.suptitle(title)

    first = 1 if array[0][2] < credit else 0
    last = 1 if array[-1][2] < credit else 0
    if first == 1 or last == 1:
        i = 0
        while first == 1 or last == 1:
            if first == 1 and array[i][2] >= credit:
                first_val = array[i]
                first = 0
                for index in range(i):
                    array[index] = first_val

            if last == 1 and array[-(i+1)][2] >= credit:
                last_val = array[-(i+1)]
                last = 0
                for index in range(i):
                    array[-(index+1)] = last_val
            i+=1
    last_value = np.array([0,0,0])
    last_index = 0
    for index, ratio in enumerate(array):
        if ratio[2] < credit:
            if last_index == 0:
                last_index = index
        else:
            if last_index != 0:
                n = index - last_index
                reg_add = np.divide(np.subtract(ratio, last_value), index - last_index + 1)
                for i in range(n):
                    array[last_index+i] = np.add(last_value, np.multiply(reg_add, i+1))
                    array[last_index+i][2] = last_value[2]
                last_index = 0
                last_value = ratio
            else:
                last_value = ratio
    if test_opt == True:
        maxs.append(max(list(zip(*array))[2]))
        mins.append(min(list(zip(*array))[2]))
        median.append(statistics.median(list(zip(*array))[2]))
        avg_accuracy.append(sum([element[2] for element in array])/len(array))
        textstr = '\n'.join((
            '+Before Calc_blank',
            r'$\mu=%.2f$' % (avg_accuracy[0], ),
            r'$\mathrm{median}=%.2f$' % (median[0], ),
            r'$\mathrm{max}=%.2f$' % (maxs[0], ),
            r'$\mathrm{min}=%.2f$' % (mins[0],),
            '+After Calc_blank',
            r'$\mu=%.2f$' % (avg_accuracy[1], ),
            r'$\mathrm{median}=%.2f$' % (median[1], ),
            r'$\mathrm{max}=%.2f$' % (maxs[1], ),
            r'$\mathrm{min}=%.2f$' % (mins[1],)))

        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        plt.text(0.8, 0.5, textstr, transform=plt.gcf().transFigure, fontsize=12,
                verticalalignment='top', bbox=props)

        plt.plot(list(zip(*array))[2], 'bo', label = "After filter_outlier")
        plt.axhline(avg_accuracy[0], c='r', label = "Average Accuracy before : %f" % avg_accuracy[0], ls=':')
        plt.axhline(avg_accuracy[1], c='b', label = "Average Accuracy After : %f" % avg_accuracy[1], ls='--')
        plt.legend()
        plt.subplots_adjust(right=0.78)
        # plt.savefig(title)
        plt.show()

def filter_noise(unfiltered_list):
    target = [0 for i in range(len(unfiltered_list))]
    noises = []
    space = 5
    for i in range(0,len(unfiltered_list),space):
        a = (unfiltered_list[i + space - 1] - unfiltered_list[i]) / space
        b = unfiltered_list[i]
        for j in range(space):
            noises.append(unfiltered_list[i+j] - a*j + unfiltered_list[i])
    tmp = list(filter(lambda x: x != 0, noises))
    noise_certain = sum(tmp)/len(tmp)
    unnatural = noise_certain / 3

    for idx, noise in enumerate(noises):
        if abs(noise) > noise_certain:
            if noise > 0:
                unfiltered_list[idx] -= unnatural
                target[idx] -= unnatural
            else:
                unfiltered_list[idx] += unnatural
                target[idx] += unnatural

    return target

def apply_vector(ex_type, length, vector):
    parts = Parts[ex_type][:]
    pairs = Pairs [ex_type][:]
    length = length[0]
    frames_len = len(vector)
    frames = []
    # print(length)
    basic_length = []
    for pair in pairs:
        basic_length.append(distance(length[pair[0]], length[pair[1]]))
    # pp(basic_length)

    n = 0
    for i in range(frames_len):
        frames.append([(0, 0, 0) for i in range(18)])
        # neck (x, y, 0)신뢰도는 0으로 고정
        frames[i][1] = tuple(vector[i][0])
        # rshoulder
        if parts[2] > 0:
            # n += 1
            frames[i][2] = calc_coordinates(frames[i][1], tuple(vector[i][1]), basic_length[0])

        # lshoulder
        if parts[5] > 0:
            # n += 1
            frames[i][5] = calc_coordinates(frames[i][1], tuple(vector[i][2]), basic_length[1])

        # rhip
        if parts[8] > 0:
            # n += 1
            frames[i][8] = calc_coordinates(frames[i][1], tuple(vector[i][7]), basic_length[6])

        # lhip
        if parts[11] > 0:
            # n += 1
            frames[i][11] = calc_coordinates(frames[i][1], tuple(vector[i][10]), basic_length[9])

        # nose
        if parts[0] > 0:
            # n += 1
            frames[i][0] = calc_coordinates(frames[i][1], tuple(vector[i][13]), basic_length[12])

        # relbow
        if parts[3] > 0:
            # n += 1
            frames[i][3] = calc_coordinates(frames[i][2], tuple(vector[i][3]), basic_length[2])

        # rwrist
        if parts[4] > 0:
            # n += 1
            frames[i][4] = calc_coordinates(frames[i][3], tuple(vector[i][4]), basic_length[3])

        # lelbow
        if parts[6] > 0:
            # n += 1
            frames[i][6] = calc_coordinates(frames[i][5], tuple(vector[i][5]), basic_length[4])

        # lwrist
        if parts[7] > 0:
            # n += 1
            frames[i][7] = calc_coordinates(frames[i][6], tuple(vector[i][6]), basic_length[5])

        # rknee
        if parts[9] > 0:
            # n += 1
            frames[i][9] = calc_coordinates(frames[i][8], tuple(vector[i][8]), basic_length[7])

        # rankle
        if parts[10] > 0:
            # n += 1
            frames[i][10] = calc_coordinates(frames[i][9], tuple(vector[i][9]), basic_length[8])

        # lknee
        if parts[12] > 0:
            # n += 1
            frames[i][12] = calc_coordinates(frames[i][11], tuple(vector[i][11]), basic_length[10])

        # lankle
        if parts[13] > 0:
            # n += 1
            frames[i][13] = calc_coordinates(frames[i][12], tuple(vector[i][12]), basic_length[11])



    # print('rshoulder : %d' % n)
    # pp(frames)

    return frames

def calc_coordinates(starting_point, norm_vector_and_size, fixed):
    point = starting_point[:2]
    # print(point)
    vector = (norm_vector_and_size[0], norm_vector_and_size[1])
    size = norm_vector_and_size[2]
    # print(size*fixed)
    coor = tuple(np.add(point, np.multiply(vector, size*fixed))) + (0.0,)
    # print(coor)
    return coor

def average(list):
    sum = 0
    for item in list:
        sum += item
    return sum/len(list)

def distance(joint_1, joint_2):
    x_diff = math.pow(joint_1[0]-joint_2[0], 2)
    y_diff = math.pow(joint_1[1]-joint_2[1], 2)
    dist = math.sqrt(x_diff + y_diff)
    # print(dist)
    return dist

def norm_vector(joint_1, joint_2):
    dist = distance(joint_1, joint_2)
    vec_x = (joint_1[0] - joint_2[0]) / dist
    vec_y = (joint_1[1] - joint_2[1]) / dist
    return (vec_x, vec_y)

def diff_degree(joint_1, joint_2):
    deg_1 = degree(joint_1)
    deg_2 = degree(joint_2)
    diff = deg_2 - deg_1
    return diff

def coordinates(degree):
    x = np.cos(degree)
    y = np.sin(degree)
    return (x, y)

def degree(joint):

    if joint[1] > 0 :
        deg = np.degrees(np.arccos(joint[0]))
    else:
        deg = np.degrees(2.0*math.pi - np.arccos(joint[0]))

    return deg

def get_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def get_body_len(frame):
    parts = [(1,2),(1,5),(1,8),(1,11),(2,3),(3,4),(5,6),(6,7),(8,9),(9,10),(11,12),(12,13)]
    length = 0
    for part in parts:
        length += distance(frame[part[0]], frame[part[1]])
    return length

CocoColors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]

CocoPairs = [
    (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (1, 11),
    (11, 12), (12, 13), (1, 0), (0, 14), (14, 16), (0, 15), (15, 17), (2, 16), (5, 17)
]   # = 19
CocoPairsRender = CocoPairs[:-2]

PART_NAMES = ['nose', 'neck',  'rshoulder', 'relbow', 'rwrist', 'lshoulder', 'lelbow', 'lwrist', 'rhip', 'rknee', 'rankle', 'lhip', 'lknee', 'lankle', 'reye', 'leye', 'rear', 'lear']


# 0.squat
# 1.pull up
# 2.shoulderpress
ACC_CRE = 0.5
Accuracys = [0.72, 0.72, 0.72]
Parts = [
[ACC_CRE for i in range(14)] + [0, 0, 0, 0], # squat side
[ACC_CRE for i in range(9)] + [0, 0, ACC_CRE, 0, 0, 0, 0, 0, 0], # Pull_up front
[ACC_CRE for i in range(9)] + [0, 0, ACC_CRE, 0, 0, 0,  0, 0, 0] # shoulder_press front
]
View = [
'side',
'front',
'front'
]
Pairs = [
CocoPairs[:-6],
CocoPairs[:7]+CocoPairs[9:10],
CocoPairs[:7]+CocoPairs[9:10]
]
Centers = [1, 1, 1, 1]

VectorPairs = [
[(0,2), (2, 3), (1, 4), (4, 5), (6, 7), (7, 8), (9, 10), (10, 11)],
[(0,2), (2, 3), (1, 4), (4, 5)],
[(0,2), (2, 3), (1, 4), (4, 5)]
]

PartPairs = [
[1, 2, 3], [2,3,4], [1,5,6], [5,6,7], [1,8,9], [8,9,10], [1,11,12], [11,12,13],
[1, 2, 3], [2,3,4], [1,5,6], [5,6,7],
[1, 2, 3], [2,3,4], [1,5,6], [5,6,7]
]

AnglePairs = [(1,2,3),(2,3,4),(3,2,8),(8,9,10),(1,5,6),(5,6,7),(6,5,11),(11,12,13)]
AnglePart = [2,3,1,9,5,6,1,12]

class CocoPart(enum.Enum):
    Nose = 0
    Neck = 1
    RShoulder = 2
    RElbow = 3
    RWrist = 4
    LShoulder = 5
    LElbow = 6
    LWrist = 7
    RHip = 8
    RKnee = 9
    RAnkle = 10
    LHip = 11
    LKnee = 12
    LAnkle = 13
    REye = 14
    LEye = 15
    REar = 16
    LEar = 17
    Background = 18

class MyException(Exception):
    pass
