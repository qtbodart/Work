import sys

class Graph:
    def __init__(self, input):
        self.grid = [[int(c) for c in line if c != '\n'] for line in input]
        self.start_node = (0,0)
        self.end_node = (len(self.grid)-1, len(self.grid[0])-1)
        self.unvisited_nodes = []
        self.shortest_path = {}
        self.previous_nodes = {}
        self.initialize()
    
    def __str__(self):
        path = []
        node = self.end_node
        while node != self.start_node:
            path.append(str(node))
            node = self.previous_nodes[node]
        path.append(str(self.start_node))
        return "We found the following best path with a value of {}.".format(self.shortest_path[self.end_node])+'\n'+" -> ".join(reversed(path))
    
    def set_start_node(self, location):
        self.start_node = (location[0],location[1])
    
    def set_end_node(self, location):
        self.end_node = (location[0],location[1])

    def reset_unvisited_nodes(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.unvisited_nodes.append((i,j))
    
    def reset_shortest_path(self,start_node):
        for node in self.unvisited_nodes:
            self.shortest_path[node] = sys.maxsize
        self.shortest_path[start_node] = 0

    def initialize(self):
        self.reset_unvisited_nodes()
        self.reset_shortest_path(self.start_node)
    
    def getNeighbours(self, node):
        output = []
        for n in [(node[0]-1,node[1]),(node[0],node[1]-1),(node[0]+1,node[1]),(node[0], node[1]+1)]:
            if -1 not in n and n[0] != len(self.grid) and n[1] != len(self.grid[0]):
                output.append(n)
        return output
    
    def get_outgoing_edges(self, current_min_node):
        if current_min_node != self.start_node:
            try:
                previous = self.previous_nodes[current_min_node]
                pprevious = self.previous_nodes[previous]
                ppprevious = self.previous_nodes[pprevious]
            except KeyError:
                #print('keyerror detected')
                return [n for n in self.getNeighbours(current_min_node) if n != previous]
            else:
                #print(f'ppprevious : {ppprevious}\npprevious : {pprevious}\nprevious : {previous}\ncurrent : {node}')
                if previous == (current_min_node[0], current_min_node[1]-1) and pprevious == (previous[0], previous[1]-1) and ppprevious == (pprevious[0], pprevious[1]-1):
                    #print('three times right in a row')
                    return [n for n in self.getNeighbours(current_min_node) if (n != previous and n != (current_min_node[0],current_min_node[1]+1))]
                elif previous == (current_min_node[0], current_min_node[1]+1) and pprevious == (previous[0], previous[1]+1) and ppprevious == (pprevious[0], pprevious[1]+1):
                    #print('three times left in a row')
                    return [n for n in self.getNeighbours(current_min_node) if (n != previous and n != (current_min_node[0],current_min_node[1]-1))]
                elif previous == (current_min_node[0]-1, current_min_node[1]) and pprevious == (previous[0]-1, previous[1]) and ppprevious == (pprevious[0]-1, pprevious[1]):
                    #print('three times down in a row')
                    return [n for n in self.getNeighbours(current_min_node) if (n != previous and n != (current_min_node[0]+1,current_min_node[1]))]
                elif previous == (current_min_node[0]+1, current_min_node[1]) and pprevious == (previous[0]+1, previous[1]) and ppprevious == (pprevious[0]+1, pprevious[1]):
                    #print('three times up in a row')
                    return [n for n in self.getNeighbours(current_min_node) if (n != previous and n != (current_min_node[0]-1,current_min_node[1]))]
            finally:
                #print('no 3-long straight line detected')
                return [n for n in self.getNeighbours(current_min_node) if n != previous]
        #print('start node')
        return self.getNeighbours(current_min_node)

    def weird_dijkstra(self):
        while(self.unvisited_nodes):
            current_min_node = None
            for node in self.unvisited_nodes: # Iterate over the nodes
                if current_min_node == None:
                    current_min_node = node
                elif self.shortest_path[node] < self.shortest_path[current_min_node]:
                    current_min_node = node
            print(f'current : {current_min_node}')
            self.get_path(current_min_node)
            neighbors = self.get_outgoing_edges(current_min_node)
            print(neighbors)
            print()
            for neighbor in neighbors:
                tentative_value = self.shortest_path[current_min_node] + self.grid[neighbor[0]][neighbor[1]]
                if tentative_value < self.shortest_path[neighbor]:
                    self.shortest_path[neighbor] = tentative_value
                    # We also update the best path to the current node
                    self.previous_nodes[neighbor] = current_min_node
                    
            self.unvisited_nodes.remove(current_min_node)
    
    def get_path(self,node):
        output = []
        current = node
        while(True):
            try:
                output.append(str(current))
                current = self.previous_nodes[current]
            except:
                break
        print('->'.join(reversed(output)))

if __name__ == '__main__':
    lines = open('Advent of Code 2023\Day 17\\test17.txt').readlines()
    graph1 = Graph(lines)
    graph1.weird_dijkstra()
    print(graph1)