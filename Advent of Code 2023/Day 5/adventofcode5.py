numbers = ['0','1','2','3','4','5','6','7','8','9']

def seedisator(lines):
    treated = lines[0].split(':')[1].split(' ')
    return [int(seed) for seed in treated if seed != '']

def maxOfSeeds(lines):
    max = 0
    seeds = seedisator(lines)
    for i in range(int(len(seeds)/2)):
        pot_max = seeds[2*i]+seeds[2*i+1]
        if max < pot_max:
            max = pot_max
    return max


def tableConvertor(lines):
    matrix = []
    table = []
    for line in lines:
        if line[0] not in numbers:
            if line == '\n':
                matrix.append(table)
                table = []
            continue
        table.append([int(number) for number in line.split(' ')])
    return matrix

def destinationConvertor(matrix, seed):
    current_value = seed
    print(f'\nseed considered : {seed}\n-------------\n ')
    for table in matrix:
        for line in table:
            if (line[1]<=current_value & current_value<line[1]+line[2]):
                current_value = current_value+(line[0]-line[1])
                break
    return current_value

def elGrandeExecutor(lines):
    seeds = seedisator(lines)
    destinations = []
    matrix = tableConvertor(lines)

    for seed in seeds:
        destination = destinationConvertor(matrix,seed)
        destinations.append(destination)
    
    return findNearest(destinations)

def findNearest(destinations):
    nearest = destinations[0]
    for dest in destinations:
        if dest<nearest:
            nearest = dest
    return nearest

if __name__ == '__main__':
    lines = open('Day 5/input5.txt').readlines()
    print(elGrandeExecutor(lines))