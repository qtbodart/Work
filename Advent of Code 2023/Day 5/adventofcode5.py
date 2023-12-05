numbers = ['0','1','2','3','4','5','6','7','8','9']

def seedisator(lines):
    treated = lines[0].split(':')[1].split(' ')
    return [int(seed) for seed in treated if seed != '']

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
                print(f'line : {line}\nvalue found to be between {line[1]} and {line[1]+line[2]}\nold value : {current_value}  ')
                current_value = current_value+(line[0]-line[1])
                print(f'new value : {current_value}\n')
                break
    return current_value

def elGrandeExecutor(lines):
    seeds = seedisator(lines)
    destinations = []
    matrix = tableConvertor(lines)

    for seed in seeds:
        destination = destinationConvertor(matrix,seed)
        destinations.append(destination)
    
    return destinations

        

if __name__ == '__main__':
    lines = open('Day 5/test.txt').readlines()
    print(elGrandeExecutor(lines))