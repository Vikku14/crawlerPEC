import numpy as np

# Max-Min Composition given by Zadeh
def maxMin(x, y):
    z = []
    for x1 in x:
        for y1 in y.T:
            z.append(max(np.minimum(x1, y1)))
    return np.array(z).reshape((x.shape[0], y.shape[1]))

# 3 arrays for the example
r1 = np.array([
[0, 0, 0.7, 0.5, 0, 0.3, 0,0,0.5, 0],
[0.1, 0,0,0.3,0,0,0,0.7, 0, 0],
[0.5, 0,0,0,0,0.3,0,0,0,0],
[0.7,0,0.7, 0,0,0.9,0,0,0,0],
[0.9,0,0.7,0.7,0,0.3,0,0.5,0.3,0],
[0,0,0,0,0,0,0,0,0.3,0],
[0.7,0,0,0.5,0,0,0,0.9,0.1,0],
[0.3,0.5,0.1,0.3,0,0.1,0,0,0.3,0],
[0,0,0.5,0,0,0.5,0,0,0,0],
[0.9,0.7,0,0.5,0.9,0,0.5,0,0.5,0]
])

r2 = np.array([
[0, 0, 0.7, 0.5, 0, 0.3, 0,0,0.5, 0],
[0.1, 0,0,0.3,0,0,0,0.7, 0, 0],
[0.5, 0,0,0,0,0.3,0,0,0,0],
[0.7,0,0.7, 0,0,0.9,0,0,0,0],
[0.9,0,0.7,0.7,0,0.3,0,0.5,0.3,0],
[0,0,0,0,0,0,0,0,0.3,0],
[0.7,0,0,0.5,0,0,0,0.9,0.1,0],
[0.3,0.5,0.1,0.3,0,0.1,0,0,0.3,0],
[0,0,0.5,0,0,0.5,0,0,0,0],
[0.9,0.7,0,0.5,0.9,0,0.5,0,0.5,0]
])
cont = 'n'
iteration = 1
while(cont == 'n'):
    print("\n--------------------- Iteration No. ("+ str(iteration)+ ") -------------------------\n")
    r2 = maxMin(r1, r2)
    print(r2)
    print("Driving Power --> ",np.sum(r2, axis=1))

    print("Driven Power --> ",np.sum(r2, axis=0))
    cont = input("\nstablized? [y/n] ")
    iteration = iteration + 1
print("\n---------------------------------------------------------")
print("\nMatrix is stablized on Iteration No. "+ str(iteration-1)+"\n")

row_sum2 = np.sum(r2, axis=1)
row_sum = []
for row in row_sum2:
    l = list()
    l.append(row)
    row_sum.append(l)
r2 = np.append(r2, row_sum, axis=1)
import pandas as pd  

df = pd.DataFrame(r2) 
df.columns += 1

df.index += 1
df.columns = [*df.columns[:-1], 'Driving Power']

print(df)

print("\nDriven Power \n",np.sum(r2, axis=0))
print("---------------------------------------------------------")

