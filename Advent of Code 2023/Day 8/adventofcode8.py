import numpy as np
nodes = {}
start = []

def dictisator(lines):
    '''
    writes the input @lines into the dict @nodes in the form of 'node' : ('left','right')
    '''
    for i in range(2, len(lines)):
        node = lines[i][0:3]
        left, right = lines[i][7:10], lines[i][12:15]
        nodes[node] = (left, right)

def instructor(lines):
    current = 'AAA'
    last = 'ZZZ'
    instructions = lines[0][:-1]
    it = 0
    while(current != last):
        for instruction in instructions:
            left, right = nodes[current]
            if instruction == 'L':
                current = left
            elif instruction == 'R':
                current = right
            it += 1
            if current == last:
                break
    
    return it

def execInstructionStarts(instruction):
    for i in range(len(start)):
        if start[i][0][2] != 'Z':
            if instruction == 'L':
                start[i] = (nodes[start[i][0]][0], start[i][1]+1)
            else:
                start[i] = (nodes[start[i][0]][1], start[i][1]+1)

def verifyEnd():
    for c,_ in start:
        if c[2] != 'Z':
            return False
    return True

def bettahInstructor(lines):
    instructions = lines[0][:-1]
    while(verifyEnd() == False):
        for instruction in instructions:
            execInstructionStarts(instruction)
            if verifyEnd():
                break

def starts():
    for key in nodes.keys():
        if key[2] == 'A':
            start.append((key,0))

def ppcm():
    numbers = [value[1] for value in start]
    return np.lcm.reduce(numbers)

if __name__ == '__main__':
    lines = open('Day 8/input8.txt').readlines()
    dictisator(lines)
    starts()
    print(instructor(lines))
    bettahInstructor(lines)
    print(ppcm())