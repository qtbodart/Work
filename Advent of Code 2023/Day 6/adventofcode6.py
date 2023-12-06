def tuplizator(lines):
    output = []

    for i in range(int(len(lines)/2)):
        line_output = []
        treated_time = [int(value) for value in lines[2*i].split(':')[1].strip(' ').split(' ') if value != '']
        treated_dist = [int(value) for value in  lines[2*i+1].split(':')[1].strip(' ').split(' ') if value != '']
        for j in range(len(treated_time)):
            line_output.append((treated_time[j], treated_dist[j]))
        output.append(line_output)
    return output

def bettahTuplizator(lines):
    output = []

    for i in range(int(len(lines)/2)):
        line_output = []
        treated_time = [int(value) for value in lines[2*i].split(':')[1].strip(' ').split(' ') if value != '']
        treated_dist = [int(value) for value in  lines[2*i+1].split(':')[1].strip(' ').split(' ') if value != '']
        treated_time_comb = ''
        treated_dist_comb = ''
        for j in range(len(treated_time)):
            treated_time_comb += str(treated_time[j])
            treated_dist_comb += str(treated_dist[j])
        output.append((int(treated_time_comb), int(treated_dist_comb)))
    return output

def multiplor(line):
    mult = 1
    for time, dist in line:
        n_wow = 0
        for hold in range(1, time):
            if hold*(time-hold) > dist : n_wow+=1
        mult *= n_wow
    return mult

def bettahMultiplor(line):
    time, dist = line[0]

    min_win = 0
    max_win = time

    while(min_win*(time-min_win) <= dist):
        min_win+=1

    while(max_win*(time-max_win) <= dist):
        max_win-=1
    
    return (max_win-min_win+1)

if __name__ == '__main__':
    lines = open('Day 6/input6.txt').readlines()
    print(multiplor(tuplizator(lines)[0]))
    print(bettahMultiplor(bettahTuplizator(lines)))