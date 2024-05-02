import matplotlib.pyplot as plt

def pltFTIR():
    pass

def pltTGA():
    pass

def parseDSC(filename):
    t = []   # temperature
    hf = []  # heat flow

    with open(filename) as f:
        for line in f.readlines():
            aline = [value for value in line.split(" ") if value != ""]
            aline[-1] = aline[-1][:-1]
            
            if aline[0].isdigit(): # checking if line contains informations
                # heat flow
                if aline[2].startswith("-"):
                    hf.append(-float(aline[2][1:8].replace(",","."))*(10**(int(aline[2][9:]))))
                else:
                    hf.append(float(aline[2][:7].replace(",","."))*(10**(int(aline[2][8:]))))

                # temperature
                if aline[3].startswith("-"):
                    t.append(-float(aline[3][1:8].replace(",","."))*(10**(int(aline[3][9:]))))
                else:
                    t.append(float(aline[3][:7].replace(",","."))*(10**(int(aline[3][8:]))))
    
    return t, hf
        


def pltDSC(filename):
    t, hf = parseDSC(filename)

    plt.plot(t, hf)
    plt.show()

pltDSC("DSC/1e chauffe.txt")