#function qui implement les conditions qui faitent changer la valeur
#avec laquelle on decide la consommation d'energie 
#la fonction funcCalculWheater retourne un tableau des valeurs 
#calculées à partire de deux fonctions
#   -saisonAnnee 
#   -rechauffementClimatique

#à chaque tour de boucle le processus weather va proteger sa memoire partagée 
#avec le mutex lockWeather et donc il modifie la valeur
#en avancent sur le tableau dans une maniére cyclique

import time


#memoire partagée
WeatherValue = VAL_INIT

def weather(lockWeather):
    
    valeurs = funcCalculWheater()
    # ce sera en fonction des deux fonctions precedentes
    #ça renvoit un tableau de N valeurs (N arbitraire mais suffisamment grande)
    index = 0
    
    while True:
        time.sleep(3)
        lockweather.acquire()
        
        WeatherValue = valeurs[index]
        index = (index+1)%len(valeurs)
        
        lockWeather.release()
    
    
def saisonAnnee():
        # function periodique qui calcule le consommation en fonction de la temperature

def rechauffementClimatique():
        # function que fait augmenter les ecarts de la fonction temperature    