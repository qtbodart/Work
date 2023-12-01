def numberGiver(line):
    numbers = ''
    for character in line:
        if character in ['0','1','2','3','4','5','6','7','8','9']:
            numbers += character
    return numbers

def elNumerator(line):
    written_numbers = ['zero','one','two','three','four','five','six','seven','eight','nine']
    for number in written_numbers:
        line = line.replace(number, number+str(written_numbers.index(number))+number)
    return line


sum = 0
bettersum = 0
with open('/home/qbodart/Git/Work/Advent of Code 2023/Day 1/text1_1.txt') as f:
    lines = f.readlines()
    for phrase in lines:
        numbers = numberGiver(phrase)
        betternumbers = numberGiver(elNumerator(phrase))
        sum += int(numbers[0]+numbers[-1])
        bettersum += int(betternumbers[0]+betternumbers[-1])
print(sum)
print(bettersum)