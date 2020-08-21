'''===================================================
*author: Rojin Aliehyaei
*description: Solving TSP using Simulated Annealing Algorithm                
*Georgia Institute of Technology, Fall 2018
====================================================='''
import copy
from utils import readfile
import time
import random
from math import sqrt,exp
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
   sa function is the main method for simulated annealing
   - read the data
   - set the parameters including temp, min_temp, cooling_rate, and random seed
   - initiate the current solution and best solution using initiate_solution function
   - check if the termination condition met
   - if for (numb_repeat) iterations no improvment achieved,
      purturb the current solution using double_bridge fun.
   - else find a new candidate using a single 2-opt move
   - if the new candidate is better than current solution accept it
     and update the best solution if it is needed 
   - else if random< exp(-(candidate_cost - current_cost) / temp) accept it 
   - update the current tempreture using cooling rate
======================'''
def sa(file_name, cut_time, random_seed,start_time):
    # read the data, and return the adj_matrix using readfile in utils.py
    dim, adj_matrix = readfile(file_name)
    temp = 10000 
    min_temp = 0.0001
    cooling_rate = 0.999999
    random.seed(random_seed)
    time_length = time.time() - start_time
    t = 0
    #current_solution = random.sample(range(0,dim),dim)
    random_vertex = random.randint(0, dim - 1)
    #current_solution =  initiate_solution(adj_matrix, dim, random_vertex, file_name, cut_time, random_seed,start_time)
    current_solution =  initiate_solution(adj_matrix, dim, random_vertex)
    best_tour_sofar = current_solution
    initial_cost = compute_cost(current_solution,adj_matrix,dim)
    current_cost = initial_cost 
    best_cost = current_cost 
    length = len(file_name)-4
    instance = file_name[0:length]
    method = "LS1"
    output_file = "output/" + instance+"_" +method+"_"+str(cut_time)
    complete_trace_output_file = output_file +"_"+str(random_seed)+".trace"
    output_trace = open(complete_trace_output_file, 'w')
    current_time = time.time() - start_time
    output_trace.write("%.10f" %current_time + ", " + str(best_cost) + "\n")
    timestamp_cost = []
    timestamp_cost.append((current_time,best_cost))
    numb_repeat = 500 
    cost_list = [current_cost]
    # create an edge list that is sorted  by weight in each row
    sorted_edge_list = []
    edge_list = []
    for i in range(0, dim):
        el=[]
        for j in range(0, dim):
            el.append((i,j,adj_matrix[i][j]))
            el.sort(key=lambda x:x[2])
            edge_list.append((i,j,adj_matrix[i][j]))
        sorted_edge_list.append(el)

    while((time.time() - start_time) < cut_time):
            t = t + 1
            if(len(cost_list)== numb_repeat) and all(item == cost_list[0] for item in cost_list):
                candidate = double_bridge(current_solution,random)
            else:
                candidate = current_solution[:]
                l = random.randint(2,dim-1)
                near = sorted_edge_list[l][1:5]
                x = random.randint(0,len(near)-1)
                random_near = near[x]
                src, dst , weight = near[x]
                s1 = current_solution.index(l)
                s2 = current_solution.index(dst) 
                if(s1 >s2):
                    s1,s2 = s2,s1
                #candidate[start:(start+l)] = reversed(candidate[start:(start+l)])
                candidate[s1:s2] = reversed(candidate[s1:s2])
            candidate_cost = compute_cost(candidate,adj_matrix,dim)
    
            if candidate_cost < current_cost:
                current_cost = candidate_cost
                current_solution = candidate
                if candidate_cost < best_cost:
                    current_time = time.time()-start_time
                    if(current_time < cut_time):
                        best_cost = candidate_cost
                        best_tour_sofar = candidate
                        output_trace.write("%.10f" % (time.time() - start_time) + ", " + str(best_cost) + "\n")
            else:
                r = random.random()
                if r < exp(-(candidate_cost - current_cost) / temp):
                    current_solution = candidate
                    current_cost = candidate_cost
            temp *= cooling_rate
            if(len(cost_list)<numb_repeat):
                cost_list.append(current_cost)
            else:
                cost_list.pop(0)
                cost_list.append(current_cost)
    print('Best cost obtained: ', best_cost)
    complete_sol_output_file = output_file +"_"+str(random_seed)+".sol"
    output_sol = open(complete_sol_output_file, 'w')
    output_sol.write(str(best_cost)+"\n")
    best_tour_sofar = [ c+1 for c in best_tour_sofar] 
    output_sol.write(", ".join(map(str,best_tour_sofar)))

