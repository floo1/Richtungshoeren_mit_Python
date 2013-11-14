from testsource import *
import numpy as np


#von 13.11.13
f= np.array([[0, 1, 2],[3, 4, 5],[6, 7, 8]])
r= np.array([[1, 1, 1],[1, 1, 1],[1, 1, 1]])


x,y=addieren(f,r)
print("Der Rueckgabewert von y ist %f und von x %f" %(y,x))
k=x+y
#print("Die Summe aus x und y sollte Null ergeben, bitte lasse dir den Wert von k anzeigen.")

