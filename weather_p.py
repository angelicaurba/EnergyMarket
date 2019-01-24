from multiprocessing import Value
import time
import math
import matplotlib.pyplot as plt
from pylab import *
import random



def weather(wValue, cont):
    VAL_INIT = 1.0
    valeurs = calculeValeurs()
    wValue.value = VAL_INIT
    index = 0
    l = len(valeurs)

    while cont.value:
        wValue.value = round(valeurs[index], 2)
        index = (index+1)%(l)
        #print("Current weather value :",round(wValue.value,2))
        t = arange(0.0, 50.0, 1)

        time.sleep(2)


def calculeValeurs():
    x = []
    N = 20
    for i in range(N):
        val = math.sin(float(i)*2*math.pi/float(20))
        val = math.fabs(val)
        val = val*4 + 1
        val = val + random.randint(-1, 1)
        val = round(val, 2)
        x.append(val)
        
    return x
        

