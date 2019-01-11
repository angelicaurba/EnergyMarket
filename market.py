import sysv_ipc
import multiprocessing
import os
import time
import signal
import random

#le market est un processus qui s'occupe des transations d'energie
#il communique avec les homes avec une Queue en envoyant/recevant de l'energie
#il fait la syncronisation entre les homes : 
#il reçcoit un signal de chaque home quand elle arrive à la fin de sa boucle
#pouis il envoye à chaque maison un signal pour les debloquer

key = 321
mqm = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

wait = True     #wait c'est une variable qui sert à dire au market 
                #s'il doit continuer à lire sur la queue partagée avec les homes
                #si wait devient false ça veut dire que toutes les homes 
                #sont arrivée à la fin de la boucle et ils peuvent repartir

argent = 100        #cette variable sert à voire si il y a beaucoup des homes qui vendent ou achetent l'energie
                    #ça sert à décider comment le prox de l'energie doit varier
countHomes = 0      #counteur des homes qui ont fini leur tour de boucle

prix = 1

prixMutex = Mutex()

lockCountHomes = Mutex()   #ce mutex sert à proteger le couteur des homes

mutex = Mutex()             #ce mutex sert à proteger la variable argent 
                            #quand'elle est modifiée pendant les transactions
 

 def handler(signal, frame):
    if signal == signal.SIGUSER1:   #SIGUSER1 est reçu par les homes
        lockCountHomes.acquire()
        countHomes +=1
        lockCountHomes.release()
    
    if signal == signal.SIGUSER2:   #SIGUSER2 est reçu par external, le fils du market
        mettrePrixAJour(prix, lockWeather, lockCont, True)
 


 #cette fonction définit le comportement du fils du market
#dans des moment aleatoires il envoye un signal au père 
#qui réagit en mettant à jour le prix de l'energie

#elle represent deux evenement qui peuvent changer en maniére asyncrone la valeur du prix
#les deux evenement vont envoyer le meme signal 
#mais avec des probabilitées differentes pour simuler deux types d'evenement 
        
def external():
    
    while(True):
        if random.randint(0,1)==0:     
            time.sleep(random.uniform(1,2)*5)
            os.kill(os.getppid(), signal.SIGUSER2)
        if random.randint(0,5)==5:
            time.sleep(random.uniform(2,3)*5)
            os.kill(os.getppid(), signal.SIGUSER2)
        

        
#transation c'est la fonction qui est executée par des threads
#chaque thread represents une home qui veut acheter ou vendre de l'energie

#sem est un semaphore qui sert à bloquer une transaction 
#s'il y en a déjà un nombre égale au nombre maximum qui a été defini

def transation(energie, t, prix, sem):
    
    sem.wait()
    
    mutex.acquire()
    prixMurex.acquire()
    
    if(energie<0):
        argent += energie*prix
        mqm.send(str(-energie).encode(), t)
    else: argent -=energie*prix
    
    prixMutex.release()
    mutex.release()
    
    sem.signal()
    
    

def market(n, lockWeather, lockCont):
    
    #avant de commencer l'execution, market attend que chaque home lui envoye son pid
    #(pour permettre au market d'envoyer aprés des signals aux homes )
    
    #aprés il envoye son pid à chaque home
    for i in range(n):
        pid, tt = mqm.receive(block = True, type = 1)
        pidHome[i] =int(pid.decode())
    
    for i in range(n):
        mqm.send(str(os.getpid()).encode(), 2)
     
    MAX_TRANSACTIONS = 2
    sem = Semaphore(MAX_TRANSACTIONS)
    
    signal.signal(signal.SIGUSER2, handler)
    signal.signal(signal.SIGUSER1, handler)
        
    child = Process(external)   #le fils commence son execution
    child.start()
    
        
    while True:
        wait = True
        countHomes = 0
        
        while(wait):
            req, t = mqm.receive(block = False, 0)
            req = int(req.decode())
            prix =  mettrePrixAJour(prix, lockWeather, lockCont, False) 
            
            thread = Thread(transation, arguments = (req,  t, prix, sem))
            thread.start()
            thread.join()
            
            if(countHomes == n):
                wait = False
                for i in range(n):
                    ok.kill(pidHome[i], signal.SIGUSER1)
                
                
        
    child.join()         
        
        

        
def mettrePrixAJour(prix, lockWeather, lockCont, facteurExt ):
    
    a,b= 3,4 #valeurs arbitraires
    
    lockCont.acquire()
    
        nbReaders+=1
        if(nbReaders == 1):
            lockWeather.acquire()  #le premier qui lu va bloquer le weather
    
        lockCont.release()
    
        internal = WeatherValue  #la valeur est lu
    
        lockCont.acquire()
    
        nbReaders-=1
        if(nbReaders ==0):
            lockWeather.release()  #le dernier redeur va debloquer le weather
    
        lockCont.release()
        
        if(facteurExt):
            ext = 1
            
        else: ext = 0
            
        prixMutex.acquire()   
        global prix = prix + internal*a + ext*b
        prixMutex.release()
        
        
        
        
        
        
    
