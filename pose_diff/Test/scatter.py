import numpy as np
import matplotlib.pyplot as plt

# Create data
N = 500
x = np.random.rand(N) * 100
y = np.random.rand(N) * 100
colors = (0,0,0)
area = np.pi*3

# Plot
plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.title('Scatter plot pythonspot.com')
plt.xlim(-100, 100)
plt.ylim(-100, 100)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
