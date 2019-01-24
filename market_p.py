import sysv_ipc 
import multiprocessing
import threading
import os
import time
import random
import threading
import signal
import matplotlib.pyplot as plt
import numpy


prix = multiprocessing.Value('f', 10.0)

def handler(sig, frame):
    global u
    global w
    global prix
    if(sig == signal.SIGUSR1):
        u = 1
        calculePrix()
    if(sig == signal.SIGUSR2):
        w = 1
        calculePrix()
    u = 0
    w = 0
    
def external(context):
    while context.value:
        time.sleep(random.randint(10,15))
        print("------> Evenement external : La France est en guerre avec les Etats-Unis (Prix du petrole augmente)")
        os.kill(os.getppid(), signal.SIGUSR1)
    
        time.sleep(random.randint(20, 25))
        print("------> Evenement external : La France a gagne la guerre! Bravo les bleus! Allons enfants de la patrie...")
        os.kill(os.getppid(), signal.SIGUSR2)


def calculePrix():
    global currentArgent
    
    prixPrec = prix.value
    prix.value = prixPrec + weather*0.001 + u*4.9 + w*(-4) + (currentArgent-argent.value)*0.004
  
    print("         NOUVEAU PRIX  :", round(prix.value,2))
   

        
def transation(prix, qte, t, argent,mqm, pid, sem):
    
    if t == 1:
        argent.value -= qte*prix.value
    
    if t == 2:
        argent.value += qte*prix.value
    
    toSend = str(qte)+"/"+str(t)
    mqm.send(toSend.encode() , type = pid)
    if t == 2:
        print("Transation effectué :",round(qte,2), "d'energie vendue à la maison", pid)
    if t == 1:
        print("Transation effectué :",round(qte,2), "d'energie vendue par la maison", pid)
    sem.release()
    calculePrix()
    global currentArgent
    
    currentArgent = argent.value
    


def market(keym, wValue, cont):
    
    global prix
    global u
    global w
    global argent
    
    
    u = 0
    w = 0
    
    mqm = sysv_ipc.MessageQueue(keym)
    MAX_TRANSATIONS = 2
    sem = threading.Semaphore(MAX_TRANSATIONS)
    
    signal.signal(signal.SIGUSR1, handler)
    signal.signal(signal.SIGUSR2, handler)
    
    argent = multiprocessing.Value('f', 100.0)
    
    context = multiprocessing.Value('i', 1)
        
    global currentArgent
    currentArgent = argent.value


    ext = multiprocessing.Process(target = external, args = (context,))
    graphique = multiprocessing.Process(target = graph2, args = (prix, context))
    
    ext.start()
    graphique.start()
    global weather
    
    time.sleep(1)
    
    while cont.value:
        
        weather = wValue.value
        u = 0
        w = 0
        
        #print(" Market attend un message...")
        message = None
        try:
            message, tt = mqm.receive(block = False, type = 1)
            message = message.decode()
            #print("Market", os.getpid(),": a recu le message ", message, "de type 1")
            mes = message.split("/")
            #print("mes", mes)
            sem.acquire()
            trans = threading.Thread(target = transation, args=(prix, float(mes[1]), tt, argent, mqm, int(mes[0]), sem))
            trans.start()
            trans.join()
            
        except:
            True
        
        try: 
            message, tt = mqm.receive(block = False, type = 2)
            message = message.decode()
            #print("message",message)
            #print("Market", os.getpid(),": a recu le message ", message, "de type 2")
            mes = message.split("/")
            #print("mes", mes)
            sem.acquire()
            trans = threading.Thread(target = transation, args=(prix, float(mes[1]), tt, argent, mqm, int(mes[0]), sem))
            trans.start()
            trans.join()
           
        
        except:
            True
            
   
        time.sleep(5)
        calculePrix()
    context.value = 0    
    graphique.join()
    ext.join()

    
def graph2(prix, context):
    

    xdata = []
    ydata = []

    plt.show()

    axes = plt.gca()
    plt.ion ()
    axes.set_xlim(0, 100)
    axes.set_ylim(0, +30)
    line, = axes.plot(xdata, ydata, 'r-')
    
    
    i = 0
       
    while context.value:
        
            
            if i<100:
                xdata.append(i)
            ydata.append(prix.value)
            if i>=100:
                del ydata[0]
            if i<100:
                line.set_xdata(xdata)
            else:
                line.set_xdata(numpy.arange ( len (ydata)))
            line.set_ydata(ydata)
            plt.draw()
            plt.pause(1e-17)
            time.sleep(0.1)
            i += 1





