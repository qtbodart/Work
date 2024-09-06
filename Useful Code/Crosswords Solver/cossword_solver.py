table = ["rrdvnisagammwbz",
         "zeqeiannomaaceb",
         "boutiquegrdahsy",
         "tejgmruhcddcsae",
         "nchooeqhydrocfw",
         "aofyslasialhxec",
         "cneqenaemdaieuc",
         "royedcqtetycnul",
         "emotleisarvhrei",
         "milneytfsceeuce",
         "mqpeqgdaefyqorn",
         "oumvomdelnnutet",
         "ceetomeutaeesde",
         "retnegrabtgbiil",
         "bjeiretarbeerte"]

words = ["achat",
         "argent",
         "banque",
         "benefice",
         "boutique",
         "braderie",
         "budget",
         "caddie",
         "catalogue",
         "cheque",
         "client",
         "clientele",
         "commercant",
         "credit",
         "dette",
         "economique",
         "employe",
         "etalage",
         "grandesurface",
         "independant",
         "magasin",
         "marchand",
         "marchandise",
         "marche",
         "monnaie",
         "publicite",
         "ristourne",
         "soldes",
         "vendeur",
         "vendeuse",
         "vente"]

output = []

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
    
    for n_line, line in enumerate(cur_table):
        for word in words:
            if word in line :
                output.append((str(orientation) + str(n_line) + " upright", word))
            if word in line[::-1]:
                output.append((str(orientation) + str(n_line) + " reversed", word))

def findAllWords():
    findWords("horizontal")
    findWords("vertical")
    findWords("diagonal")
    findWords("antidiagonal")
    
def printOutput():
    for orientation, word in output:
        print(f"found word {word} in {orientation}\n")

if __name__ == "__main__":
    findAllWords()
    printOutput()