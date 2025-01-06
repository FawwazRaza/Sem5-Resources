import numpy as np

a = [2, 2, 4, 2, 2]
n = len(a)
c = [1, 2, 0, 1, ]
d = [-1, -1, -1, -1]
b = [1, 2, -1, -2, -1]
u = np.zeros((n, 1))
y = np.zeros((n, 1))
x = np.zeros((n, 1))

#STEP 1: Calculating diagonal of upper triangular matrix:
u[0] = a[0]
for i in range(1, n):
    u[i] = a[i] - c[i - 1] * d[i - 1] / u[i - 1]

print('u=')
print(u)

#STEP 2: Calculating y from L*Y=b:
y[0] = b[0]
for i in range(1, n):
    y[i] = b[i] - c[i - 1] * y[i - 1] / u[i-1]

print('y=')
print(y)

#STEP 2: Calculating x from U*X=Y:
x[n - 1] = y[n - 1] / u[n - 1]
for i in range(n - 2, -1, -1):
    x[i] = (y[i] - d[i] * x[i + 1]) / u[i]

print('x=')
print(x)