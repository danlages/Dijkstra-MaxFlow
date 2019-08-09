
infinity = 1000000
invalid_node = - 1

class Node: #Defines a node in the network
    previous = invalid_node
    distFromSource = infinity
    visited = False

def populateNetwork(fileName): #Populates list with network nodes taking name of file as parameter
    network = [] #Defines the list to be populated by network
    networkFile = open(fileName, "r") #Opens file for reading
    for line in networkFile: #Iterate through file
        network.append(map(int,line.strip().split(','))) #Add newtwork to the list - removing commas seperating each number
    return network #Return list containing network

def defineRoute(routeFile): #Reads a text file in order to define start and end nodes when finding the shortest path
    routeFound = []
    routeFile = open(routeFile, "r") #Open route file for reading
    for char in routeFile.readline().strip('\r\n').split('>'): #Iterates through the letters using the split function to remove the '>' character
        routeFound.append(ord(char)-65) #The ord() function converts the nodes from letters to numbers and appends to list for initialisation - providing the reverse effect of chr()
    #Set nodes to the required values in the list
    startNode = routeFound[0]
    endNode = routeFound[1]
    return startNode, endNode #return start and end nodes

def populateNodeTable(network, startNode):
    nodeTable = [] #Define list to be populated by nodes (positions in the the network)
    for node in network:
        nodeTable.append(Node()) #Append node object to nodeTable
    nodeTable[startNode].distFromSource = 0 #Set distance from source as 0
    nodeTable[startNode].visited = True #Set visited to true
    return nodeTable

def nearestNeighbours(currentNode, nodeTable, network):
    neighbours = []  #To hold the neighbours of the current node that are accessable by the current node
    for nodeIndex, value in enumerate(network[currentNode]): #Looks through the nodes on the same line as the current node - possible nodes that can be accessed
        #Look at the corresponding node in nodeTable to check if it is visited and there is a connection
        if nodeTable[nodeIndex].visited == False and value != 0: #If 0 there will be no connection to the node and the route cannot be taken
            neighbours.append(nodeIndex) #Append node to neighbours list
    return neighbours

def calculateTentative(currentNode, network, nodeTable): #Calculates the distances of the neighbours from the current node
    neighboursFound = nearestNeighbours(currentNode, nodeTable, network) #The neighbours are the nodes that will be used to calculate distance as they are accessable by the current node
    for nodeIndex in neighboursFound:
        tentativeDist = nodeTable[currentNode].distFromSource + network[currentNode][nodeIndex] #Update the distance based upon the distance from each node taken
        if tentativeDist < nodeTable[nodeIndex].distFromSource: #Set distance from source to the tentative if a shorter path - This will ensure that the nodes with the least distance are chosen first when returning the next node
            nodeTable[nodeIndex].distFromSource = tentativeDist #Set the distance to the distance accumulated so far and the distance value of the node
            nodeTable[nodeIndex].previous = currentNode #The previous node is set as current node - ready for the next node to be analysed
    return nodeTable #Alter the node table accordingly

def returnNextNode(nodeTable): #Return the next node out of possible nodes if it has the least distance
    currentNode = invalid_node #Current node cannot be set as the next node
    distance = infinity
    for nodeIndex, value in enumerate(nodeTable): #Iterate through the nodeTable
        if value.distFromSource < distance and value.visited == False: #Check if the current distance total is less than the distance variable, ensuring an optimal path is taken when choosing the next node
            currentNode = nodeIndex  #Update the current node if the conditions are met
            distance = value.distFromSource #Distance is updated for each new node
    return currentNode

def calculateShortestPath(nodeTable, currentNode, network, endNode):
    path = []
    while currentNode != endNode: #Explore all nodes
        calculateTentative(currentNode, network, nodeTable) #calculateTentative is called to alter the nodeTable with the corrisponding distances
        node = returnNextNode(nodeTable) #Visit the next node
        if node == currentNode: #If all options have been explored and the optimum path is found
            return path
        else:
            currentNode = node #Final path not found - iterate through remaining nodes
            nodeTable[currentNode].visited = True #Set node to visted - it has been analysed and cannot be visited again
    path.append(endNode) #Append end node to path for printing
    while currentNode != startNode: #Insert list to path - for displaying
        path.insert(0,nodeTable[currentNode].previous)
        currentNode = path[0]
    return path

def maxflow(path, nodeTable, network, currentNode, endNode):
    maximumFlow = 0 #Maxflow varibales used to define the total max flow
    while path != []:
        capacity = findFlowCapacity(path, network, currentNode, endNode) #Find the bottleneck for the path taken
        maximumFlow += capacity #Max flow is the total of the individual path capacities
        network = alterNetwork(path, capacity, network) #Alter network based upon the bottlenecks found within each path
        nodeTable = populateNodeTable(network, startNode) #Re-populate node table with the adjusted nodes and capacities - in order to calculate the shortest path again
        printPath(path) #print path
        print "- Path Capacity:",capacity #Print path bottleneck
        path = calculateShortestPath(nodeTable, currentNode, network, endNode) #New path is calculated as the adjustment of the network may result in nodes being fully utilised
    return maximumFlow #return the Maximum Flow

def findFlowCapacity(path, network, currentNode, endNode): #Find the bottleneck in a given path
    pathCapacity = infinity
    length = len(path)
    for nodeIndex, value in enumerate(path): #Iterate through all nodes within shortest path found
        if nodeIndex < (length-1): #Examine each node in path
            if network[value][path[nodeIndex + 1]] < pathCapacity:
                pathCapacity = network[value][path[nodeIndex + 1]] #Update the path bottleneck if the new node allows for a lower capacity - Effecting the flow to that point in the path
    return pathCapacity #Bottleneck found

def alterNetwork(path, capacity, network):
    length = len(path)
    for nodeIndex, value in enumerate(path):
        if nodeIndex < (length-1):
            #Adjust the individual node capacities accordingly on both x and y axis
            network[value][path[nodeIndex + 1]] -= capacity #Ford-Fulkerson
            network[path[nodeIndex + 1]][value] += capacity
            #The capacities set when adjusting the path adhere to the bottleneck of each path, and will be added up to achive the total maximum flow
    return network #Return altered Network

def printPath(path): #Function for printing the path
    for node in path:
        print chr(node + 65), #Print as ascii values using chr(+ 65)

if __name__ == '__main__':

    startNode, endNode = defineRoute("route.txt") #Set start and end nodes to the corrisponding nodes within the route specification

    path = []
    currentNode = startNode
    network = populateNetwork("network.txt") #Populate network with that provided in the network file
    nodeTable = populateNodeTable(network, startNode) #Populate the node table with the network
    calculateTentative(currentNode, network, nodeTable)
    path = calculateShortestPath(nodeTable, currentNode, network, endNode) #Define the shortest path - Djikstra's algorithm

    #Print desired Output
    print "Shortest Path:"
    printPath(path)
    print "- Distance:", nodeTable[endNode].distFromSource
    print "Max Flow:"
    maxFlow = maxflow(path, nodeTable, network, currentNode, endNode) #Perform Max Flow

    print "Final Max Flow:", maxFlow
