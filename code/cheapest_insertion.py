'''===================================================
*author: Rojin Aliehyaei
*description: Solving TSP using Cheapest Insertion 
*Georgia Institute of Technology, Fall 2018
====================================================='''
from utils import readfile
import time
import random

'''===================
   compute_cost function calculates the cost of a given tour 
   ======================'''
def compute_cost(sol,adj_matrix,dim):
    s = sum([adj_matrix[sol[i - 1]][sol[i]] for i in range(1, dim)]) 
    s = s + adj_matrix[sol[0]][sol[dim - 1]]
    return s

'''===================
   Main method for Cheapest Insertion method 
   -Choose a random vertex i as a starting node
   -Find a node j that is closest to i and form a sub_tour ST = i-j
   -Find an edge (i, j) of the sub_tour and a node k not in the
    sub_tour such that distance = G[i][k]+G[k][j]-G[i][j]
   -Modify the sub_tour by inserting k between i and j.
   ======================'''
def ci(file_name, cut_time, random_seed,start_time):
    random.seed(random_seed)
    t = 0
    # read the data, and return the adj_matrix using readfile in utils.py
    dim, adj_matrix = readfile(file_name)
    length = len(file_name)-4
    instance = file_name[0:length]
    method = "CI"
    output_file = "output/" + instance+"_" +method+"_"+str(cut_time)
    complete_trace_output_file = output_file +"_"+str(random_seed)+".trace"
    output_trace = open(complete_trace_output_file, 'wt')
    current_vertex = random.randint(0, dim - 1)
    tour = [current_vertex]
    tour_length= float('inf')
    not_visited = [ i for i in range(0,dim)]
    not_visited.remove(current_vertex)
    closest_distance = min([adj_matrix[current_vertex][j] for j in not_visited])
    current_vertex = adj_matrix[current_vertex].index(closest_distance)
    tour.append(current_vertex) 
    not_visited.remove(current_vertex)
    while (not_visited and (time.time() -start_time) <cut_time):
        sub_best_dist = float('inf')
        sub_tour = None
        for insertion_candidate in not_visited:
            for idx in range(len(tour)-1):
                i = tour[idx] 
                j = tour[idx+1]  
                distance = adj_matrix[i][insertion_candidate] + adj_matrix[insertion_candidate][j] - adj_matrix[i][j] 
                if distance < sub_best_dist:
                    sub_best_dist = distance
                    sub_tour = tour[:idx+1] + [insertion_candidate] + tour[idx+1:]
                    best_candidate = insertion_candidate 
        tour = sub_tour
        not_visited.remove(best_candidate)
    best_tour_sofar  = tour 
    best_cost = sum([adj_matrix[best_tour_sofar[i - 1]][best_tour_sofar[i]] for i in range(1, dim)]) 
    best_cost = best_cost + adj_matrix[best_tour_sofar[0]][best_tour_sofar[dim - 1]]
    total_time = time.time() -start_time 
    if(total_time <cut_time):
        output_trace.write("%.10f" % (time.time() - start_time) + ", " + str(best_cost) + "\n")
    complete_sol_output_file = output_file +"_"+str(random_seed)+".sol"
    output_sol = open(complete_sol_output_file, 'wt')
    if(total_time <cut_time):
        output_sol.write(str(best_cost)+"\n")
        best_tour_sofar = [ c+1 for c in best_tour_sofar] 
        print('Best cost obtained: ', best_cost)
        output_sol.write(", ".join(map(str,best_tour_sofar)))


