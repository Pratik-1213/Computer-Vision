import numpy as np

m1 = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9]
])
m2 = np.array([
    [9,8,7],
    [6,5,4],
    [3,2,1]
])

print(m1+m2)
print(np.add(m1,m2))
print(m1.size)
print(m1.shape)

print(np.size(m1))