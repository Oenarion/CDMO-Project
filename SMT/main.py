import numpy as np
from z3 import *
from printer import printer
from multiprocessing import Process
from threading import Thread,Lock,Event,get_native_id
from time import perf_counter,sleep
import sys
import json
import os
import signal
from jsonToFile import saveJson

try:
    sys.path.insert(0, 'instances')
    from parser import *
except:
    print("Please move into the main folder of the project :)")
    exit(0)

obj=-1
matrix_of_tours=[]


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
        
        try:
            fileName = sys.argv[1]
        except:
            print("Give me the name of the file like first parameter")
            exit(0)

        m, n, l, s, D = parseInstance(fileName)

        #refactor dei pesi per comodità ma è SUPER IMPORTANTE PER DOPO
        s.insert(0,0) #inserisco in posizione 0 un peso nullo... comodo per fare il calcolo con starting point

        #--SUPER IMPORTANTE!!!!--------
            #preprocessing of D, we need to have the origin as first row/column for our algorithm to work correctly
            #--SUPER IMPORTANTE!!!!--------

        D.insert(0,D[-1])
        D.pop()
        D=np.array(D)
        D=np.insert(D,0,D[:,-1],axis=1)
        D=D[:,:-1]

        #calcolo valore di upper-bound per la funzione di max
        upper_bound_distances = sum(D[0,:]) + sum(D[:,0]) 
        lastDistanceFound = int(upper_bound_distances)
        #print(upper_bound_distances)

        D=D.tolist()
        #print(D)

        second_dimension = n-m+3

        #solver di SMT
        solver = Solver()

        tours = [IntVector(f"tours_{i}", second_dimension) for i in range(m) ]

        """
        la tours sarà costruita così
        c0 = [0,1,2,0]
        c1 = [0,3,0,0]
        c2 = [0,4,0,0]
        """
        print(type(tours[0][0]))

        #tutti i valori assegnati devono essere nel range 0-n
        for i in range(m):
            solver.add(tours[i][0]==0) #tutti devono partire da starting point
            solver.add(tours[i][1]>0) #tutti devono avere almeno 
            solver.add(tours[i][second_dimension-1]==0) #tutti devono terminare in end/start point
            for j in range(second_dimension):
                solver.add(tours[i][j]<=n) #dominio 0-n
                solver.add(tours[i][j]>=0)

        #prima colonna tutti distinti
        listSecondColumn = []
        for i in range(m):
            listSecondColumn.append(tours[i][1])

        solver.add(Distinct(listSecondColumn))

        #questa la usiamo per indicare che ogni numero (indice di consegna) deve apparire una sola volta!!!
        for k in range(1,n+1):
            #ricordarsi che indice poi sarà n+1 (posizione 0 non usata)

            number_of_pack_const = [tours[i][j] == k for j in range(second_dimension) for i in range(m)] + [1]

            solver.add(AtLeast(number_of_pack_const))
            solver.add(AtMost(number_of_pack_const))

        #----- no hole
        # constraint if there is the origin point, then all the number after it must be n+1
        # because he have terminated the journey
        for i in range(m):
            for j in range(2, second_dimension-1):
                solver.add(Implies(tours[i][j]==0, tours[i][j+1]==0))


        #---handling weights

        for i in range(m):
            # int vector containing in each index the weight of the item that the courier is carrying
            # the item zero has size zero
            effectiveWeight = IntVector(f"effectiveWeight_{i}", second_dimension)
            for j in range(second_dimension):
                for k in range(n+1):
                    # if the courier is carrying the item i-th then the effective weight is equal to the size of this item
                    solver.add(Implies(tours[i][j]==k, effectiveWeight[j]==s[k]))
            # summing the effective weights and imposing that it must be less or equal than the size of the truck
            solver.add(Sum(effectiveWeight)<=l[i])

        #--- handling distances

        effectiveDistances = [IntVector(f"effectiveDistance{i}", second_dimension-1) for i in range(m)]
        # imposing that the distances travelled by the courier is smaller than the previous max distance
        for i in range(m):
            # int vector containing in each index the weight of the item that the courier is carrying
            # the item zero has size zero
            #effectiveDistance = IntVector(f"effectiveDistance{i}", second_dimension-1)
            for j in range(second_dimension-1):
                for k1 in range(n+1):
                    for k2 in range(n+1):
                        # if the courier is carrying the item i-th then the effective weight is equal to the size of this item
                        solver.add(Implies(And(tours[i][j]==k1, tours[i][j+1]==k2), effectiveDistances[i][j]==D[k1][k2]))
            # summing the effective weights and imposing that it must be less or equal than the size of the truck
            solver.add(Sum(effectiveDistances[i])<lastDistanceFound)


        print(solver.check())

        if str(solver.check()) != 'unsat':
            mod = solver.model()

            #per il printer: ricostruire matrice
            matrix_of_tours = printer(mod,"tours",m,second_dimension)
            print(matrix_of_tours)

            couriers_distances = np.zeros(m)
            for i in range(m):
                couriers_distances[i] = sum([D[int(matrix_of_tours[i][j])][int(matrix_of_tours[i][j+1])] for j in range(second_dimension-1)])

            lastDistanceFailed = 0
            lastDistanceTrial = lastDistanceFound // 2
            
            obj = lastDistanceFound
            print("lastDistanceFound: ", lastDistanceFound)

            while(lastDistanceFound - lastDistanceFailed > 1 and self._stop_event.is_set()==False):
                lastDistanceTrial = (lastDistanceFailed + lastDistanceFound) // 2
                        
                print("last_distance_failed",lastDistanceFailed)
                print("last_distance_found",lastDistanceFound)
                print("last_distance_trial", lastDistanceTrial)

                # creating a new level
                solver.push()
                print("Try for: ", lastDistanceTrial)

                for i in range(m):
                    solver.add(Sum(effectiveDistances[i])<lastDistanceTrial)
            
                checkModel = solver.check()
                print("checkModel = ", checkModel)

                if str(checkModel) == 'sat':
                    mod = solver.model()
                
                    matrix_of_tours = printer(mod,"tours",m,second_dimension)
                    print(matrix_of_tours)

                    for i in range(m):
                        couriers_distances[i] = sum([D[int(matrix_of_tours[i][j])][int(matrix_of_tours[i][j+1])] for j in range(second_dimension-1)])

                    lastDistanceFound = max(couriers_distances)   #we want to check only distances < of the current max (see check_distances)
                    obj = lastDistanceFound

                    with self.lock:
                        self.data=matrix_of_tours
                        self.obj=obj
                    
                    print("lastDistanceFound: ", lastDistanceFound)
                else:
                    lastDistanceFailed = lastDistanceTrial

                solver.pop()
                print('-'*10)

        print("Last solution found: ", obj)
        matrix_of_tours = printer(mod,"tours",m,second_dimension)

        print(matrix_of_tours)


        for i in range(m):
            print(sum([D[int(matrix_of_tours[i][j])][int(matrix_of_tours[i][j+1])] for j in range(second_dimension-1)]))
            
       


if __name__ == "__main__":

    # thread = Process(target=main, args=(id(counter),))
    mainThread=myThread()
    mainThread.start()

    threadPID=os.getpid()
    print(threadPID)
    
    startingTime = perf_counter()

    terminationTime = 30
    
    while(mainThread.is_alive() and perf_counter()-startingTime <= terminationTime):
        print(perf_counter()-startingTime)
        sleep(0.5)
    

    matrix_of_tours,obj=mainThread.getValue()
    print(type(matrix_of_tours))
    mainThread.stop()

    if mainThread.is_alive():
        optimal = "false"
        print("thread killed")
    else:
        terminationTime = round(perf_counter() - startingTime,3)
        optimal = "true"

    
    print(f"execution time: {terminationTime}s", )

    if matrix_of_tours is not None:
        jsonData = {"smt":{ 
                "time": str(terminationTime),
                "optimal": optimal,
                "obj": str(int(obj)),
                "sol": matrix_of_tours.astype(int).tolist()
            }}
    else:
        jsonData = {"smt":{
                "time": str(terminationTime),
                "optimal": optimal,
                "obj": "-1",
                "sol" : "None"
            }}

    
    #jsonString = json.dumps(jsonData)
    #print(jsonString)

    saveJson(sys.argv[1],jsonData)

    os.kill(threadPID,signal.SIGKILL) #killo tutto
    
    