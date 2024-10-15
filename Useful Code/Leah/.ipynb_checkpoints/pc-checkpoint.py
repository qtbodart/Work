import numpy as np
import matplotlib.pyplot as plt

argent_recu = 420

def partie_remboursee(montants):
    remboursement = []
    for i in range(len(montants)):
        if montants[i] <= 450*(100/35):
            remboursement.append(.35*montants[i])
        else:
            remboursement.append(450)
    return remboursement

x = np.linspace(500, 2000, 1000)
plt.plot(x,(x-argent_recu)-partie_remboursee(x))
plt.show()