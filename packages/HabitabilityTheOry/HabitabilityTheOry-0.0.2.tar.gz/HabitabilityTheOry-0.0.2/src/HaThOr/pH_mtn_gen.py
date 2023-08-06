# WARNING : HARDCODED PARAMETERS HERE - ONLY PERMEABILTY 

import numpy as np
import scipy.interpolate as scintr 
import pandas as pd

phdat = pd.read_csv('HaThOr/higgins_ph/pHint_optimal.csv')


# Let us assume:
perm =  10**(-10) # m/s, given by P.H personnal communication for realistic acidophile?
#rad = 1e-6 # m, corresponds to a 1 micrometer radius cell
#surf = 4*np.pi*rad**2

hpow = phdat['Power / (perm m^2)']*perm #*surf # In Watt per surface

#vol = (4/3)*np.pi*(rad*1e6)**3 # The formula requires vol in micromcube
#Bstruct = (1.8e-14)*vol**0.94
#spec_hrate = hpow # In Watt per cell /(GLF.Eana*Bstruct)

# Interpolate (not necessary here, but in Metabolisms, will serve to provide the maintenance function)
phr = scintr.interp1d(phdat['external pH'],hpow)