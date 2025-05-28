import numpy as np
import matplotlib.pyplot as plt

alpha = np.fromfile("alpha.dat", dtype=np.uint32)
gamma = np.fromfile("gamma.dat", dtype=np.uint32)
time = np.fromfile("time.dat", dtype=np.uint32)
timesum = np.fromfile("timesum.dat", dtype=np.uint32)

plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(alpha)
plt.title("Alpha Signal")

plt.subplot(2, 2, 2)
plt.plot(gamma)
plt.title("Gamma Signal")

plt.subplot(2, 2, 3)
plt.plot(time)
plt.title("Time Delay")

plt.subplot(2, 2, 4)
plt.plot(timesum)
plt.title("Time Sum")

plt.tight_layout()
plt.show()