'''===================================================
*author: Rojin Aliehyaei
*description: Solving TSP using Iterated local search Algorithm                
*Georgia Institute of Technology, Fall 2018
====================================================='''
import time
import random
from math import sqrt
from utils import readfile

'''===================
   initiate_solution function initiates the solution 
   using nearest neighbor approximation
   ======================'''
def initiate_solution(adj_matrix,dim, random_vertex):
    current_vertex = random_vertex
    solution = [random_vertex]
    not_visited = [ i for i in range(0,dim)]
    not_visited.remove(random_vertex)
    while not_visited:
        minv = float("inf")
        minidx = -1
        for i in range(0,dim):
            if( i in not_visited and adj_matrix[current_vertex][i] < minv):
                minv = adj_matrix[current_vertex][i]
                minidx = i
        current_vertex = minidx
        not_visited.remove(current_vertex)
        solution.append(current_vertex)
    return solution
'''===================
   compute_cost function calculates the cost of a given tour 
   ======================'''
def compute_cost(sol,adj_matrix,dim):
    s = sum([adj_matrix[sol[i - 1]][sol[i]] for i in range(1, dim)]) 
    s = s + adj_matrix[sol[0]][sol[dim - 1]]
    return s
def swap_two_opt(candidate, i, j):
    new_candidate = candidate[0:i]
    new_candidate.extend(reversed(candidate[i:j+1]))
    new_candidate.extend(candidate[j+1:])
    return new_candidate

'''===================
   double_bridge function used for perturbing the solution 
   adapted from:
   www.cleveralgorithms.com/nature-inspired/stochastic/iterated_local_search.html
   ======================'''
def double_bridge(candidate,random):
    dim = len(candidate)
    r = int(dim/4)
    idx1 = 1 + random.randint(0, r)
    idx2 = idx1 + 1 + random.randint(0, r)
    idx3 = idx2 + 1 + random.randint(0, r)
    p1 = candidate[0:idx1]+candidate[idx3:len(candidate)]
    p2 = candidate[idx2: idx3]+candidate[idx1:idx2]
    return p1+p2    
'''===================
   two-opt function is invoked by the main method for iterated local search based on two-opt 
   - Read the data and construct the graph
   - Initiate the current solution and best solution randomly 
   - Check if the termination condition met
   - Perform two-opt iteratively, until no improvement achieved 
   - Purturb the current solution using double_bridge function, if needed 
   - If the new candidate is better than current solution accept it
     , update the best solution if it is needed 
======================'''
def two_opt(file_name, cut_time, random_seed,start_time):
    # set the random seed 
    random.seed(random_seed)
    # read the data, and return the adj_matrix using readfile in utils.py
    dim, adj_matrix = readfile(file_name)
    length = len(file_name)-4
    instance = file_name[0:length]
    method = "LS2"
    output_file = "output/" + instance+"_" +method+"_"+str(cut_time)
    complete_trace_output_file = output_file +"_"+str(random_seed)+".trace"
    output_trace = open(complete_trace_output_file, 'wt')
    t = 0
    #random_vertex = random.randint(0, dim - 1)
    #current_solution =  initiate_solution(adj_matrix, dim, random_vertex)
    iter_best_tour = best_tour_sofar = current_solution = random.sample(range(0,dim),dim) 
    initial_cost = iter_best_cost = best_cost = current_cost = compute_cost(current_solution,adj_matrix,dim)
    output_trace.write("%.10f" % (time.time() - start_time) + ", " + str(best_cost) + "\n")
    cost_list = [current_cost]
    timestamp_cost = []
    timestamp_cost.append(((time.time() - start_time),best_cost))
    improvement =True    
    main_loop_iter = 0
    while((time.time() - start_time) < cut_time):
        main_loop_iter = main_loop_iter + 1
        while((improvement) and (time.time() - start_time) < cut_time):
            t = t + 1
            improvement = False 
            for i in range(dim-1):
                for j in range(i+1, dim): 
                    candidate = swap_two_opt(iter_best_tour, i, j)
                    candidate_cost = compute_cost(candidate,adj_matrix,dim)
                    if candidate_cost < iter_best_cost:
                        iter_best_cost = candidate_cost
                        iter_best_tour = candidate
                        improvement = True 
                        if  iter_best_cost < best_cost: 
                            best_cost = iter_best_cost
                            best_tour_sofar = iter_best_tour 
                            current_time = time.time() - start_time
                            if(current_time < cut_time):
                                output_trace.write("%.10f" %current_time + ", " + str(iter_best_cost) + "\n")
                        break
                if improvement == True:
                    break 
        if(improvement == False and (time.time() - start_time) < cut_time) :
            improvement = True
            iter_best_tour = double_bridge(best_tour_sofar,random) 
            iter_best_cost = compute_cost(iter_best_tour,adj_matrix,dim)
            if  iter_best_cost < best_cost: 
                   best_cost = iter_best_cost
                   best_tour_sofar = iter_best_tour 
                   current_time = time.time() - start_time
                   if(current_time < cut_time):
                        output_trace.write("%.10f" %current_time + ", " + str(iter_best_cost) + "\n")
            

    print("Best cost: ", best_cost)

    complete_sol_output_file = output_file +"_"+str(random_seed)+".sol"
    output_sol = open(complete_sol_output_file, 'wt')
    output_sol.write(str(best_cost)+"\n")
    best_tour_sofar = [ c+1 for c in best_tour_sofar] 
    output_sol.write(", ".join(map(str,best_tour_sofar)))

