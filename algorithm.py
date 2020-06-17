#https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
#https://www.geeksforgeeks.org/a-search-algorithm/
import numpy as np
import math

class Node():
    """A node class for A* Search Algorithm"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

def find_coords(_list, val):
    for i, sub_list in enumerate(_list):
        if val in sub_list:
            return i, sub_list.index(val)

def distance(start, end, heuristics='manhattan'):
    x_start = start[0]
    x_end = end[0]
    y_start = start[1]
    y_end = end[1]

    distance = 0

    if heuristics == 'manhattan':
        distance = abs(x_start - x_end) + abs(y_start - y_end)
    elif heuristics == 'euclidean':
        distance = math.sqrt((x_start - x_end)**2 + (y_start - y_end)**2)

    return distance

def a_star(coord_map: list):
    start = find_coords(coord_map, 2)
    end = find_coords(coord_map, 3)

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0 
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        successors = []
        # ONLY FOR MANHATTAN DISTANCE
        successor_positions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for new_position in successor_positions:

            # Get node position
            node_position = (current_node.position[0]+new_position[0], current_node.position[1]+new_position[1])

            # Make sure within range
            if (node_position[0] > (len(coord_map)-1)) or (node_position[0] < 0) or (node_position[1] > (len(coord_map[0])-1)) or (node_position[1] < 0):
                continue

            # Make sure walkable terrain
            if coord_map[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            print(new_node.position)

            # Append
            successors.append(new_node)

        for successor in successors:
            for x in closed_list:
                if successor == x:
                    continue
            
            successor.g = current_node.g + 1
            successor.h = distance(successor.position, end_node.position)
            successor.f = successor.g + successor.h

            for open_node in open_list:
                if successor == open_node and successor.g > open_node.g:
                    continue

            open_list.append(successor)

maze = [
    [0, 0, 0, 0, 2],
    [0, 0, 1, 0, 0],
    [0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

path = a_star(maze)
print(path)