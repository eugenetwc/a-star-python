#https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
#https://www.geeksforgeeks.org/a-search-algorithm/
import numpy as np
import math
from scipy.spatial.distance import cdist
from queue import PriorityQueue

class Node():
    """A node class for A* Search Algorithm"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        # self.position is an np.ndarray
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        # check if two numpy arrays are equal
        comparison = self.position == other.position
        equal_arrays = comparison.all()
        return equal_arrays
    
    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"
    
    # defining less than for purposes of priority queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of priority queue
    def __gt__(self, other):
        return self.f > other.f

    def __hash__(self):
        return hash(self.position)

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

def a_star(coord_map):
    coord_map = np.asarray(coord_map)
    # find point where coord_map == 2 (start point)
    start = np.argwhere(coord_map == 2).reshape(2)
    # find point where coord_map == 3 (end point)
    end = np.argwhere(coord_map == 3).reshape(2)

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0 
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = PriorityQueue()
    closed_list = []

    open_list.put(start_node)

    while not open_list.empty():

        current_node = open_list.get()
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return np.asarray(path[::-1]) # Return reversed path

        # ONLY FOR MANHATTAN DISTANCE
        successors = []
        successor_positions = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])
        for new_position in successor_positions:

            # Get node position
            node_position = current_node.position + new_position

            # Make sure within range
            if (node_position[0] >= coord_map.shape[0]) or (node_position[0] < 0) or (node_position[1] >= coord_map.shape[1]) or (node_position[1] < 0):
                continue

            # Make sure walkable terrain
            if coord_map[node_position[0], node_position[1]] == 1:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            successors.append(new_node)


        for successor in successors:
            if successor in closed_list:
                continue
            
            successor_current_cost = current_node.g + 1
            # cityblock == manhattan distance
            if (successor_current_cost < successor.g) or (successor not in open_list.queue):
                successor.g = successor_current_cost
                successor.h = cdist(successor.position.reshape([1, 2]), end_node.position.reshape([1, 2]), 'cityblock').item()
                successor.f = successor.g + successor.h

                if successor not in open_list.queue:
                    open_list.put(successor)


if __name__ == "__main__":
    maze = [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 2],
        [0, 3, 1, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    path = a_star(maze)
    print(path)