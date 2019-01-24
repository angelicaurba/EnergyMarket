import sysv_ipc 

import multiprocessing

import os

import time

import random



def home(keyh, keym, wValue, cont):

    

    VAL_INIT = 10   #valeur initiale d'énergie

    #keyh = 123      #clé pour la queue entre les homes

    #keym = 321      #clé pour la queue entre les homes et le market

    

    

    energie = VAL_INIT 

    delayMax = 10

    

    mqh = sysv_ipc.MessageQueue(keyh)

    mqm = sysv_ipc.MessageQueue(keym)

    

    

    while cont.value:
        #production d'energie
        
        #energie += random.randint(2,5)

        production = random.uniform(1,5)

        energie += production

        #TODO : lire la valeur de weather avec la memoire partagée (Value)

        consommer = wValue.value

        #print(consommer,t)


        #consommer+=random.randint(2,5)

        consommer+= random.uniform(0,2)

       

        if(energie-consommer < VAL_INIT):  

           # print("Maison", os.getpid(), "demande",VAL_INIT+consommer-energie, "d'energie aux autres maisons")

            #toSend = str(os.getpid())+"/"+str(-energie+consommer+VAL_INIT)+"/"+str(time.time())

            #mqh.send(toSend.encode(), type = 1) 

            print("Maison", os.getpid(), ": a besoin d'energie:", round(-energie+consommer+VAL_INIT,2))
            
            #time.sleep(5)

            try:
                
                message, tt = mqh.receive(block = False, type = 2)
                message = message.decode()
                
                mes = message.split("/")

                recu = float(mes[1])

                pidDonneur = mes[0]

                tempsOffre = mes[2]

                #print("Maison", os.getpid(), ": a recu le message:", message, "---> temps =", time.time() - float(tempsOffre))
                
                

                if (time.time() - float(tempsOffre)) < delayMax:

                    
                    print("Maison", os.getpid(), ": a recu d'energie par la maison ", pidDonneur, round(recu,2))
                    mqh.send(str(pidDonneur,"/",recu,"/",time.time()).encode(),type=pidDonneur)

                    energie+=recu


            except :

                print("Maison", os.getpid(), ": pas d'offre d'energie...")



            if(energie-consommer < VAL_INIT): 


                print("Maison", os.getpid(), "demande au market...")
                
                toSend = str(os.getpid())+"/"+str(-energie+consommer+VAL_INIT)
                mqm.send(toSend.encode(), type = 2)
                
                #time.sleep(delayMax)

                print("Maison", os.getpid(), ": attende l'energie du market")
                message, tt = mqm.receive(block = True, type = os.getpid())

                #c'est necessaire faire une "receive" qui est bloquant,
                #parce que la home ne peut pas consommer sans recevoire l'energie
                mes = message.decode().split("/")
                recu = float(mes[0])
                
                print("Maison", os.getpid()," :reçu",round(recu,2),"d'energie du market")

                energie+=recu
                
        #consommation
        energie-= consommer
        
        
        #je vois si j'ai de l'energie en plus
        plus = energie-VAL_INIT
        
        if plus >= 1:
            
            print("Maison", os.getpid(), "offre son plus d'energie :", round(plus,2))
            toSend = str(os.getpid())+"/"+str(plus)+"/"+str(time.time())
            mqh.send(toSend.encode(), type = 2)
            
            time.sleep(10)
            
            try:
                message, tt = mqh.receive(block = False, type = os.getpid())
                energie -= plus
                print("Maison", os.getpid(), ": a envoyé",round(plus,2),"à une autre maison")
            
            except:
                
                print("Maison", os.getpid(), "vend son plus d'energie au market:", round(plus,2))
                toSend = str(os.getpid())+"/"+str(plus)
                mqm.send(toSend.encode(), type = 1)
                message, tt = mqm.receive(block = True, type = os.getpid())
                
                message = message.decode()
                mes = message.split("/")
                
                if int(mes[1] == 1):
                    energie -= float(mes[0])
                
            
            