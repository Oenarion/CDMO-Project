from minizinc import Instance, Model, Solver
import sys, os
from datetime import timedelta
from time import perf_counter
import math
import json

deletedCouriers=[]

try:
    sys.path.insert(0, 'parser')
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

    #insert of empty cells for couriers not used
    for i in deletedCouriers:
        tour.insert(i,[])
        
    terminationTime = perf_counter()-startingTime
    if math.ceil(perf_counter()-startingTime) >= 300:
        optimal = False
        terminationTime = 300 
    else:
        optimal = True
        terminationTime = str(terminationTime) 

    jsonData = {"cp":{
                "time": int(terminationTime.split('.')[0]),
                "optimal": optimal,
                "obj": int(obj),
                "sol": tour
            }}
    return jsonData


def deleteUselessCouriers(m,l,s):
    #sort s and l
    sortedS=s*1
    sortedS.sort()
    
    sortedL=l*1
    sortedL.sort()
    
    #now that we sorted couriers and packages we check if all couriers could at least
    #carry the smallest packages assigned to them
    #For example: if there is a package of size 5 and two couriers of load size 5 only
    #one will carry the item
    delCouriers=[]
    for i in range(len(l)):
        if sortedL[i]<sortedS[i]:
            currIndex=l.index(sortedL[i])
            delCouriers.append(currIndex)
    return delCouriers    


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


deletedCouriers=deleteUselessCouriers(m,l,s)
m=m-len(deletedCouriers)

newL=[]
for i in range(len(l)):
    if i not in deletedCouriers:
        newL.append(l[i])
        
l=newL

instance['m'] = m
instance['n'] = n
instance['l'] = l
instance['s'] = s
instance['D'] = D

#print('heiii')
timeout = timedelta(seconds=300-math.ceil(perf_counter()-startingTime))

result = instance.solve(timeout=timeout)

print(result)

if not result:
    terminationTime=300
    result="N/A"
    optimal=False
    tours=[[]]*m

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

directory="res/CP/"

try:
    f = open(f"{directory}{fileName}.json", "w")
    f.write(jsonString)
    f.close()
except Exception as e:
    print(e)
    print("errore scrittura file json")

