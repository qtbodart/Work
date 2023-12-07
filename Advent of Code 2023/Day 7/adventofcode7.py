import functools as ft
list = []

def add_to_list(lines):
    for line in lines:
        hand, bid = line.split(' ')
        list.append((str(recogniseStrength(hand))+hand, int(bid)))

def jokerAdd_to_list(lines):
    for line in lines:
        hand, bid = line.split(' ')
        list.append((str(jokerRecogniseStrength(hand))+hand, int(bid)))

def handAndBid(line):
    hand, bid = line.split(' ')
    return (hand, bid)

def recogniseStrength(hand):
    cards = {}
    binds = [0,0,0,0,0]
    for character in hand:
        if character in cards.keys():
            cards[character] += 1
        else:
            cards[character] = 1
    for _,num in cards.items():
        binds[num-1] += 1
    return (binds[1]*1+binds[2]*3+binds[3]*5+binds[4]*6)

def jokerRecogniseStrength(hand):
    cards_wo_J = ['2','3','4','5','6','7','8','9','T','Q','K','A']
    if 'J' not in hand:
        return recogniseStrength(hand)
    cards = {}
    for character in hand:
        if character in cards.keys():
            cards[character] += 1
        else:
            cards[character] = 1
    J_num = cards['J']
    new_strength = 0
    for char in cards_wo_J:
        pot_strength = recogniseStrength(hand.replace('J',char))
        if pot_strength > new_strength:
            new_strength = pot_strength
    return new_strength

def compare(s_hand1, s_hand2):
    cards = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    if s_hand1[0][0] != s_hand2[0][0]:
        return int(s_hand1[0][0])-int(s_hand2[0][0])
    else:
        for i in range(1,6):
            if s_hand1[0][i] != s_hand2[0][i]:
                return cards.index(s_hand1[0][i])-cards.index(s_hand2[0][i])
        return 0

def jokerCompare(s_hand1, s_hand2):
    cards = ['J','2','3','4','5','6','7','8','9','T','Q','K','A']
    if s_hand1[0][0] != s_hand2[0][0]:
        return int(s_hand1[0][0])-int(s_hand2[0][0])
    else:
        for i in range(1,6):
            if s_hand1[0][i] != s_hand2[0][i]:
                return cards.index(s_hand1[0][i])-cards.index(s_hand2[0][i])
        return 0

def sortList():
    return sorted(list, key=ft.cmp_to_key(compare))

def jokerSortList():
    return sorted(list, key=ft.cmp_to_key(jokerCompare))

def calculateWinnings(list):
    winnings = 0
    for i in range(len(list)):
        winnings += (i+1)*list[i][1]
    return winnings

if __name__ == '__main__':
    lines = open('Day 7/input7.txt').readlines()
    add_to_list(lines)
    list_wo_J = sortList()
    print(calculateWinnings(list_wo_J))
    
    list = []
    jokerAdd_to_list(lines)
    list_w_J = jokerSortList()
    print(calculateWinnings(list_w_J))

    