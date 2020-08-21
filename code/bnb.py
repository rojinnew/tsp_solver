'''===================================================
*author: Rojin Aliehyaei
*description: Branch-and-Bound algorithm 
*Georgia Institute of Technology, Fall 2018
====================================================='''
import copy
from utils import readfile
from heapq import *
import time

'''===================
   state class that helps to obtain the list of vistied and univisited cities 
======================'''
class branch_state:
    def __init__(self, d, adj_matrix ,edge_list,  visited_vertices , cost ):
        self.dim = d 
        self.visited_vertices = copy.copy(visited_vertices)
        self.adj_matrix = adj_matrix
        self.sorted_edge_list = edge_list
        self.cost = cost
        self.lower_bound = self.calculate_lower_bound() 


    '''===================
     These methods help to arrange the states in priority queue 
      ======================'''
    def __lt__(self, otherNode):
        return self.lower_bound < otherNode.lower_bound
    def __gt__(self, otherNode):
        return self.lower_bound > otherNode.lower_bound
    def __eq__(self, otherNode):
        return self.lower_bound == otherNode.lower_bound
    '''===================
      add_vertex function adds the next selected vertex to the partial solution
      it also updates the state lower bound if needed 
      ======================'''
    def add_vertex(self,vertex):
        if len(self.visited_vertices) != 0:
            self.cost += self.adj_matrix[self.visited_vertices[-1]][vertex]
        else:
            self.cost = 0 
        self.visited_vertices.append(vertex)
        if len(self.visited_vertices) != (self.dim + 1):
            self.lower_bound = self.calculate_lower_bound() 
        # if we found a tour no need to update the lower bound
        else: 
            self.lower_bound = self.cost 
    '''===================
     This method calculates the lower bound of a given state based on 2 shortest edges 
      ======================'''
    def calculate_lower_bound(self):
       # for each vertex that is not in the visited vertices 
       # sum the weight of two minimum  adjacent vertices
       sum2_shortest_edge = 0
       for v1 in range(0,self.dim):
            vertex2_short_edge = 0 
            if v1 not in self.visited_vertices:
                e  = self.sorted_edge_list[v1][:]
                cnt = 0
                for i in range(0,self.dim):
                    # closest city index 
                    v2 = e[i][1] 
                    if(v1 != v2) and (v2 not in self.visited_vertices):
                        cnt = cnt +1
                        vertex2_short_edge = e[i][2]+ vertex2_short_edge 
                        if(cnt==2):
                            break;
                sum2_shortest_edge+= vertex2_short_edge 
       temp =  self.sorted_edge_list[0][1][2]
       return ((sum2_shortest_edge/2) + temp+ self.cost)
    

    '''===================
      main function for bnb invoked by main
      This is a non-recursive branch-and-bound based on dfs 
      - First, read the data file and construct the graph 
      - Create a state for an arbitrary vertex and push into stack 
      - If a valid tour is constructed check its cost and compare against best solution
      - Update the best solution if needed
      - If state is not correspond to a solution, expand current state into new state 
      - Consider the lowerbound of each state before pushing it into stack
        , if it is larger than best solution bound the node 
      - At the top of stack you should have the vertex that is closest to the current state 
      - Repeate the step until the time is not over or the stack is empty 
      ======================'''
def bnb(file_name, cut_time, random_seed,start_time):
    # read the data, and return the adj_matrix using readfile in utils.py
    dim, adj_matrix = readfile(file_name)
    length = len(file_name)-4
    instance = file_name[0:length]
    method = "BnB"
    output_file = "output/" + instance+"_" +method+"_"+str(cut_time)
    complete_trace_output_file = output_file + ".trace"
    output_trace = open(complete_trace_output_file, 'wt')
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
    # create a new instance of branch satate
    current_state = branch_state(dim,adj_matrix, sorted_edge_list, [],0)
    #Initiate the class
    best_tour_sofar= None
    # add the first city
    current_state.add_vertex(0)
    #priority queue is defined to keep insatnce of branchState, 
    #create a priority queue and select the state with smallest lower bound first
    #pq = []
    #heappush(pq, current_state)
    #while (len(pq) > 0) and (time.time() - start_time) < cut_time:
    stack = []
    stack.append(current_state)
    timestamp_cost =[]
    while (len(stack) > 0) and (time.time() - start_time) < cut_time:
        #current_state = heappop(pq)
        current_state = stack.pop()
        #print("current_state.visited_vertices", current_state.visited_vertices)
        # if we do not have any best tour or the the calculated lower bound 
        # for the current state is smaller than the best tour
        if (not best_tour_sofar) or (current_state.lower_bound < best_tour_sofar.cost):
            # if we visited all the node
            if len(current_state.visited_vertices) == dim:
                current_state.add_vertex(current_state.visited_vertices[0])
                # if this is the first tour or current path cost is less than what we had 
                # update the best_tour_sofar 
                if (not best_tour_sofar) or (current_state.cost < best_tour_sofar.cost):
                     current_time = time.time()-start_time
                     if(current_time < cut_time):
                        best_tour_sofar= current_state
                        output_trace.write("%.10f" % current_time + ", " + str(best_tour_sofar.cost) + "\n")
                        timestamp_cost.append((current_time, best_tour_sofar.cost))
                    

            # if we have not visited all the node
            else:  
                # for the vertices that haven't been visited create a new state instance
                # keep the closest state at the top of stack 
                for i in range(dim-1,0,-1):    
                    vertex = sorted_edge_list[current_state.visited_vertices[-1]][i][1] 
                    if vertex not in current_state.visited_vertices :
                        new_state = branch_state(current_state.dim, current_state.adj_matrix,
                                     current_state.sorted_edge_list, current_state.visited_vertices,
                                     current_state.cost)
                        new_state.add_vertex(vertex)    
                        if not  best_tour_sofar or new_state.lower_bound < best_tour_sofar.cost:
                            #heappush(pq, new_state) 
                            stack.append(new_state) 

    # we are done with brnaching and priority Queue is empty             
    #total_time = time.time()-start_time
    complete_sol_output_file = output_file +".sol"
    output_sol = open(complete_sol_output_file, 'wt')
    if(len(timestamp_cost) !=0):
        total_time = timestamp_cost[-1][0]
        tour_cost = best_tour_sofar.cost
        output_sol.write(str(best_tour_sofar.cost)+"\n")
        best_tour_sofar.visited_vertices = [ c+1 for c in best_tour_sofar.visited_vertices]
        output_sol.write(", ".join(map(str,best_tour_sofar.visited_vertices[:-1])))
        print("best solution's timestamp", timestamp_cost[-1][0])
        print("optimal tour cost", tour_cost)
    else:
        output_sol.write("No valid solution found.")
