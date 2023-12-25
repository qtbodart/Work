def elDictator(instructions):
    output = {0:{0:'000000'}}
    cp = [0,0]
    for instruction in instructions:
        d, n, c = instruction.split(' ')
        n = int(n)
        c = c[2:-1]
        match d:
            case 'R':
                for j in range(cp[1]+1,cp[1]+n+1):
                    if cp[0] in output.keys():
                        output[cp[0]][j] = c
                    else:
                        output[cp[0]] = {j:c}
                cp[1] += n
            case 'L':
                for j in range(cp[1]-n,cp[1]):
                    if cp[0] in output.keys(): 
                        output[cp[0]][j] = c
                    else:
                        output[cp[0]] = {j:c}
                cp[1] -= n
            case 'D':
                for j in range(cp[0]+1,cp[0]+n+1):
                    if j in output.keys():
                        output[j][cp[1]] = c
                    else:
                        output[j] = {cp[1]:c}
                cp[0] += n
            case 'U':
                for j in range(cp[0]-n,cp[0]):
                    if j in output.keys():
                        output[j][cp[1]] = c
                    else:
                        output[j] = {cp[1]:c}
                cp[0] -= n
    return output

def visualise(instructions):
    dic = elDictator(instructions)
    min = 0
    max = 0
    min_line = 0
    max_line = 0
    for key in dic.keys():
        if min_line > key:
            min_line = key
        if max_line < key:
            max_line = key
        for index in dic[key].keys():
            if min > index:
                min = index
            if max < index:
                max = index
    print(f'{min_line} {max_line} {min} {max}')
    output = [(max-min+1)*'.' for _ in range(max_line-min_line+1)]

    for key in dic.keys():
        for index in dic[key].keys():
            output[key] = strReplace(output[key],index-min,'#')

    for line in output:
        print(line)


def parseFile(lines):
    return [line if line[-1] != '\n' else line[:-1] for line in lines]

def strReplace(string, index, c):
    return ''.join(string[i] if i != index else c for i in range(len(string)))

def calcVolume(sortedIndexes):
    output = 0
    cur = 0
    counts = True
    while(cur<len(sortedIndexes)):
        if (cur+1 == len(sortedIndexes)):
            break
        if (sortedIndexes[cur+1] == sortedIndexes[cur]+1):
            output += 1
            cur += 1
            continue
        if counts:
            output += sortedIndexes[cur+1]-sortedIndexes[cur]+1
            cur += 1
            counts = False
            continue
        if not counts:
            counts = True
            cur += 1
    return output

def calcLagoonVolume(instructions):
    output = 0
    dic = elDictator(instructions)
    for key in dic.keys():
        print(f'calculated volume for line {key} ({sorted(dic[key].keys())}) : {calcVolume(sorted(dic[key].keys()))}')
        output += calcVolume(sorted(dic[key].keys()))
    return output

def part1(instructions):
    print(calcLagoonVolume(instructions))

if __name__ == '__main__':
    instructions = parseFile(open('Advent of Code 2023/Day 18/input18.txt').readlines())
    #part1(instructions)
    visualise(instructions)