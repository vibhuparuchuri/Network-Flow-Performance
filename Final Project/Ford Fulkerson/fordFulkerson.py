import math
import sys
import time


def graphConv(file):
    file1 = open(file, 'r')
    Lines = file1.readlines()
    index = 1
    nodeDict = dict()
    nodeDict['s'] = 0
    nodeDict['t'] = math.inf
    for line in Lines:
        list = line.split()
        if list[0] not in  nodeDict.keys():
            nodeDict[list[0]] = index
            index += 1
        if list[1] not in nodeDict.keys():
            nodeDict[list[1]] = index
            index += 1
    nodeDict['t'] = index
    graph = [[0 for i in range(index+1)] for j in range(index+1)]

    for line in Lines:
        list = line.split()
        index1 = nodeDict[list[0]]
        index2 = nodeDict[list[1]]
        graph[index1][index2] = int(list[2])

    return graph


def searchDFS(graph,source,sink,path):
        #searches for valid path from s to t, returns
        #go from vertex to vertex to search for path
    row = len(graph) 
    checked = (row)*[False] #bool value of each vertex visited status
    vertex_list=[]
    vertex_list.append(source)
    checked[source] = True #source node is visited
     #loop to traverse through vertices finding adjacent vertices until sink is reached
    while vertex_list:
        first = vertex_list.pop() #one element in list - the current vertex being considered
        for i,j in enumerate(graph[first]):
         #here i is every vertex and the edge value from first to every vertex is j 
            if checked[i] == False and j > 0:
                vertex_list.append(i)
                checked[i] = True
                path[i] = first
                if i == sink:
                    return True
                    
    return False


def search(graph,source,sink,path):
        #searches for valid path from s to t, returns
        #go from vertex to vertex to search for path
    row = len(graph) 
    checked = (row)*[False] #bool value of each vertex visited status
    vertex_list=[]
    vertex_list.append(source)
    checked[source] = True #source node is visited
     #loop to traverse through vertices finding adjacent vertices until sink is reached
    while vertex_list:
        first = vertex_list.pop(0) #one element in list - the current vertex being considered
        for i,j in enumerate(graph[first]):
         #here i is every vertex and the edge value from first to every vertex is j 
            if checked[i] == False and j > 0:
                vertex_list.append(i)
                checked[i] = True
                path[i] = first
                if i == sink:
                    return True
                    
    return False
    
def FF(graph,source,sink):
        row = len(graph)
        path = (row)*[-1] 
        #path stores path to vertex and is sent to search function
        max_flow = 0
        #we calculate max flow only when path exists from source to sink
        while search(graph,source, sink, path):
            temp_flow = sys.maxsize #to be used for comparison
            stemp = sink
            while stemp!=source:
                temp_flow = min (temp_flow, graph[path[stemp]][stemp])
                stemp = path[stemp]
                
            max_flow = max_flow + temp_flow
            
            stemp2 = sink
            #updating residual capacities along the edges of the graph
            while(stemp2 !=  source):
                temp = path[stemp2]
                graph[temp][stemp2] -= temp_flow
                graph[stemp2][temp] += temp_flow
                stemp2 = path[stemp2]
        return max_flow


def getallvariables(graph_temp):
    source = 0
    sink = len(graph_temp) - 1
    start_time = time.process_time()
    val = FF(graph_temp,source, sink)
    print("Max-Flow: ",val)
    time_exec = time.process_time() - start_time
    return time_exec


fileName = str(input("Enter the filename: "))

graph_temp = graphConv(fileName)
print("Run-time: " + str(getallvariables(graph_temp)))


'''graph_temp = graphConv('r-c-100.txt')
print("Run-time: " + str(getallvariables(graph_temp)))

graph_temp = graphConv('r-c-200.txt')
print("Run-time: " + str(getallvariables(graph_temp)))

graph_temp = graphConv('r-c-300.txt')
print("Run-time: " + str(getallvariables(graph_temp)))

graph_temp = graphConv('r-c-400.txt')
print("Run-time: " + str(getallvariables(graph_temp)))

graph_temp = graphConv('r-c-500.txt')
print("Run-time: " + str(getallvariables(graph_temp)))'''