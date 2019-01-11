#cette function represente l'execution de l'entité "home"
#chaque entité va etre un different Processus qui va s'executer au meme temps des autres

#chaque home utilise deux Queue: 
#   -une pour communiquer avec les autres homes pour demander/donner de l'energie entre eux
#   -l'autre pour communiquer avec le market pour acheter/vendre de l'energie

#pour les messages échangés avec les Queues on va utiliser les pids de chaque processus 
#pour determiner les types des messages envoyés

import sysv_ipc     #on va utiliser ce module pour les Queues

#pour synchroniser la lecture/écriture de la valeur écrite par le Processus weather 
#et lu par les homes et le market
#on va utiliser la solutione du probléme readers/writer qui utilise deux mutex 
#   -un pour bloquer les rideurs si le weather est en train d'écrire (lockWeather)
#   -l'autre pour proteger le conteur quand'il est modifié  (lockCont)
#et un conteur pour voir combien de processus sont en train de lire  (nbReaders)

import multiprocessing
import os
import time

avance = False

nbReaders = 0  

def handler(signal, frame):
    if sig == signal.SIGUSR1:
        avance = True
        
    


def home(t, lockWeather, lockCont):
    
    VAL_INIT = 10   #valeur initiale d'énergie
    keyh = 123      #clé pour la queue entre les homes
    keym = 321      #clé pour la queue entre les homes et le market
    
    
    energie = VAL_INIT    
    
    mqh = sysv_ipc.MessageQueue(keyh)
    mqm = sysv_ipc.MessageQueue(keym)
    
    signal.signal(signal.SIGUSER1, handler)
    
    mqm.send(str(os.getpid()).encode(), 1)
    pidMarket, t1 = mqm.receive(block = True, 2)
    
    pidMarket = int(pidMarket.decode())
    
    while True:
        
        avance = False
    
        #production d'energie en function du type (les valeurs sont arbitraires,
        #il faudra probablement les redéfinir )
        if (t == 1):
            energie += 2
        else if (t == 2):
            energie += 3
        else:
            energie += 4
        
    
        #pour consommer l'energie il faut lire sur la memoire partegée
        #la valeur écrite par le processus weather
        lockCont.acquire()
    
        nbReaders+=1
        if(nbReaders == 1):
            lockWeather.acquire()  #le premier qui lu va bloquer le weather
    
        lockCont.release()
    
        consommer = WeatherValue  #la valeur est lu
    
        lockCont.acquire()
    
        nbReaders-=1
        if(nbReaders ==0):
            lockWeather.release()  #le dernier redeur va debloquer le weather
    
        lockCont.release()
    
    
        #ici on recalcule la valeur d'energie en function du type de home 
        #(valeur arbitraires, il faudra les recalculer)
        if(t == 1):
            consommer+=1
        else if(t == 2):
            consommer+=2
        else:
            consommer+=3
        
        #on voit si la consumation d'energie porte la home à avoire une energie plus basse 
        #d'un certain seuil (ici la valeur initiale) 
        #si c'est le cas la home va demander aux autres homes 
        #s'elles ont de l'energie en plus
        if(energie-consommer < VAL_INIT):  
            mqh.send(str(-1).encode, type = os.getpid()+3) 
            #pour demander de l'energie on envoye une valeur negative 
            #comme message sur la queue, pour distinguer les demandes et les donations
            #on envoye aussi le pid du processus 
            #pour avoire un type different pour chaque processus home
            time.sleep(1)
        
            message, tt = mqh.receive(block = false, type = os.getpid()+3)
            recu = int(message.decode())
        
            #si la home a reçu une valeur differente de -1 ça veut dire 
            #que la home a reçu de l'energie
            #donc on rajoute cette energie à l'energie de la home 
            if(recu > 0):
                energie+=recu
        
            #si la valeur reçu est inferieur à 0, ça veut dire 
            #que la home a lu le meme message qu'elle avait envoyé,
            #donc il y a personne que peut donner de l'energie, 
            #donc elle va l'acheter du market
        
            else:
                mqm.send(str(-(energie+consommer-VAL_INIT)).encode, type = os.getpid()+3)
                message, tt = mqh.receive(block = true, type = os.getpid()+3)
                #c'est necessaire faire une "receive" qui est bloquant,
                #parce que la home ne peut pas consommer sans recevoire l'energie
            
                recu = int(message.decode())
                energie+=recu
            
            
        #consumation d'energie (les valeurs sont arbitraires et dependent du type)       
        if (t == 1):
            energie -= 3
        else if (t == 2):
            energie -= 2
        else:
            energie -=4 
        
     
    
        
        envoyer = energie-VAL_INIT
        #on calcule l'eventuelle energie en plus que la home peut donner/vendre
        #en dependant du type de home elle va donner ou vandre l'energie
        if envoyer>0:
            
            if(t == 1):
                message, tt = mqh.receive(block = false, type = 0)  #lit par la queue 
                if(int(message.decode()) != -1):        
                    #si la valeur lit est different de -1 le message n'est pas une demande
                    mqh.send(message, tt)               
                    #donc il va reécrire sur la queue le meme message
                else: 
                    mqh.send(str(envoyer).encode(), tt)      
                    #s'il lit une demande, il envoit l'energie 
                    energie-= envoyer
            
            elif(t == 2):
                mqm.send(envoyer.encode(), os.getpid()+3)       
                #il vende l'energie au market
                energie-=envoyer
        
            else:
                message = None 
                message, tt = mqh.receive(block = false, type = 0)
                if(int(message.decode()) != -1):
                    mqh.send(message, tt)
                elif(int(message.decode()) <= 0): 
                    mqh.send(envoyer.encode(), tt)
                    energie-= envoyer
            
                else:
                    mqm.send(envoyer.encode(), os.getpid()+3)   
                    #s'il a pas reçu un message ça veut dire qu'il n'y a pas de homes
                    #auquelles donner de l'energie, donc il vende l'energie au market
                    energie-= envoyer
            
            
    
        os.kill(pidMarket, signal.SIGUSR1)      
    
        while(not avance):
            pass
    
    #pour faire une syncronisation entre les homes, à la fin de chaque tour de boucle 
    #chaque home envoye un message au market
    #le market compte le nombre de signal reçus 
    #et quand il arrive à recevoir un signal de toutes les homes il debloque les homes
    #en envoyant un signal qui fait sortir de la dernier boucle while
    
            
        
                
    
    
    
    