'''===================================================
*author: Rojin Aliehyaei
*description: Kruskal's Algorithm
*Georgia Institute of Technology, Fall 2018
====================================================='''
import time
import sys

'''===================================================
union-find data structure based on rank and path compression
====================================================='''
class unionFind:
    def __init__(self,g,dim):
        #self.n = g.number_of_nodes()
        self.n = dim 
        #self.vertices = list(g.nodes())
        self.vertices = range(0,dim)
        self.roots = {} 
        self.rank = {}
        for i in self.vertices:
            self.roots[i]= i 
            self.rank[i]= 0 

    def find(self,v):
        root = v 
        # find the root of component
        while (root != self.roots[root]):
            root = self.roots[root]
        # Compress the paths 
        while (root != v):
            next = self.roots[v]
            self.roots[v] = root
            v = next
        return root

    def union(self,v1, v2):
        root1 = self.find(v1)
        root2 =self.find(v2)
        if(self.rank[root1] < self.rank[root2]):
            self.roots[root1] = root2
        elif(self.rank[root1] > self.rank[root2]):
            self.roots[root2] = root1
        else:
            self.roots[root2] = root1
            self.rank[root1] = self.rank[root1] + 1

'''===================================================
computeMST function returns the MST tree and its cost 
it is based on Kruskal's algorithm
====================================================='''
def computeMST(g, edge_list,dim):
    T = [] 
    edge_list.sort(key=lambda t: t[2])
    uf = unionFind(g,dim)
    MST_cost = 0
    for e in edge_list:
        s, d, w = e[0],e[1],e[2]
        if (uf.find(s) != uf.find(d)):
            uf.union(s,d)
            T.append(e)
            MST_cost = MST_cost + w 
    #print("MST_cost", MST_cost)
    return MST_cost,T 

