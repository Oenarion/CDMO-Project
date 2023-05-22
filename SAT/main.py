from z3 import *
from itertools import *
import math
import numpy as np
from cardinality_constraints import *
from printer import *
from arithmetic_op import *

import sys
sys.path.insert(0, 'instances')
from parser import *

#input model
m = 3 #couriers
n = 7 #items
l = [15, 10, 7] #max load per courier
s= [3,2, 6, 8, 5, 4, 4] #weight of each item
D = [[0, 3, 3, 6, 5, 6, 6, 2], #distances
    [3, 0, 4, 3, 4, 7, 7, 3],
    [3, 4, 0, 7, 6, 3, 5, 3],
    [6, 3, 7, 0, 3, 6, 6, 4],
    [5, 4, 6, 3, 0, 3, 3, 3],
    [6, 7, 3, 6, 3, 0, 2, 4],
    [6, 7, 5, 6, 3, 2, 0, 4],
    [2, 3, 3, 4, 3, 4, 4, 0]]

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



"""
#tours = [[[Bool(f"tour{i}_{j}_{k}") for k in range(depth_tours)] for j in range(n-m+3)] for i in range(m)]
matrix = [[[False for _ in range(depth_tours)] for _ in range(n-m+3)] for _ in range(m)]

for var_name, value in model:
    if var_name.startswith("tour"):
        parts = var_name.split("_")
        row = int(parts[1])
        col = int(parts[2])
        layer = int(parts[3])
        matrix[row][col][layer] = value
"""


def main():
    #m, n, l, s, D = parseInstance("instances/inst01.dat")

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
    tours = [[[Bool(f"tour{i}_{j}_{k}") for k in range(depth_tours)] for j in range(n-m+3)] for i in range(m)]

    weights=[[[Bool(f"weight{i}_{j}_{k}") for k in range(depth_weight)] for j in range(n-m+3)] for i in range(m)]
    
    #constraint 1: each item exactly once
    for i in range(1,n+1): #iterate on 1,2,3...5
        # for each [i][j] where bin(item_index) == [j][j][:] --> add constraint exactly_once
        solver.add(exactly_one_np(find(i,n,m,tours,depth_tours)))
        
    # constraint if there is the origin point, then all the number after it must be n+1
    # because he have terminated the journey
    for i in range(m):
        for j in range(2, n-m+3-1):
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
    bool_vars = [[tours[i][j] for j in range(n-m+3)] for i in range(m)]
    solver.add(at_least_k_seq(bool_vars=find(0,n,m,tours,depth_tours), k=(n-m+3)*m-n, name="at_least_k_0"))
    
    max_distance = max(max(D, key=lambda x: max(x))) #compute the maximum distance among all the distances
    depth_distance = math.ceil(math.log2(max_distance+1))
    distances = [[[Bool(f"distance{i}_{j}_{k}") for k in range(depth_distance)] for j in range(n-m+2)] for i in range(m)]
    
    check_weight(solver,n,m,s,depth_tours,depth_weight,tours,weights,capacities)
    create_distances(solver,n,m,D,depth_tours,depth_distance,distances,tours)

    checkModel = solver.check()

    while(str(checkModel) == 'sat'):
        model = solver.model()
        # printer(model,"weight",m,n-m+3,depth_weight)
        # printer(model,"tour",m,n-m+3,depth_tours)
        matrix_of_distances=getMatrix(model, "distance", m, n-m+2, depth_distance)
        current_max_distance=np.max(np.sum(matrix_of_distances,axis=1))-1   #we want to check only distances < of the current max (see check_distances)
        
        #while(str(checkModel) == 'sat'):
        solver.push()
    
        current_binary_max=binary_encoding(current_max_distance,math.ceil(math.log2(max_distance+1)))
        current_binary_max_bool=[]
        for i in range(len(current_binary_max)):        #current_max needs to be in z3
            if(current_binary_max[i]=='0'):
                current_binary_max_bool.append(Bool(f"current_binary_max_{i}"))
        
        solver.add(And(current_binary_max_bool))
        for i in range(m):
            check_distances(solver,n,m,distances,current_binary_max_bool,i)

        checkModel = solver.check()

        print('iterazione')
        if (str(checkModel) == 'unsat'):
            print('facio pop')
            solver.pop()

        print('-'*10)

    solver.check()
    model = solver.model()
    printer(model,"tour",m,n-m+3,depth_tours)
    

if __name__ == "__main__":
    main()
    
    