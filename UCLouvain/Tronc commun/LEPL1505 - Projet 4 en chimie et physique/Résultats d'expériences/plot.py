import matplotlib.pyplot as plt
import csv
import scipy as sp

# unset GTK_PATH

def parseFTIR(filename):
    wn = [] # wave number (cm-1)
    t = [] # transmittance

    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            wn.append(float(row[0][0:7])*(10**int(row[0][-3:])))
            t.append(float(row[1][0:7])*(10**int(row[1][-3:])))
    
    return wn, t

def pltFTIR(filename):
    wn, t = parseFTIR(filename)
    peaks, _ = sp.signal.find_peaks([-value for value in wn])
    print(f"Peaks found : {[value for value in peaks]}")

    # plt.title("FTIR - " + filename.split("/")[1].split(".")[0])
    plt.title("FTIR")
    plt.xlabel("Wave number [cm-1]")
    plt.ylabel("Transmittance")
    plt.plot(wn, t)
    ax = plt.axis()
    plt.axis((ax[1],ax[0],ax[2],ax[3]))
    plt.show()
    
def parseTGA(filename):
    t = []   # temperature
    w = []  # weight

    with open(filename) as f:
        for line in f.readlines():
            aline = [value for value in line.split(" ") if value != ""]
            aline[-1] = aline[-1][:-1]
            
            if aline[0].isdigit(): # checking if line contains informations
                # weight
                if aline[2].startswith("-"):
                    w.append(-float(aline[2][1:8].replace(",","."))*(10**(int(aline[2][9:]))))
                else:
                    w.append(float(aline[2][:7].replace(",","."))*(10**(int(aline[2][8:]))))

                # temperature
                if aline[3].startswith("-"):
                    t.append(-float(aline[3][1:8].replace(",","."))*(10**(int(aline[3][9:]))))
                else:
                    t.append(float(aline[3][:7].replace(",","."))*(10**(int(aline[3][8:]))))
    
    return t, w

def pltTGA(filename):
    t, w = parseTGA(filename)

    plt.title("TGA - " + filename.split("/")[1].split(".")[0])
    plt.xlabel("Temperature [°C]")
    plt.ylabel("Mass [g]")
    plt.plot(t, w)
    plt.show()

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

    plt.title("DSC - " + filename.split("/")[1].split(".")[0])
    plt.xlabel("Temperature [°C]")
    plt.ylabel("Heatflow [W/g]")
    plt.plot(t, hf)
    plt.show()

def pltAllDSC(filenames):
    thfs = []
    for filename in filenames:
        t, hf = parseDSC(filename)
        thfs.append([t,hf])
    
    plt.title("DSC")
    plt.xlabel("Temperature [°C]")
    plt.yticks([0,1])
    plt.ylabel("Heatflow [W/g]")
    for i in range(len(filenames)):
        if filenames[i] == "DSC/Refroidissement.txt":
            index = thfs[i][1].index(max(thfs[i][1]))
        else:
            index = thfs[i][1].index(min(thfs[i][1]))
        print(f"Extrema heat flow : {thfs[i][1][index]} at temperature {thfs[i][0][index]}\n")
        plt.plot(thfs[i][0], [thfs[i][1][j]+i*0.75 for j in range(len(thfs[i][1]))])
    plt.legend(["First heating", "Second heating", "Cooling"],loc="upper left")
    plt.show()

# Change "/" into "\\" on Windows 
def pltAll():
    pltDSC("DSC/1e chauffe.txt")
    pltDSC("DSC/2e chauffe.txt")
    pltDSC("DSC/Refroidissement.txt")
    pltFTIR("FTIR - ATR/Boite noire t.CSV")
    pltTGA("TGA/TGA.txt")


# pltAll()
pltAllDSC(["DSC/1e chauffe.txt","DSC/2e chauffe.txt","DSC/Refroidissement.txt"])