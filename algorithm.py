#https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
#https://www.geeksforgeeks.org/a-search-algorithm/
import numpy as np
import math
import time
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
        comparison = self.position == other
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

def get_neighbours(node, coordMap):
    mapSize = coordMap.shape
    x, y = node.position
    positions = np.array([(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)])
    filter = (positions[:, 0] >= 0) & (positions[:, 0] < mapSize[0]) & (positions[:, 1] >= 0) & (positions[:, 1] < mapSize[1])
    positions = positions[filter]
    positions = positions[coordMap[positions[:, 0], positions[:, 1]] != 1]
    return positions


def a_star(coord_map):
    coord_map = np.asarray(coord_map)
    # find point where coord_map == 2 (start point)
    start = np.argwhere(coord_map == 2).reshape(2)
    # find point where coord_map == 3 (end point)
    end = np.argwhere(coord_map == 3).reshape(2)

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0 

    open_list = PriorityQueue()
    closed_list = []

    open_list.put(start_node)

    while not open_list.empty():

        current_node = open_list.get()
        closed_list.append(current_node)

        if current_node == end:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return np.asarray(path[::-1]) # Return reversed path

        successor_positions = get_neighbours(current_node, coord_map)
        for pos in successor_positions:
            tentativeGScore = current_node.g + 1

            openVisited = False
            for i, openNode in enumerate(open_list.queue):
                if openNode == pos:
                    if openNode.g <= tentativeGScore:
                        openVisited = True
                        break
                    else:
                        open_list.pop(i)
                        break
            if openVisited:
                continue

            closedVisited = False
            for i, closedNode in enumerate(closed_list):
                if closedNode == pos:
                    if closedNode.g <= tentativeGScore:
                        closedVisited = True
                        break
                    else:
                        closed_list.pop(i)
                        break
            if closedVisited:
                continue

            newNode = Node(parent=current_node, position=pos)
            newNode.g = tentativeGScore
            newNode.h = int(cdist(pos.reshape(1, -1), end.reshape(1, -1), metric='cityblock'))
            newNode.f = newNode.g + newNode.h

            open_list.put(newNode)

if __name__ == "__main__":
    maze = [
        [0, 0, 1, 0, 3, 0],
		[0, 0, 0, 1, 0, 0],
		[1, 1, 0, 1, 1, 0],
		[2, 0, 0, 0, 0, 0],
    ]

    path = None
    start = time.time()
    # for i in range(1000):
    path = a_star(maze)
    elapsed = time.time() - start
    print("solution:", path)
    print("time elapsed:", elapsed)
