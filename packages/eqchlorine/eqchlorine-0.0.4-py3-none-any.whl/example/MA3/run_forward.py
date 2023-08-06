# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:47:42 2022

@author: Maureen Llinares
"""
import geometric_scaling_factors
import cl36_concentration as cl36
import parameters
from constants import constants
from seismic_scenario import seismic_scenario

import matplotlib.pyplot as plt
import numpy as np


param = parameters.param() # import site parameters

""" First calculate scaling factors """
depth_rock, depth_coll, surf_rock, S_S = geometric_scaling_factors.neutron_scaling(param, constants, len(seismic_scenario['ages']))


""" Then calculate 36Cl concentration due to long term history """
cl36_long_term, h_longterm = cl36.long_term(param, constants, seismic_scenario, scaling_factors)

""" Seismic phase """
synthetic_production, height, out = cl36.cl36_seismic_sequence(param, constants, seismic_scenario, scaling_factors, cl36_long_term)
toc3=time.time()


""" Plotting results """

plt.figure(figsize=(6, 8))
plt.subplot(2,1,1)
plt.title('Long-term')
plt.plot(cl36_long_term, h_longterm*1e-2, color = 'steelblue', linestyle='', marker='.')
plt.xlabel ('36Cl [at/g]')
plt.ylabel ('Height (m)')



plt.subplot(2, 1, 2)
measured_production = param.cl36AMS
plt.title('Final')
plt.plot(synthetic_production, height*1e-2, color = 'cornflowerblue', linestyle='', marker='.', label='synthetic')
plt.plot(measured_production, height*1e-2, color = 'black', linestyle='', marker='.', label='measured')
plt.xlabel ('36Cl [at/g]')
plt.ylabel ('Height (m)')
plt.legend()
plt.tight_layout()

np.savetxt('results.txt', synthetic_production) # saving results under .txt file
plt.savefig('plot.png', dpi=500) # saving plot
