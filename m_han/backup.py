# length 빈것 채우기
first = 1 if body_movement_length[idx][0] == 0 else 0
last = 1 if body_movement_length[idx][-1] == 0 else 0
if first == 1 or last == 1:
    i = 0
    while first == 1 or last == 1:
        if first == 1 and body_movement_length[idx][i] != 0:
            first = body_movement_length[idx][i]
            for index in range(i):
                body_movement_length[idx][index] = first

        if last == 1 and body_movement_length[idx][-(i+1)] != 0:
            last = body_movement_length[idx][-(i+1)]
            for index in range(i):
                body_movement_length[idx][-(index+1)] = last
        i+=1

last_value = 0
last_index = 0
for index, ratio in enumerate(body_movement_length[idx]):
    if ratio == 0:
        if last_index == 0:
            last_index = index
    else:
        if last_index != 0:
            #print("%d번째 Ratio : %f" % (index, ratio))
            n = index - last_index
            reg_add = (ratio - last_value) / (index - last_index + 1)
            for i in range(n):
                nm_num += 1
                body_movement_length[idx][last_index+i] = last_value + reg_add * (i + 1)
            last_index = 0
            last_value = ratio
        else:
            #print("%d번째 Ratio : %f" % (index, ratio))
            last_value = ratio
