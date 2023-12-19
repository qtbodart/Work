import sys
sys.setrecursionlimit(10000)


def parseFile(lines):
    return [line[:-1] if line[-1] == '\n' else line for line in lines]
grid = parseFile(open('Advent of Code 2023/Day 16/input16.txt').readlines())
output = {}
dir_visited = {}

def reinitialize():
    output.clear()
    dir_visited.clear()

def nextDir(dir,c):
    if dir == 'right':
        if c == '/':
            return ['up']
        elif c == '\\':
            return ['down']
        elif c == '|':
            return ['up', 'down']
        else:
            return ['right']
    
    if dir == 'left':
        if c == '/':
            return ['down']
        elif c == '\\':
            return ['up']
        elif c == '|':
            return ['up', 'down']
        else:
            return ['left']
    
    if dir == 'up':
        if c == '/':
            return ['right']
        elif c == '\\':
            return ['left']
        elif c == '-':
            return ['left', 'right']
        else:
            return ['up']
    
    if dir == 'down':
        if c == '/':
            return ['left']
        elif c == '\\':
            return ['right']
        elif c == '-':
            return ['left', 'right']
        else:
            return ['down']

def getNextCP(direction, cp):
    if direction == 'left':
        return [cp[0],cp[1]-1]
    if direction == 'right':
        return [cp[0],cp[1]+1]
    if direction == 'up':
        return [cp[0]-1,cp[1]]
    if direction == 'down':
        return [cp[0]+1,cp[1]]

def part1():
    reinitialize()
    energize('right', [0,0])
    print(len(output))

def energize(direction,cp):
    if (cp[0] != -1 and cp[0] != len(grid)) and (cp[1] != -1 and cp[1] != len(grid[0])):
        if tuple(cp) not in dir_visited.keys() or direction not in dir_visited[tuple(cp)]:
            if tuple(cp) not in dir_visited.keys():
                dir_visited[tuple(cp)] = [direction]
            else:
                dir_visited[tuple(cp)].append(direction)
            #print(f'current direction : {direction}\ncurrent position : {(cp[0], cp[1])}\n character in grid : {grid[cp[0]][cp[1]]}\n')
            output[tuple(cp)] = '#'
            for dire in nextDir(direction,grid[cp[0]][cp[1]]):
                ncp = getNextCP(dire,cp)
                #print(f'current position : {cp}\ncurrent direction : {direction}\ncurrent character : {grid[cp[0]][cp[1]]}\nnext direction and position : {dire}, {ncp}\n')
                energize(dire,ncp)

def toGraph(dic):
    output = [['.']*len(grid[0]) for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i,j) in dic.keys():
                output[i][j] = '#'
    for line in output:
        print(line)

def part2():
    max = 0
    for i in range(len(grid)):
        reinitialize()
        energize('down',[0,i])
        if len(output) > max:
            max = len(output)
        reinitialize()
        energize('up',[len(grid)-1,i])
        if len(output) > max:
            max = len(output)
    for j in range(len(grid[0])):
        reinitialize()
        energize('right',[j,0])
        if len(output) > max:
            max = len(output)
        reinitialize()
        energize('left',[j,len(grid[0])-1])
        if len(output) > max:
            max = len(output)
    print(max)
        

if __name__ == '__main__':
    part1()
    part2()