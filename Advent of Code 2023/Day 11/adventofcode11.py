'''
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
'''

import copy
from collections import Counter

def augmentator(im):
    nw_im = copy.deepcopy(im)
    h_upgrade = []
    v_upgrade = []
    
    for i in range(len(im)):
        if '#' not in im[i]:
            h_upgrade.append(i)
            
    j = 0
    for col in zip(*im):
        if '#' not in col:
            v_upgrade.append(j)
        j += 1
    
    h_lines = '.'*len(im[0])
    for i in range(len(h_upgrade)-1,-1 , -1):
        nw_im.insert(h_upgrade[i],h_lines)
        
    for i in range(len(v_upgrade)-1,-1 , -1):
        for j in range(len(nw_im)):
            nw_im[j] = nw_im[j][:v_upgrade[i]]+'.'+nw_im[j][v_upgrade[i]:]
            
    return nw_im

def get_galaxiator(im):
    pos = []
    for i in range(len(im)):
        for j in range(len(im[i])):
            if im[i][j] == '#':
                pos.append((i,j))
    return pos

def get_chemator(pos):
    chem = 0
    for i in range(len(pos)):
        for j in range(i+1, len(pos)):
            chem += abs(pos[i][0]-pos[j][0]) + abs(pos[i][1]-pos[j][1])
    return chem

def remplacator(im):
    nw_im = copy.deepcopy(im)
    h_upgrade = []
    v_upgrade = []
    
    for i in range(len(im)):
        if '#' not in im[i]:
            h_upgrade.append(i)
            
    j = 0
    for col in zip(*im):
        if '#' not in col:
            v_upgrade.append(j)
        j += 1
    
    h_lines = '+'*len(im[0])
    for i in range(len(h_upgrade)-1,-1 , -1):
        nw_im[h_upgrade[i]] = h_lines
        
    for i in range(len(v_upgrade)-1,-1 , -1):
        for j in range(len(nw_im)):
            nw_im[j] = nw_im[j][:v_upgrade[i]]+'+'+nw_im[j][v_upgrade[i]+1:]
            
    return nw_im

def get_chemator2(im,pos,facteur=10):
    chem = 0
    for i in range(len(pos)):
        for j in range(i+1, len(pos)):
            if pos[i][1] <= pos[j][1]:
                h_count = Counter(im[pos[i][0]][pos[i][1]:pos[j][1]+1])
            else:
                h_count = Counter(im[pos[i][0]][pos[j][1]:pos[i][1]+1])
            v_count = Counter([im[k][pos[i][1]] for k in range(pos[i][0],pos[j][0]+1)])
            
            chem += h_count['.'] + h_count['+']*facteur + (h_count['#']-1) 
            chem += v_count['.'] + v_count['+']*facteur + (v_count['#']-1)

    return chem

if __name__ == '__main__':
    lines = open('Day 11/input11.txt', 'r').readlines()
    # lines = open('test.txt', 'r').readlines()
    lines = [line.strip() for line in lines]
    #print(lines)
    image = augmentator(lines)
    #print(image)
    gal = get_galaxiator(image)
    #print(gal)
    res = get_chemator(gal)
    print(res)
    image2 = remplacator(lines)
    # print(image2)
    gal2 = get_galaxiator(image2)