def findGalaxies(lines):
    output = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '#':
                output.append((i,j))
    return output

def findEmptyColumns(galaxies,max):
    output = []
    for i in range(max-1):
        found = False
        for _,index in galaxies:
            if i == index:
                found = True
                break
        if not found:
            output.append(i)
    return output

def findEmptyLines(galaxies,lines_length):
    output = []
    for i in range(lines_length):
        found = False
        for index,_ in galaxies:
            if i == index:
                found = True
                break
        if not found:
            output.append(i)
    return output

def expand(galaxies, expNum, max, lines_length):
    empty_columns = findEmptyColumns(galaxies, max)
    for j in range(len(empty_columns)-1,-1,-1):
        empty_column = empty_columns[j]
        for i in range(len(galaxies)):
            line, column = galaxies[i]
            if column > empty_column:
                galaxies[i] = (line, column+expNum)
    
    empty_lines = findEmptyLines(galaxies, lines_length)
    for j in range(len(empty_lines)-1,-1,-1):
        empty_line = empty_lines[j]
        for i in range(len(galaxies)):
            line, column = galaxies[i]
            if line > empty_line:
                galaxies[i] = (line+expNum,column)
    return galaxies

def abs(value):
    if value < 0:
        return -value
    return value

def calculateDistance(expGal):
    sum = 0
    for i in range(len(expGal)):
        for j in range(i,len(expGal)):
            sum += abs(expGal[i][0]-expGal[j][0])+abs(expGal[i][1]-expGal[j][1])
    return sum


if __name__ == '__main__':
    lines = open('Day 11/test11.txt').readlines()
    max = len(lines[0])
    lines_length = len(lines)

    galaxies = findGalaxies(lines)
    #print(galaxies)
    #print(expand(galaxies,1,max,lines_length))
    print(calculateDistance(expand(galaxies,1000000,max,lines_length)))
