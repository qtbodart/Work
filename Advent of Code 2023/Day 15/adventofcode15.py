def Hash(str1):
    current = 0
    for i in range(len(str1)):
        for c in str1[i]:
            current = ((current+ord(c))*17)%256
    return current

def HashLine(line):
    res = 0
    for str1 in line:
        res += Hash(str1)
    return res

def parseFile(lines):
    return lines[0].split(',')

def part1(lines):
    list_of_str = parseFile(lines)
    print(HashLine(list_of_str))

def instToDict(line):
    res = {}
    for str1 in line:
        if '=' in str1:
            auth, focal_len = str1.split('=')
            box = Hash(auth)
            if box not in res.keys():
                res[box] = [(auth, focal_len)]
                continue
            else:
                replaced = False
                for i,list_lenses in enumerate(res[box]):
                    if list_lenses[0] == auth:
                        res[box][i] = (auth, focal_len)
                        replaced = True
                if not replaced:
                    res[box].append((auth,focal_len))
        
        elif '-' in str1:
            auth =  str1[:-1]
            box = Hash(auth)
            if box in res.keys():
                for i,list_lenses in enumerate(res[box]):
                    if list_lenses[0] == auth:
                        res[box].pop(i)
    
    return res
        
def sumOfFocusPowah(box_dict):
    res = 0
    for i in box_dict.keys():
        if box_dict[i] != []:
            for index,list_lenses in enumerate(box_dict[i]):
                res += (i+1)*(index+1)*int(list_lenses[1])
    return res

def part2(lines):
    print(sumOfFocusPowah(instToDict(parseFile(lines))))

if __name__ == '__main__':
    lines = open('Day 15/input15.txt').readlines()
    part1(lines)
    part2(lines)