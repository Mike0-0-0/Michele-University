# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:07:42 2025

@author: miche
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Dati numerici
P0= np.array([0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5]) #Lunghezze reticolo
tau_c = np.array([17134, 11490, 8615, 6939, 5777, 4979, 4362, 3868, 3496])  # Tempi di confinamento


# Fit 
def model(x, A, b):
    return A*x**b

popt, _ = curve_fit(model, P0, tau_c)
A,b= popt
y=np.arange(min(P0), max(P0), 0.001)
#y=np.linspace(min(P0),max(P0))
tau_fit = model(y,A, b)
#print(tau_fit) # Ricostruzione per il plot
#print(popt) #Stampa parametri ottimali

plt.figure(figsize=(6, 4))
plt.plot(P0, tau_c, 'o', label='Dati simulati')
plt.plot(y, tau_fit,  '-', label=r"$\tau_c \propto P_{0}^{-0.98}$")
plt.xlabel(r"$P_{0}$ (probabilità di iniezione)")
plt.ylabel(r"$\tau_c$ (time iteration)")
plt.title("Fit di $\\tau_c$ con $P_0$")
plt.xticks(np.arange(0.1, 0.55, 0.05)) 
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

