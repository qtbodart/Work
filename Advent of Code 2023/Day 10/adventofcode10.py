left = {'F':'down','-':'left','L':'up'}
right = {'7':'down','-':'right','J':'up'}
up = {'7':'left','|':'up','F':'right'}
down = {'J':'left','|':'down','L':'right'}
directions = [left,right,up,down]

def findS(lines):
    for i in range(len(lines)):
        if 'S' in lines[i]:
            return (i,lines[i].index('S'))
    return

def findConnecting(lines,line,index):
    output = []
    if index != 0 and lines[line][index-1] in left.keys():
        output.append(0)
    if index != len(lines[line])-1 and lines[line][index+1] in right.keys():
        output.append(1)
    if line != 0 and lines[line-1][index] in up.keys():
        output.append(2)
        

def toArray(lines):
    line, index = findS(lines)


if __name__ == '__main__':
    lines = open('Day 10/input10.txt').readlines()
    toArray(lines)