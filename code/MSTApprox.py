'''===================================================
*author: Rojin Aliehyaei
*description: Solving TSP using MST Aprroximation                 
*Georgia Institute of Technology, Fall 2018
====================================================='''
from utils import readfile,dfsPreorder
from mst import unionFind 
from mst import computeMST 
import random
import time
'''===================================================
mst_approximation is the main method invoked by main  
-Read data from instance tsp file 
-Build mst tree using Kruskal's algorithm using computeMST function
-Perform prorder tree walk using dfsPreorder function 
-Build the approximate tour using result of dfsPreorder 
====================================================='''
def mstapprox(file_name,cut_time, random_seed,start_time):
    timestamp_cost = []
    # read data and set the distance matrix
    dim, adj_matrix = readfile(file_name)
    edge_list = []
    for i in range(0, dim):
        for j in range(0, dim):
            edge_list.append((i,j,adj_matrix[i][j]))
    # build the MST using kruskal implemented in mst.py
    MST_cost,T = computeMST(adj_matrix, edge_list, dim) 
    mst_G = {}      
    T = sorted(T, key=lambda x: int(x[2]))
    for e in T:
        if(e[0] not in mst_G):
            mst_G[e[0]] = []
        mst_G[e[0]].append(e[1])
        if(e[1] not in mst_G):
            mst_G[e[1]] = []
        mst_G[e[1]].append(e[0])
    visited = [-1]*dim
    v_visited = []
    # perform a dfs on the mst tree and store the order of visiting vertices 
    random.seed(random_seed)
    random_vertex = random.randint(0, dim - 1)
    dfsPreorder(mst_G,random_vertex, 0, visited, v_visited)
    i = 0
    tour = []
    tour_cost= 0
    # build tour using the order of visited vertex 
    # in dfs and compute the tour cost 
    while(i < dim):
        l1 = v_visited[i]
        l2= v_visited[(i+1)%dim]
        tour.append( (l1, l2,adj_matrix[l1][l2]))
        tour_cost+= adj_matrix[l1][l2] 
        i+=1 
    total_time = time.time() - start_time
    timestamp_cost.append((total_time, tour_cost))
    return total_time, v_visited, tour_cost
