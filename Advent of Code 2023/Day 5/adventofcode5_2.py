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

