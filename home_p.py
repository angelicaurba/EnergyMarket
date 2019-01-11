import sysv_ipc 
import multiprocessing
import os
import time
import random

def home(t, keyh, keym, wValue):
    
    VAL_INIT = 10   #valeur initiale d'énergie
    #keyh = 123      #clé pour la queue entre les homes
    #keym = 321      #clé pour la queue entre les homes et le market
    
    
    energie = VAL_INIT 
    delayMax = 5
    
    mqh = sysv_ipc.MessageQueue(keyh)
    mqm = sysv_ipc.MessageQueue(keym)
    
    
    while True:
        
        #production d'energie en function du type (les valeurs sont arbitraires,
        #il faudra probablement les redéfinir )
        if (t == 1):
            #energie += random.randint(2,5)
            production = 2
            energie += production
        elif (t == 2):
            #energie += random.randint(2,5)
            production = 5
            energie += production
        else:
            #energie += random.randint(2,5)
            production = 3
            energie += production
            
        #TODO : lire la valeur de weather avec la memoire partagée (Value)
        consommer = wValue.value
        
        #print(consommer,t)
        
        
        if(t == 1):
            #consommer+=random.randint(2,5)
            consommer+= 5
        elif(t == 2):
            #consommer+=random.randint(2,5)
            consommer+= 1
        else:
            #consommer+=random.randint(2,5)
            consommer+= 10
            
            
        if(energie-consommer < VAL_INIT):  
            print("Maison", os.getpid(), "demande",VAL_INIT+consommer-energie, "d'energie aux autres maisons")
            
            toSend = str(os.getpid())+"/"+str(-energie+consommer+VAL_INIT)+"/"+str(time.time())
            mqh.send(toSend.encode(), type = 1) 
            
            #pour demander de l'energie on envoye une valeur negative 
            #comme message sur la queue, pour distinguer les demandes et les donations
            #on envoye aussi le pid du processus 
            #pour avoire un type different pour chaque processus home
            time.sleep(2)
            
            try:
                message, tt = mqh.receive(block = False, type = 2)
            
            
                mes = message.decode().parse("/")
                recu = float(mes[1])
                pidDonneur = mes[0]
                tempsOffre = mes[2]
                
                if (time.time() - float(tempsOffre)) < delayMax:
                    
                    mqh.send(str(pidDonneur,"/",recu,"/",time.time()).encode(),type=3)
                    energie+=recu
                

                
                
            except :
                print("Pas d'offre d'energie...")

            
            if(energie-consommer < VAL_INIT): 
                
                
                print("Demande au market...")
                
                
                
                #mqm.send(str(energie-consommer-VAL_INIT).encode(), type = os.getpid()+3)
                #message, tt = mqm.receive(block = true, type = os.getpid()+3)
                #c'est necessaire faire une "receive" qui est bloquant,
                #parce que la home ne peut pas consommer sans recevoire l'energie
            
                #recu = int(message.decode())
                #energie+=recu
            
        