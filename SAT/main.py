from z3 import *
from itertools import *
import math
import numpy as np
from cardinality_constraints import *
from printer import *
from arithmetic_op import *
from time import perf_counter,sleep
import sys
from threading import Thread,Lock,Event
from jsonToFile import saveJson
import os
import signal
import platform

#set_param("verbose",10)
# currentWorkingDirectory = os.path.abspath(os.getcwd())
# programName = sys.argv[0]
# print(currentWorkingDirectory, programName)

# exit(0)
#pathParser = currentWorkingDirectory + programName.split("/")

try:
    sys.path.insert(0, 'parser')
    from parser import *
except:
    print("Please move into the main folder of the project :)")
    exit(0)

obj = -1
sol = []
secondDimension=-1
m=-1
firstSolutionFound=-1
startingTime=-1
deletedCouriers=[]


def maxNumberItem(s, l):
    max_l = max(l)
    s_copy = s.copy()
    s_copy.sort()
    tmp = 0
    i = 0
    while(tmp+s_copy[i] < max_l):
        tmp = tmp + s_copy[i]
        i += 1
    return i

class myThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.lock=Lock()
        self.data=None
        self._stop_event = Event()
        self.threadPID=os.getpid()
        self.obj = None

        print('hey sonon il thread.. pid: ',self.threadPID)
        
    def run(self):
        #running main
        self.main()
            
    def getValue(self):
        with self.lock:
            print("richiesta di accesso a tipo:",type(self.data))

            if self.data is not None:
                return self.data.copy(),self.obj
            return None,None
                
            
        
    def stop(self):
        self._stop_event.set()
        
    #m courier, l load, s size
    def deleteUselessCouriers(self,m,l,s):
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
    

    def main(self):

            #m, n, l, s, D = parseInstance("instances/inst01.dat")
            
            try:
                fileName = sys.argv[1]
            except:
                print("Give me the name of the file like first parameter")
                exit(0)

            global m
        
            m, n, l, s, D = parseInstance(fileName)
            
            global deletedCouriers
            deletedCouriers=self.deleteUselessCouriers(m,l,s)
            m=m-len(deletedCouriers)
            
            newL=[]
            for i in range(len(l)):
                if i not in deletedCouriers:
                    newL.append(l[i])
                    
            l=newL
        
            global firstSolutionFound
            global startingTime
            global secondDimension
            secondDimension=n-m+3

            solver = Solver() # create a solver s

            # encoding of the sizes of items
            max_weight = max(s) #compute the maximum weight among all items
            depth_weight = math.ceil(math.log2(max_weight+1))

            # encoding of the capacity of each couriers
            max_capacity = max(l) #compute the maximum capacity among all couriers
            depth_capacity = math.ceil(math.log2(max_capacity+1))
            capacities = [[Bool(f"capacity{i}_{j}") for j in range(depth_capacity)] for i in range(m)]
            for i in range(m):
                binary_enc = bin(l[i])[2:].rjust(depth_capacity, '0')
                for j in range(depth_capacity):
                    if binary_enc[j] == '0':
                        solver.add(Not(capacities[i][j]))
                    else:
                        solver.add(capacities[i][j])

            #control parameters
            depth_tours = math.ceil(math.log2(n+1))


            """
            tours: 3 boolean arrays, each position in each row is the delivery index. starting from origin point, ending in origin point
            ex: [0,1,2,0]
                [0,3,0,0]
                [0,4,0,0]
            """
            tours = [[[Bool(f"tour{i}_{j}_{k}") for k in range(depth_tours)] for j in range(secondDimension)] for i in range(m)]

            weights=[[[Bool(f"weight{i}_{j}_{k}") for k in range(depth_weight)] for j in range(secondDimension)] for i in range(m)]
            
            #constraint 1: each item exactly once
            for i in range(1,n+1): #iterate on 1,2,3...5
                # for each [i][j] where bin(item_index) == [j][j][:] --> add constraint exactly_once
                solver.add(exactly_one_np(find(i,n,m,tours,depth_tours)))
                
            # constraint if there is the origin point, then all the number after it must be n+1
            # because he have terminated the journey
            for i in range(m):
                for j in range(2, secondDimension-1):
                    tmp = []
                    tmp2 = []
                    for k in range(depth_tours): 
                        tmp.append(Not(tours[i][j][k]))
                        tmp2.append(Not(tours[i][j+1][k]))
                    # tmp2 = []
                    # for k in range(depth_tours): 
                    #     tmp2.append(Not(tours[i][j+1][k]))
                    solver.add(Implies(And(tmp), And(tmp2)))
                    
                # tmp constraint on the starting point
                tmp = []
                # tmp2 constraint To achieve a fair division among drivers, 
                # each courier must have at least an item (because n>=m)
                tmp2 = []
                for k in range(depth_tours):
                    tmp.append(Not(tours[i][0][k]))
                    tmp2.append(tours[i][1][k])
                solver.add(And(tmp))
                solver.add(Or(tmp2))

            # for i in range(m):
            #     tmp = []
            #     for k in range(depth_tours):
            #         tmp.append(Not(tours[i][0][k]))
            #     solver.add(And(tmp))

            # constraint To achieve a fair division among drivers, 
            # each courier must have at least an item (because n>=m)
            # for i in range(m):
            #     tmp = []
            #     for k in range(depth_tours):
            #         tmp.append(tours[i][1][k])
            #     solver.add(Or(tmp))


            # constraint to have the exact number of 0 in the matrix       
            solver.add(at_least_k_seq(bool_vars=find(0,n,m,tours,depth_tours), k=(secondDimension)*m-n, name="at_least_k_0"))
            
            max_distance = max(max(D, key=lambda x: max(x))) #compute the maximum distance among all the distances
            depth_distance = math.ceil(math.log2(max_distance+1))
            distances = [[[Bool(f"distance{i}_{j}_{k}") for k in range(depth_distance)] for j in range(secondDimension-1)] for i in range(m)]
            
            check_weight(solver,n,m,s,depth_tours,depth_weight,tours,weights,capacities)
            create_distances(solver,n,m,D,depth_tours,depth_distance,distances,tours)

            #solver.set("timeout", 60000)
            firstSolutionFound=True
            startingTime=perf_counter()
            checkModel = solver.check()
            print(checkModel)

            if str(checkModel) == 'sat':

                model = solver.model()
                printer(model, "weight", m, secondDimension, depth_weight)
                printer(model,"tour",m,secondDimension,depth_tours)
                printer(model, "distance", m, secondDimension-1, depth_distance)
                matrix_of_distances=getMatrix(model, "distance", m, secondDimension-1, depth_distance)

                lastDistanceFound = np.max(np.sum(matrix_of_distances,axis=1))   #we want to check only distances < of the current max (see check_distances)
                lastDistanceFailed = 0
                lastDistanceTrial = lastDistanceFound // 2
                solutionFound = True
                
                obj = lastDistanceFound
                sol = getMatrix(model, "tour", m, secondDimension, depth_tours)
                print("lastDistanceFound: ", lastDistanceFound)
                # with self.lock:
                #     self.data=sol
                #     self.obj=obj
                
                while(lastDistanceFound - lastDistanceFailed > 1):

                    lastDistanceTrial = (lastDistanceFailed + lastDistanceFound) // 2
                    
                        
                    print("last_distance_failed",lastDistanceFailed)
                    print("last_distance_found",lastDistanceFound)
                    print("last_distance_trial", lastDistanceTrial)
                    print("found",solutionFound)

                    # creating a new level
                    solver.push()
                    print("Try for: ", lastDistanceTrial)
                    print(lastDistanceFound,lastDistanceTrial)               
                    # binary encoding of the max distrance
                    current_binary_max = binary_encoding(lastDistanceTrial, math.ceil(math.log2(lastDistanceTrial + 1)))
                    # creting the z3 binary values
                    current_binary_max_bool=[Bool(f"current_binary_max_{i}") for i in range(len(current_binary_max))]
                    # imposing that the binary encoding is equal to the number
                    current_binary_max_bool_list = []
                    for i in range(len(current_binary_max)):
                        if current_binary_max[i] == '0':
                            current_binary_max_bool_list.append(Not(current_binary_max_bool[i]))
                        else:
                            current_binary_max_bool_list.append(current_binary_max_bool[i])
                    
                    solver.add(And(current_binary_max_bool_list))
                    
                    # constraint on the distances: each distance must be less or equal w.r.t. the one for which we are trying
                    for i in range(m):
                        res = check_distances(solver,n,m,distances,current_binary_max_bool,i)
                        # we add to the solver the bit representing the sign of the subtraction
                        # between the maximum distance and the sum of the distances travelled by each courier
                        solver.add(res)
        
                    # check if there is a solution
                    print("I'M ALIVE!")
                    checkModel = solver.check()
                    print("checkModel = ", checkModel)
                    if str(checkModel) == 'sat':
                        # solutionFound = True
                        model = solver.model()
                        # printer(model,"weight",m,secondDimension,depth_weight)
                        printer(model,"tour",m,secondDimension,depth_tours)
                        matrix_of_distances=getMatrix(model, "distance", m, secondDimension-1, depth_distance)
                        #printer(model,"distance",m,secondDimension,depth_tours)
                        lastDistanceFound = np.max(np.sum(matrix_of_distances,axis=1))   #we want to check only distances < of the current max (see check_distances)
                        obj = lastDistanceFound
                        sol = getMatrix(model, "tour", m, secondDimension, depth_tours)
                        print("lastDistanceFound: ", lastDistanceFound)
                        
                    else:
                        # solutionFound = False
                        lastDistanceFailed = lastDistanceTrial

                    # with self.lock:
                    #     self.data=sol
                    #     self.obj=obj
                    solver.pop()
                    print('-'*10)

                    with self.lock:
                        self.data=sol
                        self.obj=obj
                        print('lock conclusa e aggiornata: ',obj)


                print("Last solution found: ", obj)
                print("sol :", sol)
                printer(model,"tour",m,secondDimension,depth_tours)
                printer(model,"weight",m,secondDimension,depth_weight)
                printer(model,"distance",m,secondDimension-1,depth_distance)
            

if __name__ == "__main__":


    #Windows and Linux use 2 different signal to kill the threads
    if platform.system()=="Windows":
        signalKill=signal.SIGILL
    else:
        signalKill=signal.SIGKILL
        
    # thread = Process(target=main, args=(id(counter),))
    mainThread=myThread()
    mainThread.start()

    threadPID=os.getpid()
    print(threadPID)
    
    startingTime = perf_counter()

    terminationTime = 300
    
    while not firstSolutionFound:
        #print("I'm here")
        sleep(10)
    while(mainThread.is_alive() and perf_counter()-startingTime <= terminationTime):
        sleep(0.1)
    

    sol,obj=mainThread.getValue()
    print(type(sol))
    mainThread.stop()

    if sol:
        sol=[[sol[i][j] for j in range(secondDimension) if sol[i][j]!=0]for i in range(m)]
    
    #insert of empty cells for couriers not used
    for i in deletedCouriers:
        sol.insert(i,[])

    if mainThread.is_alive():
        optimal = False
        print("thread killed")
    else:
        terminationTime = math.floor(perf_counter() - startingTime)
        optimal = True

    
    print(f"execution time: {terminationTime}s", )

    if sol is not None:

        print("il risultato è un bel tipo del tipo: ",type(sol))

        jsonData = {"sat":{ 
                "time": terminationTime,
                "optimal": optimal,
                "obj": int(obj),
                "sol": sol
            }}
    else:
        sol=[]
        for i in range(m):
            sol.append([])
        jsonData = {"smt":{
                "time": terminationTime,
                "optimal": optimal,
                "obj": "N/A",
                "sol" : sol
            }}

    saveJson(sys.argv[1],jsonData)

    os.kill(threadPID,signalKill) #killo tutto

