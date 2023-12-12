def check(arrangement, numbers):
    n_hashtags = 0
    compare_numbers = []
    for i in range(len(arrangement)):
        if arrangement[i] == '#':
            n_hashtags += 1
        elif n_hashtags != 0:
            compare_numbers.append(n_hashtags)
            n_hashtags = 0
        if i == len(arrangement)-1 and n_hashtags != 0:
            compare_numbers.append(n_hashtags)
    return compare_numbers == numbers

def p1(lines):
    output = 0
    for line in lines:
        arrangement, numbers = line.split(' ')
        qm_pos = [i for i in range(len(arrangement)) if arrangement[i] == '?']
        for i in range(2**(len(qm_pos))):
            binary = ['.' if i=='0' else '#' for i in '0'*(len(qm_pos)-len(bin(i))+2)+bin(i)[2:]]
            new_arrangement = ''
            for j in range(len(arrangement)):
                if j in qm_pos:
                    new_arrangement += binary[qm_pos.index(j)]
                else:
                    new_arrangement += arrangement[j]
            if check(new_arrangement, [int(i) for i in numbers.split(',')]):
                output += 1
    print(output)

def p2(lines):
    pass

if __name__ == '__main__':
    lines = open('Day 12/input12.txt').readlines()
    p1(lines)