import numpy as np
import matplotlib.pyplot as plt

argent_recu = 420

def partie_remboursee(montant):
    if montant < 450*(100/35):
        return montant*.35
    return 450

x = np.linspace(500, 1400, 1000)
y = []

for i in range(len(x)):
    y.append(x[i]-partie_remboursee(x[i])-420)

y = np.array(y)

plt.plot(x,y)
plt.grid(visible=True)
plt.show()