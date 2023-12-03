def elIndexator(line):
    '''
    Outputs an array of indexes and values of numbers in the line, (index, 'number')
    '''
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    output = []
    current = ''
    for i in range(len(line)):
        if line[i] in numbers:
            current += line[i]
        elif current != '':
            output.append((i-len(current), current))
            current = ''
    return output

def elSymbolisator(line):
    '''
    outputs an array of the indexes of the symbols in the line
    '''
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    output = []
    for i in range(len(line)):
        if line[i] not in ['.', '\n'] and line[i] not in numbers:
            output.append(i)
    return output

def elStarSymbolisator(line):
    output = []
    for i in range(len(line)):
        if line[i] == '*':
            output.append(i)
    return output

def elSimpleSommator(lines):
    sum = 0
    for i in range(len(lines)):
        previous = ''
        current = ''
        next = ''

        current = lines[i]
        if i != 0:
            previous = lines[i-1]
        if i != len(lines)-1:
            next = lines[i+1]
        
        for index, number in elIndexator(current):
            for j in range(index-1,index+len(number)+1):
                if j in elSymbolisator(previous) or j in elSymbolisator(next) or j in elSymbolisator(current):
                    sum += int(number)
                    break
    return(sum)

def elMuchoBettahSommator(lines):
    sum = 0
    for i in range(len(lines)):
        previous = ''
        current = ''
        next = ''

        current = lines[i]
        if i != 0:
            previous = lines[i-1]
        if i != len(lines)-1:
            next = lines[i+1]

        star_indexes = elStarSymbolisator(current)
        dic_star_indexes = {}
        for index in star_indexes:
            dic_star_indexes[index] = []
        
        indexators = [elIndexator(previous), elIndexator(current), elIndexator(next)]

        for indexator in indexators:
            for index, number in indexator:
                for possible_index in dic_star_indexes.keys():
                    if possible_index in range(index-1, index+len(number)+1):
                        dic_star_indexes[possible_index].append(number)
        
        for key in dic_star_indexes.keys():
            if len(dic_star_indexes[key]) == 2:
                sum += int(dic_star_indexes[key][0])*int(dic_star_indexes[key][1])
    
    return sum

if __name__ == '__main__':
    with open('/home/qbodart/Git/Work/Advent of Code 2023/Day 3/input.txt') as f:
        lines = f.readlines()
        print(elSimpleSommator(lines))
        print(elMuchoBettahSommator(lines))