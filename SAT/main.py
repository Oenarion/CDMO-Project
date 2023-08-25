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

# Set verbosity level to maximum (this will show debug and error messages)
set_param('verbose', 10)

#os.nice(1)
#os.sched_get_priority_max(1)

# currentWorkingDirectory = os.path.abspath(os.getcwd())
# programName = sys.argv[0]
# print(currentWorkingDirectory, programName)

# exit(0)
#pathParser = currentWorkingDirectory + programName.split("/")

try:
    sys.path.insert(0, 'instances')
    from parser import *
except:
    print("Please move into the main folder of the project :)")
    exit(0)

obj = -1
sol = []


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


#----bellissimo thread

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
            

    def main(self):

        #m, n, l, s, D = parseInstance("instances/inst01.dat")
        
        try:
            fileName = sys.argv[1]
        except:
            print("Give me the name of the file like first parameter")
            exit(0)

        m, n, l, s, D = parseInstance(fileName)
        
        secondDimension=n-m+3

        solver = Solver() # create a solver s

        #ATTENZIONE
        #timeout_milliseconds = 5000
        #solver.set("timeout", timeout_milliseconds)

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
                for k in range(depth_tours): 
                    tmp.append(Not(tours[i][j][k]))
                tmp2 = []
                for k in range(depth_tours): 
                    tmp2.append(Not(tours[i][j+1][k]))
                solver.add(Implies(And(tmp), And(tmp2)))

        # constraint on the starting point
        for i in range(m):
            tmp = []
            for k in range(depth_tours):
                tmp.append(Not(tours[i][0][k]))
            solver.add(And(tmp))

        # constraint To achieve a fair division among drivers, 
        # each courier must have at least an item (because n>=m)
        for i in range(m):
            tmp = []
            for k in range(depth_tours):
                tmp.append(tours[i][1][k])
            solver.add(Or(tmp))


        # constraint to have the exact number of 0 in the matrix       
        solver.add(at_least_k_seq(bool_vars=find(0,n,m,tours,depth_tours), k=(secondDimension)*m-n, name="at_least_k_0"))
        
        max_distance = max(max(D, key=lambda x: max(x))) #compute the maximum distance among all the distances
        depth_distance = math.ceil(math.log2(max_distance+1))
        distances = [[[Bool(f"distance{i}_{j}_{k}") for k in range(depth_distance)] for j in range(secondDimension-1)] for i in range(m)]
        
        check_weight(solver,n,m,s,depth_tours,depth_weight,tours,weights,capacities)
        create_distances(solver,n,m,D,depth_tours,depth_distance,distances,tours)

        print('CHECKPOINT 1'+'-'*20)
        checkModel = solver.check()
        print('CHECKPOINT 2'+'-'*20)

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

            with self.lock:
                    self.data=sol
                    self.obj=obj
                    print('lock conclusa e aggiornata: ',obj)

            
            while(lastDistanceFound - lastDistanceFailed > 1):

                lastDistanceTrial = (lastDistanceFailed + lastDistanceFound) // 2
                    
                print("last_distance_failed",lastDistanceFailed)
                print("last_distance_found",lastDistanceFound)
                print("last_distance_trial", lastDistanceTrial)
                print("found",solutionFound)

                # creating a new level
                solver.push()
                print("Try for: ", lastDistanceTrial)

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

                print('CHECKPOINT 1'+'-'*20)
                checkModel = solver.check()
                print('CHECKPOINT 2'+'-'*20)



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

                solver.pop()
                print('-'*10)

                with self.lock:
                    self.data=sol
                    self.obj=obj
                    print('lock conclusa e aggiornata: ',obj)

                # if self.lock.acquire(blocking=False):
                #     self.data=sol
                #     self.obj=obj
                # else:
                #     print("COLLISION DETECTED D:")

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

    terminationTime = 120
    
    while(mainThread.is_alive() and perf_counter()-startingTime <= terminationTime):
        sleep(0.1)
    

    sol,obj=mainThread.getValue()
    print(type(sol))
    mainThread.stop()

    if mainThread.is_alive():
        optimal = "false"
        print("thread killed")
    else:
        terminationTime = round(perf_counter() - startingTime,3)
        optimal = "true"

    
    print(f"execution time: {terminationTime}s", )

    if sol is not None:

        print("il risultato è un bel tipo del tipo: ",type(sol))

        jsonData = {"sat":{ 
                "time": str(terminationTime),
                "optimal": optimal,
                "obj": str(int(obj)),
                "sol": sol
            }}
    else:
        jsonData = {"sat":{
                "time": str(terminationTime),
                "optimal": optimal,
                "obj": "-1",
                "sol" : "None"
            }}

    saveJson(sys.argv[1],jsonData)

    os.kill(threadPID,signalKill) #killo tutto

