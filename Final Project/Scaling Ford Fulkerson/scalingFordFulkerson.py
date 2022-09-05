import time
from scalingFordFulkersonHelp import *


#takes the file name of the input graph .txt file    
stringFile = str(input("Enter the filename: "))

#pass the file to the graphConv() to convert
#text file into a adjacency matrix 
graph = graphConv(stringFile)


#intialise maxCapacity and nodes
maxCapacity = -math.inf
nodes = len(graph)


#find the maximum capacity of all edges
maxCapacity = setMax(graph,nodes)


#set the source
source = 0

#set the sink
sink = len(graph) -1 


#run the ford fulkerson algorithm on the input graph
snapshot1 = time.process_time()
maxFlow = scalingFordFulkerson(graph,nodes,maxCapacity,source,sink)
snapshot2 = time.process_time()
print("Maximum flow: " + str(maxFlow))
print("Time taken: " + str(snapshot2-snapshot1))
