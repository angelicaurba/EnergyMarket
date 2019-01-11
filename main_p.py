import home_p
#import market_p
import sysv_ipc
import multiprocessing
from multiprocessing import Process, Value, Array

weatherValue = Value('d',0.0)


keyh = 123      #clé pour la queue entre les homes
keym = 321      #clé pour la queue entre les homes et le market
    
mqm = sysv_ipc.MessageQueue(keym, sysv_ipc.IPC_CREAT)
mqh = sysv_ipc.MessageQueue(keyh, sysv_ipc.IPC_CREAT)



pm1 = multiprocessing.Process(target = home_p.home, args = (1, keyh, keym,weatherValue))
#pm2 = multiprocessing.Process(target = home_p.home, args = (2, keyh, keym,weatherValue))
#pm3 = multiprocessing.Process(target = home_p.home, args = (3, keyh, keym,weatherValue))


pm1.start()
#pm2.start() 
#pm3.start() 
#pm1.join()

#pm2.join()

#pm3.join()
