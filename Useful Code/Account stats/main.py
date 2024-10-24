import pandas as pd
import matplotlib.pyplot as plt



def read(year):
    global df
    df = pd.read_csv("/home/qbodart/Git/Work/Useful Code/Account stats/data" + year + ".csv", sep=";", dayfirst=True, parse_dates=[1], decimal=",")
    df.drop(["Compte","Num?ro d'extrait","Num?ro de transaction","Rue et num?ro","Code postal et localit?","Transaction","Date valeur","Devise","BIC","Code pays","Communications"], axis=1, inplace=True)
    df.drop(df[df["Compte contrepartie"] == "BE76 0836 5445 8595"].index)
    df.drop(df[df["Compte contrepartie"] == "BE05 7925 3708 1675"].index)

def getAmountByDest():
    all_paid = []
    dests = {}
    for i, data in df.iterrows():
        if data["Nom contrepartie contient"] in dests.keys():
            dests[data["Nom contrepartie contient"]] += float(data["Montant"])
        else :
            dests[data["Nom contrepartie contient"]] = float(data["Montant"])

    for dest, amount in dests.items():
        all_paid.append((dest, amount))

    all_paid.sort(key=lambda a: a[1])

    return all_paid

def getMonthSpendings():
    output = []
    for i in range(1,13):
        month = df[df['Date de comptabilisation'].dt.month == i]
        output.append((i, month["Montant"].astype(float).sum()))
    return output

def printYearlyAmountByDest(start,stop):
    for i in range(start,stop+1):
        print(f"YEAR {i}:\n__________")
        read(str(i))
        total = 0.0
        for dest, sum in getAmountByDest():
            if (dest == "Bodart Denis" or dest == "Kryszczak Elwira" or dest == "Bodart Quentin"):
                continue
            total += sum
            print(f"{dest} : {sum:.2f}")
        print(f"TOTAL : {total}")
        print("\n")

def printYearlyMonthSpendings(start,stop):
    for i in range(start,stop+1):
        print(f"YEAR {i}:\n__________")
        read(str(i))
        for month, sum in getMonthSpendings(): 
            print(f"Month {month:2} : {sum:.2f}€")
        print("\n")


if __name__ == "__main__":
    # printYearlyAmountByDest(2021,2024)
    printYearlyMonthSpendings(2021,2024)