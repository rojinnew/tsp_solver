'''===================================================
*author: Rojin Aliehyaei
*description: This file constin utility function including:
              euc_distance, geo_distance, readfile, dfsPreorder,write_to_file 
*Georgia Institute of Technology, Fall 2018
====================================================='''
from math import sqrt, sin, cos, floor,acos
from numpy import fix
import random
import numpy

'''===================================================
    euc_distance function calculates the euclidean distance 
====================================================='''
def euc_distance(loc1, loc2):
        dis = int(round(sqrt((loc1[0] - loc2[0])*(loc1[0] - loc2[0])+ (loc1[1] - loc2[1])*(loc1[1] - loc2[1]))))
        #print("raw",sqrt((loc1[0] - loc2[0])*(loc1[0] - loc2[0])+ (loc1[1] - loc2[1])*(loc1[1] - loc2[1])))
        return dis

'''===================================================
    geo_distance function calculates the geographical distance 
====================================================='''
def geo_distance(loc1, loc2):
    #x is lat, y is long
    p =  3.141592;
    x1 = loc1[0]
    y1 =loc1[1]
    deg = fix(x1);
    min = x1 - deg;
    rad_x1 = p*(deg + 5.0*min/3.0)/180.0;
    
    deg = fix(y1);
    #print("deg", deg)
    #print("e", floor(y1)*1.0)
    min = y1 - deg;
    rad_y1 = p*(deg + 5.0*min/3.0)/180.0;

    x2 = loc2[0]
    y2 =loc2[1]
    deg = fix(x2)*1.0;
    min = x2 - deg;
    rad_x2 = p*(deg + 5.0*min/3.0)/180.0;
    
    deg = fix(y2)*1.0;
    min = y2 - deg;
    rad_y2 = p*(deg + 5.0*min/3.0)/180.0;
    RRR = 6378.388;
    q1 = cos( rad_y1 - rad_y2 ); 
    q2 = cos( rad_x1 - rad_x2 ); 
    q3 = cos( rad_x1 + rad_x2 ); 
    dis = (int) ( RRR * acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0);  
    #dis =floor( RRR * acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0);  
    return dis



'''===================================================
    readfile function reads the input file and initiate the adjaceny matrix 
====================================================='''
def readfile(file_name):
    path = "DATA/"+ file_name
    with open(path, 'rt') as input:
        for line in input:
            if "DIMENSION" in line:
                dim = int(line.split(': ')[1])
                #print ("dim", dim)
            if "EDGE_WEIGHT_TYPE" in line:
                #print("line",line)
                temp = line.split(': ')[1]
                if(temp.split('\n')[0]== "EUC_2D"):
                    EUC = 1
                    #print("EUC is true:",EUC)
                else:
                    EUC = 0 
                    #print("EUC",EUC)
            if "NODE_COORD_SECTION" in line:
                break
        location = []
        c  = 0
        for line in input:
            #print(line)
            if "EOF" in line:
                #print("End of file")
                break;
            '''
            if len(line.split(" ")) == 3: 
                [idx, x, y ] = line.split(" ")
                location.append((float(x),float(y)))
            else: 
                [buf,idx, x, y ] = line.split(" ")
                location.append((float(x),float(y)))
            '''
            [idx, x, y ] = line.split()
            location.append((float(x),float(y)))
            c+=1;
        assert(c==dim)
        #for i in range(0,len(location)):
                #print location[i][0];
        #print("location", location)
        adj_matrix = []
        for i in range(dim):
            adj_matrix.append([0 for i in range(dim)])
        for i in range(0,dim):
            for j in range(i+1,dim):
                if(EUC==1):
                    adj_matrix[i][j]=adj_matrix[j][i]= euc_distance(location[i],location[j])
                else:
                    adj_matrix[i][j]=adj_matrix[j][i]= geo_distance(location[i],location[j])
                    #print("1",euc_distance(location[i],location[j]))
                    #print("2",euc_distance(location[j],location[i]))
        #for i in range(0,dim):
            #for j in range(0,dim):
                #euc_distance(location[i],location[j])
                #print("(i,j,adj_matrix)"+ str(i) + "," + str(j) + ": " + str(adj_matrix[i][j]))
        #print("adj_matrix", adj_matrix)
        return dim,adj_matrix 
def dfsPreorder(g,s, count, visited, vertices_visited):
        if s not in vertices_visited:
            vertices_visited.append(s)
            visited[s] = 1 
            count+=1
            #neighbors = [n for n in g.neighbors(s)]
            #print("s",s)
            neighbors = [n for n in g[s]]
            if(len(neighbors)>0):
                for v in neighbors:
                    dfsPreorder(g,v,count, visited, vertices_visited)   
            else:
                return
def write_to_file(tour_list, tour_cost, timestamp_cost,instance, method, cut_off,random_seed):
    #print("instance", instance)
    #print("method", method)
    #print("cut_off", cut_off)
    length = len(instance)-4
    instance = instance[0:length]
    output_file = "output/" + instance+"_" +method+"_"+str(cut_off)+ "_"+str(random_seed)
    if(method == "Approx" or method == "Christofides"):
        sol_output_file = output_file +".sol"
        output_sol = open(sol_output_file, 'wt')
        output_sol.write(str(tour_cost)+"\n")
        output_sol.write(", ".join(map(str,tour_list)))
        trace_output_file = output_file +".trace"
        output_trace = open(trace_output_file, 'wt')
        for x in timestamp_cost:
            t = x[0]           
            c = x[1]           
            output_trace.write("%.10f" % t + ", " + str(c) + "\n")
    else:
        complete_sol_output_file = output_file +"_"+str(random_seed)+".sol"
        output_sol = open(complete_sol_output_file, 'wt')
        output_sol.write(str(tour_cost)+"\n")
        tour_list = [c+1 for c in tour_list]
        output_sol.write(", ".join(map(str,tour_list)))
        

        complete_trace_output_file = output_file +"_"+str(random_seed)+".trace"
        output_trace = open(complete_trace_output_file, 'wt')
        print("timestamp_cost" , len(timestamp_cost))
        for i in range(0, len(timestamp_cost)):
            t = timestamp_cost[i][0]           
            c = timestamp_cost[i][1]           
            output_trace.write("%.10f" % t + ", " + str(c) + "\n")









