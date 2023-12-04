def removeSpaces(array):
    return [value for value in array if value not in [' ', '']]

def getNumber(line):
    return int(removeSpaces(line.split(':')[0].split(' '))[1])

def DiePuntizator(line):
    treated = line.split(':')[1][1:]
    winnings = removeSpaces(treated.split('|')[0].split(' '))
    actuals = removeSpaces(treated.split('|')[1][:-1].split(' '))

    sum = 0
    for winning in winnings:
        for actual in actuals:
            if winning == actual:
                sum += 1
    
    if sum == 0:
        return sum
    else:
        return 2**(sum-1)

def DieNumerizator(line):
    treated = line.split(':')[1][1:]
    winnings = removeSpaces(treated.split('|')[0].split(' '))
    actuals = removeSpaces(treated.split('|')[1][:-1].split(' '))

    sum = 0
    for winning in winnings:
        for actual in actuals:
            if winning == actual:
                sum += 1
    return sum

def LaaargePuntizator(lines):
    sum = 0
    for line in lines:
        sum += DiePuntizator(line)
    print(sum)

def bettahLaaargePuntizator(lines):
    scratchcards = [1]*len(lines)
    for line in lines:
        index = getNumber(line)-1
        winners = DieNumerizator(line)

        for i in range(index+1,index+winners+1):
            scratchcards[i] += scratchcards[index]
    
    sum = 0
    for number in scratchcards:
        sum += number
    
    print(sum)

if __name__ == '__main__':
    lines = open('/home/qbodart/Git/Work/Advent of Code 2023/Day 4/input4.txt').readlines()
    LaaargePuntizator(lines)
    bettahLaaargePuntizator(lines)