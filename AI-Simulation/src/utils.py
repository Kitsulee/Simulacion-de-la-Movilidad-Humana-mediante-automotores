from heapq import heappop, heappush
import sys
sys.path.append('../AI-Simulation')
from extra_classes.graph import *
from math import sqrt

def heuristic(start_point, end_point):
    return sqrt((start_point.x - end_point.x)**2 + (start_point.y - end_point.y)**2)

def aStar(start, goal):
    #The open and closed sets
    openset = set()
    closedset = set()
    
    #Current point is the starting point
    current = start
    
    #Add the starting point to the open set
    openset.add(current)
    
    #While the open set is not empty
    while openset:
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.G + o.H)
        
        #If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent and current.value != start.value:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        
        #Remove the item from the open set
        openset.remove(current)
        
        #Add it to the closed set
        closedset.add(current)
        
        #Loop through the node's children/siblingsmove_cost(
        #for node in children(current,grid):
        for node in current.neighbors:
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score 
                new_g = current.G + current.get_edge(node.value)[1]
                if node.G > new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.get_edge(node.value)[1]
                node.H = heuristic(node, goal)
                
                #Set the parent to our current item
                node.parent = current
                
                #Add it to the set
                openset.add(node)
    #Throw an exception if there is no path
    raise ValueError('No Path Found')

def get_nodes_by_value(start,end,node_list):
    start_node=None
    end_node=None
    for i in node_list:
        if i.value==start:
            start_node=i
        
        if i.value==end:
            end_node=i
    
    return start_node,end_node

    