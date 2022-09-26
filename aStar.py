from Map import *
def manhattan_distance(startposition, endposition):
    """
    Calculates the manhattan-distance between two nodes whose position is given as parameters
    Parameters
    ---------- 
    startposition : list[int]
        Startposition for manhattan-distance calculation

    endposition : list[int]
        Endposition for manhattan-distance calculation

    Returns
    ----------

    """
    return abs(startposition[0] - endposition[0]) + abs(startposition[1] - endposition[1])

class Node:
    def __init__(self, map_obj:Map_Obj, pos:list[int]):
        """
        Instantiate a Node object with position given as parameter

        Parameters
        ---------- 
        pos : list[int]
            Position of given node
        """
        self.parent = None
        self.pos = pos
        self.g = 0
        self.h = manhattan_distance(self.pos, map_obj.get_goal_pos())

    def get_f(self):
        """
        Getter for the given node's f-value, defined as g-value + h-value
        """
        return self.g + self.h
    
    def get_h(self):
        """
        Getter for the given node's h-value
        """
        return self.h
    
    def get_g(self):
        """
        Getter for the given node's g-value
        """
        return self.g


def aStarAlgorithm(task):
    """
    Function that implements the A-star algorithm for given task
    Parameters
    ---------- 
    task : int
        Number of task we are currently solving

    Returns
    ----------
    bool :
        True if goal is found and False if goal is nt found
    """
    map = Map_Obj(task)
    openList = []
    closedList = []

    def findNeigbors(node:Node):
        """
        Finds the neighbouring nodes of node given as parameter

        Parameters
        ----------
        node : Node
            Node that we want to find the neighbours of

        Returns
        ----------
         neighbors : list[Node]
            List of the valid neighbors adjacent to the node, aka. the nodes that are inside of the path and not the wall
        """
        validDirections = [(-1, 0),(1, 0), (0, -1), (0, 1)]
        neighbors = []

        for y, x in validDirections:
            neighborPos = [node.pos[0] + y, node.pos[1] + x]

            neighborValue = map.get_cell_value(neighborPos)
            
            #If neighborValue is less than one, it is a wall and this node is then skipped
            if neighborValue < 0:
                continue

            neighborNode = Node(map, neighborPos)
            neighborNode.parent = node
            neighborNode.g = node.g + map.get_cell_value(neighborNode.pos)
            neighbors.append(neighborNode)
        
        return neighbors

    def isGoal(node:Node):
        """
        Function that checks if the node given as parameter is the goal-node

        Parameters
        ----------
        node : Node
            Node that we want to check if is the goal-node

        Returns
        ----------
        bool : True if node is goal-node, false if not
        """
        return node.pos == map.get_goal_pos()

    def alreadyDiscoveredNode(node:Node, existingList):
        """
        Function that checks if node given as first parameter is a part of the list given as the second parameter

        Parameters
        ----------
        node : Node
            Node that we want to check if is inside of list

        existingList : list[Node]

        Returns
        ----------
        bool : True if node is a part of the list, False if not
        """
        for exisitingNode in existingList:
            if node.pos == exisitingNode.pos:
                return True
        return False

    startNode = Node(map, map.get_start_pos())
    openList.append(startNode)

    while len(openList) > 0:
        
        #Sorting the list of open nodes based on their f-value
        openList.sort(key = lambda node: node.get_f())
        currentNode = openList.pop(0)
        closedList.append(currentNode)

        #If currentnode is goal, trace back the path through parent-nodes and use function of map-class to color the path.
        if isGoal(currentNode): 
            parentNode = currentNode.parent
            while parentNode is not None and parentNode is not startNode:
                map.replace_map_values(parentNode.pos, 0, map.get_goal_pos())
                parentNode = parentNode.parent
                
            map.show_map()
            print("Goal found")
        
        neighbors = findNeigbors(currentNode)
        
        for neighbor in neighbors:
            
            #Checking if neighbor-node is already in openlist or closedlist, before appending to openlist if not discovered
            if not alreadyDiscoveredNode(neighbor, openList) and not alreadyDiscoveredNode(neighbor, closedList):
                openList.append(neighbor)

            #If node is already discovered, check if the cost is lower via new parent. Replace old node in openList with new node if True.
            else:
                for openNode in openList:
                    if openNode.pos == neighbor.pos:
                        if openNode.get_f() > neighbor.get_f():
                            openList.remove(openNode)
                            openList.append(neighbor)
    
    
    #If goal-node is never found, return False
    print("Did not find goal")
    return False

aStarAlgorithm(1)

        
        


