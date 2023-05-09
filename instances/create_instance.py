import sys
import subprocess
import numpy as np

if len(sys.argv)  != 3:
    print("Not enough aruments given. Expected:\nnumber of courier\nnumber of items")
    exit(1)
try:
    n_courier = int(sys.argv[1])
except:
    print("The first argument must be an integer")
    exit(1)
try:
    n_items = int(sys.argv[2])
except:
    print("The second argument must be an integer")
    exit(1)

# sizes = np.round(np.random.normal(30, 5, n_courier))
sizes = np.random.randint(5, 51, n_courier)

checkWeigths = False
while(not checkWeigths):
    weights = np.random.randint(1, 10, n_items)
    if sum(weights) <= sum(sizes) and max(weights) <= max(sizes):
        checkWeigths = True

print(f"m = {n_courier};\nn = {n_items};")
print(f"l = {sizes};\ns = {weights};")

res = subprocess.run(["minizinc", "getDistances.mzn", "-D", f"m={n_courier};n={n_items};"], capture_output=True)
distances = str(res.stdout).split(';')[0].split('\'')[1]
for el in distances.split('\\n'):
    print(el)
print(";")
