import itertools as it
from functools import cache

def getColumn(lines, index):
    return ''.join([line[index] for line in lines])

def getLine(lines, index):
    return lines[index] if lines[index][-1] != '\n' else lines[index][:-1]

def getGrid(lines):
    return [line if line[-1]!='\n' else line[:-1] for line in lines]

def getRolledNorth(column):
    round = [i for i in range(len(column)) if column[i] == 'O']
    for round_index in round:
        while(round_index != 0 and column[round_index-1] == '.'):
            column = swap(column, round_index, round_index-1)
            round_index -= 1
    return column

def rotate(grid):
    output = []
    for i in range(len(grid[0])):
        column = ''
        for j in range(len(grid)):
            column += grid[j][i]
        output.append(column)
    return output


def getGridRolled(grid, direction):
    newgrid = []
    if direction == 'N':
        for i in range(len(grid[0])):
            newgrid.append(getRolledNorth(getColumn(grid,i)))
        newgrid = rotate(newgrid)
    if direction == 'S':
        for i in range(len(grid[0])):
            newgrid.append(getRolledSouth(getColumn(grid,i)))
        newgrid = rotate(newgrid)
    if direction == 'W':
        for i in range(len(grid)):
            newgrid.append(getRolledWest(getLine(grid,i)))
    if direction == 'E':
        for i in range(len(grid)):
            newgrid.append(getRolledEast(getLine(grid,i)))
    return newgrid
    

def getRolledSouth(column):
    round = [i for i in range(len(column)) if column[i] == 'O']
    for i in range(len(round)-1,-1,-1):
        round_index = round[i]
        while(round_index != len(column)-1 and column[round_index+1] == '.'):
            column = swap(column, round_index, round_index+1)
            round_index += 1
    return column

def getRolledWest(line):
    round = [i for i in range(len(line)) if line[i] == 'O']
    for round_index in round:
        while(round_index != 0 and line[round_index-1] == '.'):
            line = swap(line, round_index, round_index-1)
            round_index -= 1
    return line

def getRolledEast(line):
    round = [i for i in range(len(line)) if line[i] == 'O']
    for i in range(len(round)-1,-1,-1):
        round_index = round[i]
        while(round_index != len(line)-1 and line[round_index+1] == '.'):
            line = swap(line, round_index, round_index+1)
            round_index += 1
    return line
    
def swap(str1,i1,i2):
    l = list(str1)
    l[i1], l[i2] = l[i2], l[i1]
    return ''.join(l)

def calculateColumnLoad(lines,index):
    sum = 0
    column = getRolledNorth(getColumn(lines, index))
    round = [i for i in range(len(column)) if column[i] == 'O']
    for round_index in round:
        sum += len(column)-round_index
    return sum

def countzeros(str1):
    return sum(1 for character in str1 if character == 'O')

def calculateLoad(lines):
    output = 0
    for i in range(len(lines)):
        output += countzeros(lines[i])*(len(lines)-i)
    return output

def part1(lines):
    output = 0
    for i in range(len(lines[0])-1):
        output += calculateColumnLoad(lines,i)
    print(output)


@cache
def cycle(lines):
    grid = [line for line in lines]
    grid = getGridRolled(grid,'N')
    grid = getGridRolled(grid,'W')
    grid = getGridRolled(grid,'S')
    grid = getGridRolled(grid,'E')
    return tuple(grid)

def part2(lines):
    grid = tuple(getGrid(lines))
    for i in it.count(1):
        if(i%1000000 == 0):
            print(f'number of cycles done: {int(i/1000000)}*10^6')
        grid = cycle(grid)
        if i == 1000000000:
            break
    print(calculateLoad(grid))

if __name__ == '__main__':
    lines = open('Day 14/input14.txt').readlines()
    part1(lines)
    part2(lines)