numbers = ['0','1','2','3','4','5','6','7','8','9']
lines = open('Day 5/test.txt').readlines()

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

interval = [([0,maxOfSeeds(lines)*10],0)]

def intervalModifier(fr, to, modifier):
    current_interval = interval
    for i in range(len(interval)):
        rng, cur_modifier = interval[i]
        fr_int, to_int = rng
        if fr_int < fr and to < to_int:
            current_interval.remove(([fr_int,to_int], cur_modifier))
            current_interval.append(([fr_int,fr-1], cur_modifier))
            current_interval.append(([to, to_int-1], cur_modifier))
            current_interval.append(([fr,to-1], cur_modifier+modifier))
            continue
        if fr_int >= fr and to > fr_int and to < to_int:
            current_interval.remove(([fr_int,to_int], cur_modifier))
            current_interval.append(([fr_int, to-1], cur_modifier+modifier))
            current_interval.append(([to, to_int-1], cur_modifier))
            continue
        if fr_int < fr and fr < to_int and to_int <= to:
            current_interval.remove(([fr_int,to_int], cur_modifier))
            current_interval.append(([fr_int,fr-1], cur_modifier))
            current_interval.append(([fr, to_int], cur_modifier+modifier))
            continue
        elif (fr<fr_int & to<fr_int) or (to_int<fr & to_int<to):
            continue
        interval = current_interval

if __name__ == '__main__':
    table = tableConvertor(lines)
    for function in table:
        for line in function:
            print(f'line : {line}\ninterval : {interval}\nmodifying interval from {line[1]} to {line[1]+line[2]} by {line[0]-line[1]}')
            intervalModifier(line[1], line[1]+line[2], line[0]-line[1])
            print(f'interval after modification : {interval}\n')
    print(interval)