def FDP_inator(lines):
    cut = list(map(int, lines[0].split(":")[1].strip().split()))
    
    seeds = []
    for i in range(0, len(cut), 2):
        seeds.append([cut[i], cut[i] + cut[i + 1]])

    popator = seeds

    for lin in lines[1:]:
        modifier = []
        
        for line in lin.split("\n")[1::]:
            modifier.append(list(map(int, line.split())))

        impact = []

        while(popator):
            frst, lst = popator.pop()
            for src,fin,mod in modifier:
                mx = max(frst, fin)
                mn = min(lst, fin+mod)
                if mx<mn:
                    impact.append([mx+(src-fin), mn+(src-fin)])
                    if mx > frst:
                        popator.append([frst, mx])
                    if lst > mn:
                        popator.append([mn, lst])
                    break
            else:
                impact.append([frst, lst])

        res = min(impact)[0]
        popator = impact
    
    return res

if __name__ == "__main__":
    file = open('Day 5/input5.txt', 'r')
    #file = open('test.txt', 'r')
    liness = file.read().split("\n\n")
    print(FDP_inator(liness))