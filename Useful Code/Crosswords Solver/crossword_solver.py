table = []
words = []
output = []

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def parseTable():
    with open(__file__[:-19]+"crosswords.txt","r") as f:
        wordsBegun = False
        for line in f.readlines():
            if(line == "\n"):
                wordsBegun = True
                continue
            
            if not wordsBegun:
                table.append(line[:-1] if "\n" in line else line)
            else:
                words.append(line[:-1] if "\n" in line else line)

def getVertical():
    verticals = []
    for i in range(len(table[0])):
        vertical = ""
        for j in range(len(table)):
            vertical += table[j][i]
        verticals.append(vertical)
    return verticals

def getDiagonal():
    diagonals = [""]*(len(table) + len(table[0])-1)
    for i, line in enumerate(table):
        for j, c in enumerate(line):
            diagonals[j-i+len(table)-1] += c
    return diagonals

def getAntiDiagonal():
    antidiagonals = [""]*(len(table) + len(table[0])-1)
    for i, line in enumerate(table):
        for j, c in enumerate(line):
            antidiagonals[i+j] += c
    return antidiagonals

def findWords(orientation):
    cur_table = []
    match orientation:
        case "horizontal":
            cur_table = table
        case "vertical":
            cur_table = getVertical()
        case "diagonal":
            cur_table = getDiagonal()
        case "antidiagonal":
            cur_table = getAntiDiagonal()
    
    n = 0
    for n_line, line in enumerate(cur_table):
        for word in words:
            if word in line :
                output.append((str(orientation), n_line , line.index(word), word, False if orientation=="antidiagonal" else True))
                n+=1
            if word in line[::-1]:
                output.append((str(orientation), n_line, len(line)-line[::-1].index(word)-len(word), word, True if orientation=="antidiagonal" else False))
                n+=1
    print(f"{orientation} : {n}")

def findAllWords():
    findWords("horizontal")
    findWords("vertical")
    findWords("diagonal")
    findWords("antidiagonal")
    
def printOutput():
    cur_color = ""
    for orientation, n, index, word, upright in output:
        print(f"{color.BOLD}{word}{color.END} : (à l'{"endroit" if upright else "envers"})")
        boldedLetters = []
        match orientation:
            case "horizontal":
                cur_color = color.RED if upright else color.YELLOW
                for i in range(index , index+len(word)):
                    boldedLetters.append((n,i))
                pass
            case "vertical":
                cur_color = color.GREEN if upright else color.BLUE
                for i in range(index, index+len(word)):
                    boldedLetters.append((i,n))
                pass
            case "diagonal":
                cur_color = color.CYAN
                if n < len(table):
                    for i in range(index, index+len(word)):
                        boldedLetters.append((len(table)-n+i-1, i))
                else:
                    for i in range(index, index+len(word)):
                        boldedLetters.append((i,i+n-len(table)+1))
                pass
            case "antidiagonal":
                cur_color = color.CYAN
                if n < len(table[0]):
                    for i in range(index, index+len(word)):
                        boldedLetters.append((i, n-i))
                else:
                    for i in range(index, index+len(word)):
                        boldedLetters.append((n-len(table[0])+i+1, len(table[0])-i-1))
                pass

        for i in range(len(table)):
            line = ""
            for j in range(len(table[0])):
                if (i,j) in boldedLetters:
                    line += f"{cur_color}{table[i][j].upper()}{color.END}  "
                else:
                    line += str(table[i][j].upper()) + "  "
            print(line)
        print("\n")

if __name__ == "__main__":
    parseTable()
    findAllWords()
    printOutput()