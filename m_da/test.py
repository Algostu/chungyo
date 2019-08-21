
import numpy as np
human = np.array([[1,1],[2,5],[2,1],[4,4],[6,6]])
print (human)
a = np.zeros((5,3))
for i in range(0,5):
    for j in range(0,2):
        a[i][j]=human[i][j]
        a[i][j + 1] = 255

print(a)

