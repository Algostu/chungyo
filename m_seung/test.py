from m_seung.coco import  AnglePairs
import numpy as np

trainer = np.load('../data/user/IU/walk/trained_skeleton.npy')

trainer_angle = []
user_angle = []
tangle = [None]*18
uangle = [None]*18
list = [1,2,3]
list2 = [4,5,6]
list3 = [7,8,9]
trainer_angle.append(list)
trainer_angle.append((list2))
print(list3)
print(trainer_angle)

list3[0] = list[0]
list3[1] = list[1]
list3[2] = list[2]

print(list3)

list[0] = 10
print(list3)