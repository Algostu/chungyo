import numpy as np
import matplotlib.pyplot as plt


def save_graph(i,name):

    file_1 = np.load('skeleton1.npy')
    file_2 = np.load('skeleton2.npy')


    '''
        body[0] = 코
        body[1] = 목
        body[2] = 왼쪽 어깨
        body[3] = 왼쪽 팔꿈치
        body[4] = 왼쪽 손목
        body[8] = 왼쪽 골반
    '''
    joints=list(zip(*file_1))
    joints_2=list(zip(*file_2))

    # Shoulder to hip
    syuagol_vecs = []
    arm_vecs = []
    arm_vecs2 = []
    sonmock_vecs = []

    syuagol_vecs2 = []
    arm_vecs3 = []
    arm_vecs4 = []
    sonmock_vecs2 = []

    for a, b, c, d in zip(joints[1], joints[2], joints[3], joints[4]):
        syuagol_vecs.append((a[0] - b[0], a[1] - b[1]))
        arm_vecs.append((b[0] - c[0], b[1] - c[1]))
        arm_vecs2.append((c[0] - b[0], c[1] - b[1]))
        sonmock_vecs.append((d[0] - c[0], d[1] - c[1]))

    for a, b, c, d in zip(joints_2[1], joints_2[2], joints_2[3], joints_2[4]):
        syuagol_vecs2.append((a[0] - b[0], a[1] - b[1]))
        arm_vecs3.append((b[0] - c[0], b[1] - c[1]))
        arm_vecs4.append((c[0] - b[0], c[1] - b[1]))
        sonmock_vecs2.append((d[0] - c[0], d[1] - c[1]))



    # normalize vectors
    syuagol_vecs = syuagol_vecs / np.expand_dims(np.linalg.norm(syuagol_vecs, axis=1), axis=1)
    arm_vecs = arm_vecs / np.expand_dims(np.linalg.norm(arm_vecs, axis=1), axis=1)
    arm_vecs2 = arm_vecs2 / np.expand_dims(np.linalg.norm(arm_vecs2, axis=1), axis=1)
    sonmock_vecs = sonmock_vecs / np.expand_dims(np.linalg.norm(sonmock_vecs, axis=1), axis=1)

    syuagol_vecs2 = syuagol_vecs2 / np.expand_dims(np.linalg.norm(syuagol_vecs2, axis=1), axis=1)
    arm_vecs3 = arm_vecs3 / np.expand_dims(np.linalg.norm(arm_vecs3, axis=1), axis=1)
    arm_vecs4 = arm_vecs4 / np.expand_dims(np.linalg.norm(arm_vecs4, axis=1), axis=1)
    sonmock_vecs2 = sonmock_vecs2 / np.expand_dims(np.linalg.norm(sonmock_vecs2, axis=1), axis=1)

    # Check if raised all the way up

    angles_1 = np.degrees(np.arccos(np.sum(np.multiply(arm_vecs2,syuagol_vecs), axis=1)))
    angles_2 = np.degrees(np.arccos(np.clip(np.sum(np.multiply(arm_vecs, sonmock_vecs), axis=1), -1.0, 1.0)))
    angles_3 = np.degrees(np.arccos(np.sum(np.multiply(arm_vecs4, syuagol_vecs2), axis=1)))
    angles_4 = np.degrees(np.arccos(np.clip(np.sum(np.multiply(arm_vecs3, sonmock_vecs2), axis=1), -1.0, 1.0)))

    for idx, a,b,c,d in zip(range(len(joints[1])), joints[1], joints[2], joints[3], joints[4]):
        if ((b[1]-a[1])/(b[0]-a[0]))*(c[0] - a[0]) + a[1] > c[1]:
            angles_1[idx] = 360 - angles_1[idx]

    for idx, a,b,c,d in zip(range(len(joints_2[1])), joints_2[1], joints_2[2], joints_2[3], joints_2[4]):
        if ((b[1]-a[1])/(b[0]-a[0]))*(c[0] - a[0]) + a[1] > c[1]:
            angles_3[idx] = 360 - angles_3[idx]

    if i==1:
        output_M=angles_1
        output_T=angles_3
    else:
        output_M=angles_2
        output_T=angles_4

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
    fig.savefig(name)