import home_p
import market_p
import weather_p
import sysv_ipc
import multiprocessing
from multiprocessing import Process, Value, Array, Pipe
import sys
import threading
import os
import time
import signal

#os.system("ipcrm -Q 123")
#os.system("ipcrm -Q 321")


        
weatherValue = Value('f',0.0)
cont = Value('i', 1)


keyh = 123      #clé pour la queue entre les homes
keym = 321      #clé pour la queue entre les homes et le market
    
mqm = sysv_ipc.MessageQueue(keym, sysv_ipc.IPC_CREAT)
mqh = sysv_ipc.MessageQueue(keyh, sysv_ipc.IPC_CREAT)

#signal.signal(signal.SIGINT, handler)

try:
    nbHomes = int(sys.argv[1])
except:
    nbHomes = 6
    
try:
    temps = int(sys.argv[2])
except:
    temps = 150

if __name__ == "__main__":
    print("Starting the simulation for", nbHomes,"homes")
    
    market = multiprocessing.Process(target = market_p.market, args = (keym, weatherValue, cont))
    homeList = [multiprocessing.Process(target = home_p.home, args = (keyh, keym,weatherValue, cont)) for i in range(nbHomes)]
    weather = multiprocessing.Process(target = weather_p.weather, args = (weatherValue, cont))
    
    weather.start()
   
    market.start()
    for currentHome in homeList:
        currentHome.start()
        
    time.sleep(temps)
    cont.value = 0

   
    market.join()
    
    #for currentHome in homeList:
        #currentHome.join()
    
    weather.join()
    
    
    #weather.join()
    
    mqm.remove()
    mqh.remove()
    print("--------------- Fin de la simulation ---------------")
   


