import math

#converts the graph data in text file to a suitable format
def graphConv(file):

    file1 = open(file, 'r')
    Lines = file1.readlines()
    index = 1
    nodeDict = dict()

    #index of source node is 0 
    nodeDict['s'] = 0

    #temporarily set the index of sink node as a very high integer value
    nodeDict['t'] = math.inf

    #read line by line and assign each node a unique index
    for line in Lines:
        list = line.split()
        if list[0] not in  nodeDict.keys():
            nodeDict[list[0]] = index
            index += 1
        if list[1] not in nodeDict.keys():
            nodeDict[list[1]] = index
            index += 1

    #assign sink node the last index
    nodeDict['t'] = index

    #initialise a 2-D array with all 0 values
    graph = [[0 for i in range(index+1)] for j in range(index+1)]

    #read the file again, replace the 0 values with the capacity of the edges
    for line in Lines:
        list = line.split()
        index1 = nodeDict[list[0]]
        index2 = nodeDict[list[1]]
        graph[index1][index2] = int(list[2])

    #return the graph
    return graph

#finds the largest power of two which is no larger than the value of n 
def largestPowerofTwo(n):
 
    i = 0

    while 2 ** i <= n:
        i += 1
    
    return i 

#finds and returns the maximum capacity of all edgess
def setMax(graph,numberofNodes):
    
    maximumCapacity = -math.inf
    for i in range(numberofNodes):
        for j in range(numberofNodes):
            if graph[i][j] > maximumCapacity:
                maximumCapacity = graph[i][j]
    
    return maximumCapacity



#Ford Fulkerson Helper Function - implements a standard DFS traversal with modifications
#to accomodate for the delta condition
def scalingfordFulkersonHelperDFS(graph, nodes, s, t, parent,delta):

    #source node is the first node to be visited
    stack = []
    stack.append(s)

    
    #intially all nodes are not visited
    visited = [False for i in range(nodes)]

    visited[s] = True

    #BFS Traversal 
    while len(stack) > 0 :
        
        #Dequeue
        currNode = stack.pop()


        #explore all the neighbours of currentNode
        for i in range(len(graph[currNode])):
            tempCapacity = graph[currNode][i]
            #unvisited adjacent nodes are only visited if the capacity on the edge is >= delta value
            if not(visited[i]) and tempCapacity >= delta:
                stack.append(i)
                visited[i] = True
                parent[i] = currNode
                #return when the BFS traversal reaches the sink node
                if i == t:
                    return True

    #sink is unreachable from source
    return False


#Ford Fulkerson Helper Function - implements a standard BFS traversal with modifications
#to accomodate for the delta condition
def scalingfordFulkersonHelper(graph, nodes, s, t, parent, delta):

    #source node is the first node to be visited
    queue = []
    queue.append(s)

    
    #intially all nodes are not visited
    visited = [False for i in range(nodes)]

    visited[s] = True

    #BFS Traversal 
    while len(queue) > 0 :
        
        #Dequeue
        currNode = queue.pop(0)


        #explore all the neighbours of currentNode
        for i in range(len(graph[currNode])):
            tempCapacity = graph[currNode][i]
            #unvisited adjacent nodes are only visited if the capacity on the edge is >= delta value
            if not(visited[i]) and tempCapacity >= delta:
                queue.append(i)
                visited[i] = True
                parent[i] = currNode
                #return when the BFS traversal reaches the sink node
                if i == t:
                    return True

    #sink is unreachable from source
    return False
             
     

#Main Function - returns the maximum Flow
def scalingFordFulkerson(graph,nodes,maximumCapacity,source, sink):

    #parent array stores the path 
    parent = [-1 for i in range(nodes)]

    #initial flow is zero
    maxFlow = 0 

    #initial delta is the largest power of 2 that is no larger than maximum capacity 
    delta = largestPowerofTwo(maximumCapacity)


    while delta > 0 :
        #if there is a s-t path, then augment the flow
        while scalingfordFulkersonHelper(graph,nodes,source, sink, parent,delta) :

            pathFlow = math.inf

            current = sink

            #find the bottleneck along the path 
            while(current !=  source):
                pathFlow = min (pathFlow, graph[parent[current]][current])
                current = parent[current]


            # Add the bottleneck value to the maxFlow
            maxFlow +=  pathFlow

            currentNode = sink
            #update the flow on forward and backward edges
            while(currentNode !=  source):

                prevNode = parent[currentNode]

                #increment the flow on the forward edges
                graph[currentNode][prevNode] += pathFlow

                #decrement the flow on the backward edges
                graph[prevNode][currentNode] -= pathFlow

                currentNode = parent[currentNode]

        #update the delta value till it reaches 0 
        delta = delta // 2

    return maxFlow



