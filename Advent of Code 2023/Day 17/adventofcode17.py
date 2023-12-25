import sys

def parseFile(directory):
    return [line[:-1] if line[-1] == '\n' else line for line in open(directory).readlines()]
input = parseFile('Advent of Code 2023/Day 17/test17.txt')

def get_path(node):
    output = []
    current = node
    while(True):
        try:
            output.append(str(current))
            current = self.previous_nodes[current]
        except:
            break
    print('->'.join(reversed(output)))

def getInt(y,x):
    return int(input[y][x])

def getUnvisitedNodes():
    output = []
    for i in range(len(input)):
        for j in range(len(input[0])):
            output.append((i,j))
    return output

def getNeighbours(node):
    output = []
    for n in [(node[0]-1,node[1]),(node[0],node[1]-1),(node[0]+1,node[1]),(node[0], node[1]+1)]:
        if -1 not in n and n[0] != len(input) and n[1] != len(input[0]):
            output.append(n)
    return output

def get_outgoing_edges(node, previous_nodes, start_node):
    if node != start_node:
        try:
            previous = previous_nodes[node]
            pprevious = previous_nodes[previous]
            ppprevious = previous_nodes[pprevious]
        except KeyError:
            #print('keyerror detected')
            return [n for n in getNeighbours(node) if n != previous]
        else:
            #print(f'ppprevious : {ppprevious}\npprevious : {pprevious}\nprevious : {previous}\ncurrent : {node}')
            if previous == (node[0], node[1]-1) and pprevious == (previous[0], previous[1]-1) and ppprevious == (pprevious[0], pprevious[1]-1):
                #print('three times right in a row')
                return [n for n in getNeighbours(node) if (n != previous and n != (node[0],node[1]+1))]
            elif previous == (node[0], node[1]+1) and pprevious == (previous[0], previous[1]+1) and ppprevious == (pprevious[0], pprevious[1]+1):
                #print('three times left in a row')
                return [n for n in getNeighbours(node) if (n != previous and n != (node[0],node[1]-1))]
            elif previous == (node[0]-1, node[1]) and pprevious == (previous[0]-1, previous[1]) and ppprevious == (pprevious[0]-1, pprevious[1]):
                #print('three times down in a row')
                return [n for n in getNeighbours(node) if (n != previous and n != (node[0]+1,node[1]))]
            elif previous == (node[0]+1, node[1]) and pprevious == (previous[0]+1, previous[1]) and ppprevious == (pprevious[0]+1, pprevious[1]):
                #print('three times up in a row')
                return [n for n in getNeighbours(node) if (n != previous and n != (node[0]-1,node[1]))]
        finally:
            #print('no 3-long straight line detected')
            return [n for n in getNeighbours(node) if n != previous]
    #print('start node')
    return getNeighbours(node)

def dijkstra_algorithm(start_node, end_node):
    unvisited_nodes = getUnvisitedNodes()
    shortest_path = {}
    previous_nodes = {}

    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    shortest_path[start_node] = 0

    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        
        print(f'current : {current_min_node}')
        get_path(current_min_node)
        neighbors = get_outgoing_edges(current_min_node, previous_nodes, start_node)
        print(neighbors)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + getInt(neighbor[0], neighbor[1])
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
                
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path

def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(str(node))
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(str(start_node))

    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))

def part1():
    previous_nodes, shortest_path = dijkstra_algorithm((0,0),(len(input)-1,len(input[0])-1))
    print_result(previous_nodes,shortest_path,(0,0),(len(input)-1,len(input[0])-1))

if __name__ == '__main__':
    part1()