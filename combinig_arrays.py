# Arrays zusammenführen
# hier mal ein Beispiel wie man Arrays zu einem Array zusammenfassen kann:

import numpy as np
# erzeuge zwei zeilenvektoren mit jew. 2 spalten 
a = np.zeros([2,2])
b =  np.array([[5,6],[7,8]])

# ranheangen der zwei vektoren als zeilenvektor in einem array
p=np.vstack([a,b])

# weiter Array erzeugen und anhaengen:
b2 = np.array([[1,1],[1,1]])
p=np.vstack([p,b2])
b3 = np.array([[2,2],[2,2]])
p3=np.vstack([p,b3])

print(p3)