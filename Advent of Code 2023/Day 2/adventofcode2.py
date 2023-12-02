colors = ['red', 'green', 'blue']

def lineChonker(line):
    """strips line from the end '\\n' character and the 'Game #' at the beginning of each line"""
    if(line[-1] == '\n'):
        treated = line[0:-1]
    else:
        treated = line
    treated = treated.split(':')[1][1:]
    return treated

def elNumerator(line):
    """converts input line into the max occuring number of each color : red, green and blue"""
    line = lineChonker(line)
    output = [0, 0, 0]

    subsets = line.split(';')
    for subset in subsets:
        sub_colors = subset.split(',')
        for sub_color in sub_colors:
            info = sub_color.strip().split(' ')
            num = int(info[0])
            col = info[1]
            min = output[colors.index(col)]
            if min < num:
                output[colors.index(col)] = num
    return output

def gameNumberReader(line):
    return int(line.split(':')[0].split(' ')[1])


sum = 0
with open('/home/qbodart/Git/Work/Advent of Code 2023/Day 2/input2.txt') as f:
    lines = f.readlines()
    for line in lines:
        feasable = True
        max = elNumerator(line)
        print(max)
        for i in range(3):
            if max[i] >= 13+i:
                feasable = False
                print('Bad')
        if feasable == True:
            sum += gameNumberReader(line)
            print('Good')
    print(sum)
