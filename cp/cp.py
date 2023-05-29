from minizinc import Instance, Model, Solver
import sys, os
from datetime import timedelta
import time
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
    obj = rows[-1].split(' ')[1]
    tourStr = rows[1:len(rows)-1]
    tour = []

    for line in tourStr:
        tmp = []
        for column in line.split(' '):
            if column != '':
                tmp.append(int(column))
        tour.append(tmp)

    terminationTime = time.time()-startingTime
    if math.ceil(time.time()-startingTime) >= 300:
        optimal = "false"
        terminationTime = "300" 
    else:
        optimal = "true"
        terminationTime = str(terminationTime) 

    jsonData = {"sat":{
                "time": str(terminationTime),
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

model = Model("./cp/MCP_cp.mzn")
gecode = Solver.lookup("gecode")
instance = Instance(gecode, model)

startingTime = time.time()
m, n, l, s, D = parseInstance(fileName)

instance['m'] = m
instance['n'] = n
instance['l'] = l
instance['s'] = s
instance['D'] = D


timeout = timedelta(seconds=math.ceil(time.time()-startingTime))

result = instance.solve(timeout=timeout)
jsonData = createJson(result)
    
jsonString = json.dumps(jsonData)
print(jsonString)