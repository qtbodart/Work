from numpy import *
def zerizator(line):
    output = [[int(value) for value in line.split(' ')]]
    while(output[-1] != len(output[-1])*[0]):
        output.append([output[-1][i+1]-output[-1][i] for i in range(len(output[-1])-1)])
    return output

def extrapolator(triangle):
    value = 0
    for i in range(len(triangle)-2,-1,-1):
        value += triangle[i][-1]
        triangle[i].append(value)
    return triangle[0][-1]

def extraSummator(lines):
    sum = 0
    for line in lines:
        sum += extrapolator(zerizator(line))
    print(sum)

def backwardsExtrapolator(triangle):
    value = 0
    for i in range(len(triangle)-2,-1,-1):
        value = triangle[i][0]-value
        triangle[i].insert(0,value)
    return triangle[0][0]

def backwardsSummator(lines):
    sum = 0
    for line in lines:
        sum += backwardsExtrapolator(zerizator(line))
    print(sum)

if __name__ == '__main__':
    lines = open('Day 9/input9.txt').readlines()
    extraSummator(lines)
    backwardsSummator(lines)
