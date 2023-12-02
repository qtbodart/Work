colors = ['blue', 'green', 'red']

def lineChonker(line):
    if(line[-1] == '\n'):
        treated = line[0:-1]
    else:
        treated = line
    treated = treated.split(':')[1][1:]
    return treated

def elNumerator(line):
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
print(elNumerator('Game 2: 6 blue, 3 green; 4 red, 1 green, 7 blue; 2 green'))
