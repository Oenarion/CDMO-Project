from minizinc import Instance, Model, Solver
import sys, os
from datetime import timedelta
from time import perf_counter
import math
import json


try:
    sys.path.insert(0, 'instances')
    from parser import *
except:
    print("Please move into the main folder of the project :)")
    exit(0)

def createJson(result):
    
    rows = str(result).split("\n")
    print(rows)
    obj = rows[-1].split(': ')[1]
    tourStr = rows[1:len(rows)-1]
    tour = []
    
    for line in tourStr:
        tmp = []
        for column in line.split(' '):
            if column != '':
                currentInt=int(column)
                if currentInt!=n+1:
                    tmp.append(int(column))
        tour.append(tmp)
        
    terminationTime = perf_counter()-startingTime
    if math.ceil(perf_counter()-startingTime) >= 300:
        optimal = "false"
        terminationTime = "300" 
    else:
        optimal = "true"
        terminationTime = str(terminationTime) 

    jsonData = {"cp":{
                "time": terminationTime.split('.')[0],
                "optimal": optimal,
                "obj": str(obj),
                "sol": tour
            }}
    return jsonData


try:
    fileName = sys.argv[1]
except:
    print("Give me the name of the file like first parameter")
    exit(0)

# with open("cp/CP_temp.mzn","w") as f:
#     with open("./cp/MCP_cp.mzn","r") as f2:
#         #f.write(str([f"{string}" for string in f2.readlines()]))
#         f.write(str(f2.readlines()).split("\n"))
#     f.write(searchSelection[int(sys.argv[2])])
#     # with open("./cp/MCP_solvePrinter.txt","r") as f3:
#     #     f.write(str([f"{string}" for string in f3.readlines()]))

# exit(1)

#we need to pass the model of cp so that we can choose the strategy to search the solution
try:    
    model = Model(str(sys.argv[2]))
except(Exception):
    print("Model of cp needed")
    exit(1)
    
if "chuffed" in sys.argv[3]:
    solver = Solver.lookup("chuffed")
else:
    solver=Solver.lookup("gecode")
instance = Instance(solver, model)

startingTime = perf_counter()
m, n, l, s, D = parseInstance(fileName)

instance['m'] = m
instance['n'] = n
instance['l'] = l
instance['s'] = s
instance['D'] = D

#print('heiii')
timeout = timedelta(seconds=300-math.ceil(perf_counter()-startingTime))

result = instance.solve(timeout=timeout)

print(result)

jsonData = createJson(result)
    
jsonString = json.dumps(jsonData)
print(jsonString)

#rimozione stringa
print(fileName)
if "/" in fileName:
    fileName=fileName.split("/")[-1]
    print(fileName)
if "inst0" in fileName:
    fileName = fileName[5:6]
else:
    fileName = fileName[4:6]

print(fileName)

#creazione del file JSON

directory="results/CP/"

try:
    f = open(f"{directory}{fileName}.json", "w")
    f.write(jsonString)
    f.close()
except Exception as e:
    print(e)
    print("errore scrittura file json")

