### A Study on Traveling Salesperson Problem

This study evaluates six algorithms for solving metric version of Traveling Salesperson Problem. First, an exact algorithm based on branch-and-bound (BnB) strategy is implemented and evaluated.  Since the exact algorithm is computationally expensive, we also implement three constructive heuristic methods based on Minimum Spanning Tree, Cheapest Insertion, and Christofides. Finally, we implement two algorithms based on stochastic local search strategy including Simulated Annealing and Iterative Local Search. The paper also provides the theoretical and empirical analyses on runtime, solution quality, and relative error of each algorithm. Thes number of nodes in graph is in range of 10 to 250.

<p align = "center">

![Image](https://github.com/rojinnew/tsp_solver/blob/master/image.png)

< /p>

**Requirements**

Python2.7, NumPy-1.15.4, networkx-2.2

**Details**

- The code is developed and tested using python2.7.

- In utils for calculating the distance, fix method from numpy-1.15.4 is used. 

- In Christofides method, max_weight_matching function from networkx-2.2 is used.

#### Overall Structure of code directory

Below, the name of each code, description, related class and local functions and the dependencies are listed.  

(1) exec

- exec file contains the main method and it is a driver program. It's invoked by command prompt and invokes the requested method entered by the user. It also passes  the entered parameters to the chosen algorithm.

- MSTApprox.mstapprox, bnb.bnb, simAnnealing.sa, two_opt.two_opt, cheapest_insertion.ci, Christofides.christofides functions are imported into this file.

(2) utils.py

- This file provide utility functions to all algorithms.

- External library dependencies: NumPy Python library

- Local functions: euc_distance, geo_distance, readfile, dfsPreorder, and write_to_file.

(3) MSTApprox.py 

- Contains the code for solving TSP using mst-approximation. It's invoked by exec file.
 
- mst.unionFind,mst.computeMST, utils.readfile,utils.dfsPreorder are imported from other source code into this file.

- Local functions:  mstapprox. 

(4) mst.py

- Contains Kruskal's method 

- Local functions: computeMST, union , find 

(5) bnb.py 
- Contains the code for solving TSP using mst approximation. It's invoked by exec file. 

- utils.readfile is imported from utils source code.

- bnb has local class and its method including: branch_state class, add_vertex, calculate_lower_bound

- Local functions: bnb

(6) simAnnealing.py 

- Contains the code for solving TSP using simulated annealing.  It's invoked by exec file. 

- utils.readfile is imported from utils source code

- Local functions: sa, initiate_solution, compute_cost, double_bridge


(7) two_opt.py 

- Contains the code for solving TSP using Iterated local search based on 2-opt.  It's invoked by exec file. 

- utils.readfile is imported from utils source code

- Local functions: two_opt, initiate_solution, compute_cost, double_bridge, swap_two_opt


(8) cheapest_insertion.py 

- Contains the code for solving TSP using Cheapest Insertion. It's invoked by exec file.
 
- utils.readfile is imported from utils source code

- Local functions:  compute_cost

(9) Christofides.py 

- Contains the code for solving TSP using Cheapest Insertion. It's invoked by exec file.
 
- utils.readfile, mst.unionFind,mst.computeMST are imported from utils source code

- Graph and max_weight_matching method imported from networkx 

- Local functions: odd_vertices, min_w_matching, and eulerian_tour

#### Instruction for running:

- Change the current directory to code.

- Make sure DATA folder is located in code directory 

- Create a directory called output
 
- General command format :

exec -inst <filename> -alg [BnB | Approx | CI | Christofides | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]

- Assume we plan to set instance to Berlin.tsp, time to 60 and random_seed to 1. 


#### For the competition the best result is from LS2

-To run the iterated local search based on 2-opt algorithm type the following command:

    ./exec -inst Berlin.tsp -alg LS2 -time 60 -seed 1

-To run the branch and bound method, type the following command:

    ./exec -inst Berlin.tsp -alg BnB -time 60 
 
-To run MST-Approximation method, type the following command:

    ./exec -inst Berlin.tsp -alg Approx -time 60 -seed 1 

-To run Cheapest Insertion method, type the following command:

    ./exec -inst Berlin.tsp -alg CI -time 60 -seed 1 

-To run Christofides method, type the following command:

    ./exec -inst Berlin.tsp -alg  Christofides -time 60 -seed 1 

-To run the simulated annealing algorithm type the following command:

    ./exec -inst Berlin.tsp -alg LS1 -time 60 -seed 1

