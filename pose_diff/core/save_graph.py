
import matplotlib.pyplot as plt
from pose_diff.core.calculate_angle import get_angle_part

'''
    body[0] = 코
    body[1] = 목
    body[2] = 왼쪽 어깨
    body[3] = 왼쪽 팔꿈치
    body[4] = 왼쪽 손목
    body[8] = 왼쪽 골반
'''
def save_graph(part1,part2,video1,video2,graph_file_name):

    output_M=get_angle_part(part1,video1)
    output_T=get_angle_part(part2,video2)

    plt.figure(figsize=(10,5))
    plt.subplot(131)
    plt.plot(output_M)
    plt.title('User')
    plt.subplot(132)
    plt.plot(output_T)

    plt.title('Trainer')
    plt.subplot(133)
    plt.plot(range(len(output_M)),output_M, 'r', range(len(output_T)), output_T, 'b')
    plt.title('Diff(User-RED,Trainer-BLUE)')
    fig=plt.gcf()
    fig.savefig(graph_file_name)
