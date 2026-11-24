# %%
# -*- coding: utf-8 -*-

"""
Created on Mon May 12 12:42:34 2025

@author: miche
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
K=100

tau_c_samples = np.array([33962, 34883, 33576, 34439, 33256, 34036, 34023, 35253, 34339, 33017, 34114, 33907, 34566, 35255, 33785, 35294, 34162, 33746, 34012, 34505, 34050, 34026, 33104, 34311, 35006, 34191, 34104, 34147, 34684, 35257, 33434, 33668, 34810, 33526, 36007, 33988, 33293, 35771, 33720, 33904, 33368, 34444, 34571, 33598, 34589, 34850, 33231, 34641, 34333, 34243, 33589, 35122, 34106, 33262, 33976, 34689, 33080, 34063, 32938, 34971, 34239, 33515, 33886, 34094, 34729, 34293, 33792, 35144, 33544, 36603, 33806, 33923, 33174, 33615, 33312, 33790, 34601, 34692, 34026, 34030, 35835, 34073, 34229, 34355, 34551, 34118, 34523, 35682, 34936, 34283, 33532, 34173, 33255, 34397, 34531, 34771, 35053, 33725, 34513, 34584])


# Calcolo della media e deviazione standard 
mu = np.mean(tau_c_samples)
sigma = np.std(tau_c_samples)
sem_tau=sigma/(np.sqrt(K))
error=sem_tau/mu

    
#Istogramma empirico
count, bins, _ = plt.hist(tau_c_samples, bins=15, density=True ,  alpha=0.5, color='skyblue', edgecolor='black', label='Dati')

#Gaussiana teorica
x = np.linspace(min(bins), max(bins), 1000)
pdf = norm.pdf(x, mu, sigma)


if error <0.05:
    print("K è sufficiente: errore relativo < 5%. Per questo set di parametri, tau_c=", mu)
else:
    print("K non è ancora sufficiente")

plt.plot(x, pdf, 'r--', linewidth=2, label=f'Fit Gaussiana\nμ={mu:.1f}, σ={sigma:.1f}')
plt.xlabel(r'$\tau_c$')
plt.ylabel('Densità di probabilità')
plt.title("Distribuzione di" r"$\tau_c$ con fit gaussiano")
plt.legend()
plt.show()






