class Common():
    def __init__(self):
        self.PART_NAMES = ['nose', 'neck',  'rshoulder', 'relbow', 'rwrist', 'lshoulder', 'lelbow', 'lwrist', 'rhip', 'rknee', 'rankle', 'lhip', 'lknee', 'lankle', 'reye', 'leye', 'rear', 'lear']
        # 각 부위별 인식률
        self.initial_parts = [0.6 for i in range(18)]
        # 전체 인식률 (한 프레임)
        self.accuracy = .75
        # 전체 인식률 (동영상 전체)
        self.agv_accuracy = 0.8
        self.ex_parts = [
        [],
        [],
        [],
        [0.5, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0] # walk
        ]


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
            print("accuracy %d # : %f" % (idx, accuracy[idx]))
            if accuracy[idx] >= avg_acc:
                if exit_flags == 1:
                    print("Found Target Frame")
                    print("Found Target Frame Number is #%d" % idx)
                    return accuracy[idx], [frame]
                else:
                    accurate_frame_num.append(1)
                    accurate_frame.append(frame)
            else:
                accurate_frame_num.append(0)

        avg_accuracy = self.average(accuracy)
        print("This frames accuracy is %f" % avg_accuracy)

        return avg_accuracy, [accurate_frame, accurate_frame_num]

    def average(self, list):
        sum = 0
        for item in list:
            sum += item
        return sum/len(list)

    def fname(arg):
        pass



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
