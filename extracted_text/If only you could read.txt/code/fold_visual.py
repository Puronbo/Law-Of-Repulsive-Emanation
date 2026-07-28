import numpy as np
import matplotlib.pyplot as plt

# 90-degree crease example
x = np.linspace(-3, 3, 500)
y = np.abs(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=3, label='|x| — the 90° crease function')
plt.plot([-3,0], [3,0], 'r--', linewidth=2, label='Left ray (slope -1)')
plt.plot([0,3], [0,3], 'g--', linewidth=2, label='Right ray (slope +1)')
plt.axvline(0, color='k', linestyle=':', label='Crease line')
plt.title('Your Core Intuition: Folding the 90° Crease')
plt.xlabel('x'); plt.ylabel('f(x)')
plt.legend(); plt.grid(True)
plt.show()  # or plt.savefig('90_degree_fold.png')