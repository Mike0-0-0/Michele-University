# -*- coding: utf-8 -*-
"""
Created on Mon May  5 15:33:24 2025

@author: miche
"""
#PRIMO STADIO DELLA SIMULAZIONE

import matplotlib.pyplot as plt
import numpy as np

#INIZIALIZZAZIONE DELLE VARIABILI
N=200
N_f=1 #numero di granelli che vengono trasferiti dalle celle instabili
N_iter=50000 #numero iterazioni
Z_c=10

P0=0.5 #probabilità di pioggia su ogni cella (fissata)
lost=0

#CREAZIONE DELLE LISTE DI OUTPUT
activity =[]
mass=[]
confinement_time=[] #inseriremo con un append il tempo di confinamento del granello marcato

K=100
for run in range(K):
    Ret=np.zeros(N)
    Ret[0] += 1 #iniettiamo forzatamente il granello nel primo sito
    grain_pos=0 #con questa variabile teniamo traccia della posizione del granello nel reticolo
    time=0 # stima tempo di confinamento 
    uscita=False 
#RUNNING SANDPILE
    for j in range (N_iter):
        time +=1 #ogni volta che iteriamo aggiorniamo il tempo
        a=0 #contatore celle instabili. Aggiungeremo alla lista activity
        v=np.random.choice([1,0] , size=N , p=[P0, 1-P0])
        Ret += v
    
    #ENTRIAMO NEL CICLO WHILE 
        unstable=True
        while unstable:
            
        #IPOTESI DI STABILITà DEI SITI
            unstable=False
        #CHECK DEI SITI INSTABILI
            for k in range(len(Ret)-1):
                if Ret[k]-Ret[k+1]>=Z_c:
                    
                    Ret[k]=Ret[k]-N_f
                    Ret[k+1]=Ret[k+1]+N_f
                    a +=1 
                    unstable=True
                    if grain_pos==k:
                        grain_pos+= 1
            if Ret[-1]>0:
                if grain_pos==N-1 and not uscita:#altrimenti il granello marcato resterebbe virtualmente nel sito N-1
                    confinement_time.append(time)
                    #print(confinement_time)
                    uscita=True  #uscita effettiva del granello marcato
                lost += Ret[-1]
                a+=1
                Ret[-1]=0 
                unstable=True
    
        
    if run==0:
        #AGGIUNGO ALLA LISTA IL NUMERO DI SITI INSTABILI PER QUESTA ITERAZIONE
        activity.append(a)
        #AGGIUNGO ALLA LISTA LA MASSA DEL RETICOLO A QUESTA ITERAZIONE
        mass.append(np.sum(Ret))
    
print(confinement_time) #printa un singolo valore
#PLOT DELLA MASSA
plt.figure(figsize=(10,4))
plt.plot(mass, linestyle="-")
plt.axhline(np.mean(mass[-2000:]), linestyle="--", color="red", label="massa media in SOC") #prende la media degli ultimi duemila elementi del vettore mass
plt.axvline()
plt.xlabel("Iterazioni")
plt.ylabel("Massa ")
plt.title("Raggiungimento del SOC")
plt.legend()
plt.show()

#PLOT DELL'ATTIVITà
plt.figure(figsize=(10,4))
plt.plot(activity, linestyle="-")
plt.axhline(np.mean(activity[-2000:]), linestyle="-", color="red", label="attività media a regime") #prende la media degli ultimi duemila elementi del vettore activity
plt.xlabel("Iterazioni")
plt.ylabel("Numero di siti instabili")
plt.title("Attività")
plt.legend()
plt.show()
            
            
    
    