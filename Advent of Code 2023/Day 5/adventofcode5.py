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

if __name__ == '__main__':
    lines = open('Day 5/input5.txt').readlines()
    print(tableConvertor(lines))