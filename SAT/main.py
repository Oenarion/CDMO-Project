from z3 import *
from itertools import *
import math
from cardinality_constraints import *
from printer import *
from arithmetic_op import *

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

# m = 5
# n = 20
# l = [15, 43, 42, 16, 42]
# s= [5, 4, 3, 5, 6, 3, 9, 5, 6, 1, 6, 4, 8, 3, 1, 4, 8, 6, 8, 8]
# D = [  [0, 10,  5,  2, 11,  7, 20, 16,  6,  1, 18, 20, 15, 19, 17, 10, 18, 19,  6, 13, 10],
#   [20,  0, 16, 10,  7, 16, 17,  9, 16, 11,  9, 15, 13,  9, 12, 13,  8, 14,  9,  6,  6],
#   [19, 20,  0, 15, 11,  7, 18, 12, 16, 10, 19, 15, 11, 20, 18, 10, 15, 16,  7, 19, 12],
#   [17, 16, 11,  0, 19,  8, 19, 20, 14, 18, 17, 18, 16, 20, 19, 14, 20, 20, 11, 20, 17],
#   [13, 11, 12, 11,  0, 16, 20, 12, 17, 14,  9, 17, 18, 15, 11,  9, 15, 19, 19, 16, 14],
#   [17, 13,  7,  9, 16,  0, 20, 13, 14, 12, 19, 19, 11, 13, 16, 11, 14, 20,  7, 12, 16],
#   [10,  9, 13, 10, 11, 15,  0, 10,  9,  8, 10,  7,  7,  8,  5, 11,  6, 11,  6, 13,  9],
#   [15,  8, 14, 15,  4, 20, 14,  0, 19, 15,  8, 14, 17, 16, 11, 12,  8, 20, 10, 12, 14],
#   [11, 14, 14,  4, 19, 12, 15, 19,  0, 10, 18, 16, 16, 17, 15, 12, 13, 18, 13, 19, 11],
#   [10, 19, 12,  8, 15,  9, 20, 18, 16,  0, 19, 20, 17, 19, 18, 12, 18, 18,  7, 14, 11],
#   [17, 10, 12, 17, 15, 19, 14, 14, 19, 17,  0,  8, 13, 10,  9, 15, 14, 15, 12, 12, 14],
#   [16,  9, 15, 12,  7, 18, 20, 10, 20, 14, 16,  0,  9, 13, 11, 10, 13,  9, 12,  8, 10],
#   [19, 17, 15, 17, 12, 10, 17, 11, 16, 16, 17, 10,  0, 12, 18, 18, 17, 11,  7,  8, 15],
#   [20, 12, 19, 11, 11, 15, 12, 18, 15, 19, 14, 12, 18,  0, 13, 19, 17, 14, 15, 13, 16],
#   [14, 12, 11,  9, 18, 16, 18, 16, 20,  8, 16, 20, 15, 17,  0,  7,  9, 18, 12, 11, 18],
#   [12, 13, 17,  8, 19, 12, 13, 19, 18,  9, 14, 19, 10, 13, 16,  0, 15, 16, 13, 15, 19],
#   [13,  7, 13, 13,  9, 14, 12,  9, 14,  7, 12, 11, 14, 15, 10, 13,  0, 19,  9,  7,  9],
#   [13, 12,  9, 15, 13, 14, 18, 13, 11, 10, 15, 14, 12, 20, 20, 10, 15,  0,  5,  6, 13],
#   [16, 17, 19, 12, 18, 14, 16, 14, 18, 17, 12, 20, 13, 16, 19, 17, 15, 16,  0, 15, 10],
#   [20, 13, 11, 10, 11, 14, 18,  9, 18, 15, 10, 16, 12, 20, 19, 11, 12, 19, 17,  0, 10],
#   [17,  9, 16, 15, 14, 11, 14, 10, 12, 15,  9, 10,  8, 18, 12, 15, 16, 19, 12,  9,  0],
#  ]

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
    checkDistances(solver,n,m,D,depth_tours,depth_distance,distances,tours)

    print(solver.check())


    model = solver.model()
    #printGivenName(model, "final")
    printer(model,"weight",m,n-m+3,depth_weight)
    printer(model,"tour",m,n-m+3,depth_tours)
    printer(model, "distance", m, n-m+2, depth_distance)


if __name__ == "__main__":
    main()
    
    