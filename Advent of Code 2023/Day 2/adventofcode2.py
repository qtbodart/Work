def lineChonker(line):
    if(line[-1] == '\n'):
        treated = line[0:-1]
    else:
        treated = line
    treated = treated.split(':')[1][1:-1]

def elNumerator(line):
    return