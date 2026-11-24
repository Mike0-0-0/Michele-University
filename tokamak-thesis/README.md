# Tokamak Diffusion Simulation (Bachelor's Thesis)
Inside the Tokamak, plasma dynamics are primarily governed by collective motions and non-diffusive behaviors. Within this context, this thesis aims to study, through numerical  
simulation, plasma behavior under a specific confinement regime known as L-mode (low confinement). This regime marks the point where plasma deviates from classical diffusive
behavior and is instead governed by the typical dynamics of self-organized systems. To this end, the problem was generalized and described through the definition of a 1
dimensional cellular automaton, which reproduces the salient features of the  self-organized systems. 


This project models plasma confinement and diffusion processes in a Tokamak device using a 1-dimensional cellular automaton (L-mode regime simulation), structured across three sequential stages.

### Stages Description
1. **First Stage (`TokaThesis-1.py`):** Implements the core running sandpile simulation. It injects a tracked particle into the lattice, handles instability thresholds and avalanche
propagation, and monitors system relaxation toward Self-Organized Criticality (SOC) by tracking grid mass and activity.
3. **Second Stage (`TokaThesis-2.py`):** Performs statistical analysis on the particle confinement times ($\tau_c$). It computes the mean and standard error over multiple runs ($K=100$) and fits an empirical Gaussian distribution to validate statistical sufficiency.
4. **Third Stage (`TokaThesis-3.py`):** Analyzes the scaling behavior of confinement time ($\tau_c$) as a function of the injection probability ($P_0$), applying a power-law curve fit to evaluate the physical dependency.
