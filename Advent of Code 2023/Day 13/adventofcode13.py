from functools import cache

def getColumn(pattern, index):
    arr = [line[index] for line in pattern]
    output = ''
    for c in arr:
        output += c
    return output

def numberOfDiff(str1, str2):
    return sum(1 for c1,c2 in zip(str1, str2) if c1 != c2)

def findHorizontal(pattern):
    for i in range(len(pattern)-1):
        j = i+1
        loc = j
        symetric = True
        while(i != -1 and j != len(pattern)):
            if pattern[i] != pattern[j]:
                symetric = False
                break
            i += -1
            j += 1
        if symetric == True:
            return loc
    return 0

def findHorizontalSmudge(pattern):
    for i in range(len(pattern)-1):
        j = i+1
        loc = j
        smudged = False
        symetric = True
        while(i != -1 and j != len(pattern)):
            if pattern[i] != pattern[j]:
                if smudged == False and numberOfDiff(pattern[i], pattern[j]) == 1:
                    smudged = True
                else:
                    symetric = False
                    break
            i += -1
            j += 1
        if smudged == False and symetric:
            continue
        if symetric:
            return loc
    return 0

def findVertical(pattern):
    for i in range(len(pattern[0])-1):
        j = i+1
        loc = j
        symetric = True
        while (i != -1 and j != len(pattern[0])):
            if getColumn(pattern,i) != getColumn(pattern,j):
                symetric = False
                break
            i -= 1
            j += 1
        if symetric == True:
            return loc
    return 0

def findVerticalSmudge(pattern):
    for i in range(len(pattern[0])-1):
        j = i+1
        loc = j
        smudged = False
        symetric = True
        while (i != -1 and j != len(pattern[0])):
            if getColumn(pattern,i) != getColumn(pattern,j):
                if smudged == False and numberOfDiff(getColumn(pattern,i), getColumn(pattern,j)) == 1:
                    smudged = True
                else:
                    symetric = False
                    break
            i -= 1
            j += 1
        if smudged == False and symetric:
            continue
        if symetric == True:
            return loc
    return 0

def getPattern(lines, n):
    output = []
    count = 0
    for i in range(len(lines)):
        if count > n:
            break
        if lines[i] == '\n':
            count += 1
            continue
        elif count == n:
            output.append(lines[i][:-1])
    return output

def part1(lines):
    sum = 0
    for i in range(lines.count('\n')+1):
        pattern = getPattern(lines, i)
        columns_left = findVertical(pattern)
        rows_above = findHorizontal(pattern)
        sum += columns_left + 100*rows_above
    print(sum)

def part2(lines):
    sum = 0
    for i in range(lines.count('\n')+1):
        pattern = getPattern(lines, i)
        columns_left = findVerticalSmudge(pattern)
        rows_above = findHorizontalSmudge(pattern)
        sum += columns_left + 100*rows_above
    print(sum)

if __name__ == '__main__':
    lines = open('Day 13/input13.txt').readlines()
    part1(lines)
    part2(lines)