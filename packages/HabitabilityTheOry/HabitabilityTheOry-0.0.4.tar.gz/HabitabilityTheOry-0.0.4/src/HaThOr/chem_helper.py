# Here, we get the functions that do some good ol' simple chemical stuff for us, and we also have some chemical data

import numpy as np

R     = 8.314             # ideal gas constant J/mol/K
TS    = 298               # Standard temperature
T0    = 273.15            #useful to convert to C

l10 = np.log(10)

## Henry law parameters Ci/Pi
aH = 7.8e-4
aC = lambda T : np.exp(9345.17/T-167.8108+23.3585*np.log(T)+(0.023517-2.3656e-4*T+4.7036e-7*T**2)*35.0) #solubility of CO2 from Sauterey 2020
aG = 1.4e-3
Henry_data = {'H2':lambda T : aH,'DIC': aC, 'CH4':lambda T : aG} # It is written DIC for convenience but it is actually aqueous CO2

# Dissociation constants/functions
# dissociation of DIC = [CO2aq] + [HCO3-] + [CO3--]
k1 = lambda T : 10**-((-1.1e-4*((T-273.15)**2) + 0.012*(T-273.15) - 6.58)* -1)   # CO2aq <=> HCO3- + H+ K1 = [H+][HCO3-]/[CO2aq]
k2 = lambda T : 10**-((-9.0e-5*((T-273.15)**2) + 0.0137*(T-273.15) - 10.62)* -1) # HCO3- + H+ <=> CO3-- K2 = [CO3--]/[H+][HCO3-]
# dissociation of DIN = [NH3] + [NH4+]
ka = lambda T : 10**-(0.09108+(2729.92/T)) # Ka = [H+][NH3]/[NH4+]

acorr = lambda T,Y,Kh : -R*T*np.sum(Y*np.log(Kh)) # aqueous correction Kh is the vector containing the Henry parameters Ci/Pi


hydrogenotrophy_dat = {'S':{'H2':-1,'DIC':-0.25,'CH4':0.25},'DG0S':-32575,'DH0S':-63175,'eD':'H2','Hp':0}
acetotrophy_dat     = {'S':{'DIC':1,'CH4':1,'CH3COOH':-1},'DG0S':-55000,'DH0S':16200,'eD':'CH3COOH','Hp':0} #Not sure if should be CH3COO- Provided by B. Sauterey
methanotrophy_dat   = {'S':{'CH4':-1,'H2SO4':-1,'H2S':1,'DIC':1},'DG0S':-107000,'DH0S':-1800,'eD':'CH4','Hp':0} # provided by B. Sauterey
acetogeny_dat       = {'S':{'CO':-1,'CH3COOH':1,'DIC':2},'DG0S':-77900,'DH0S':-129900,'eD':'CO','Hp':0} # provided by B. Sauterey
glyFermentation_dat  = {'S':{'Gly':-1,'CH3COOH':1,'DIN':1,'DIC':1,'H2':0.5},'DG0S':-5781,'DH0S':17400,'eD':'Gly','Hp':0.5,'NoC':2,'gamma':1} # Should be CH3COO- but since its dissociation is not implemented yet I let is as CH3COOH. Provided by L. Molares Moncayo

#predation_dat       = {'S':{'H2':4/6,'CO2':2/6,'CH3COOH':2/6,'X':-1},'DG':-212e3,'eD':'X'} # Elaborate thermodynamics of heterotrophy

def DIC_correction(T,Hp):
    # Corrects DIC in HCO3- NOT anything else
    K1 = k1(T)
    K2 = k2(T)
    return(R*T*(np.log(K1*Hp/(K1*Hp+Hp**2+K1*K2))))

def DIN_correction(T,Hp):
    KA = ka(T)
    return(-R*T*np.log(1+KA/Hp))

def AmmFromDIN(T,Hp,DIN):
    return(DIN/(1+ka(T)/Hp))

def HCO3FromDIC(T,Hp,DIC):
    return(DIC/(1+Hp/k1(T)+k2(T)/Hp))

def CO3FromDIC(T,Hp,DIC):
    return(k2(T)*HCO3FromDIC(T,Hp,DIC)/Hp)

def pH_correction(T,Hp,Yh):
    return(Yh*R*T*np.log(Hp))


def SolutionCorrection(T,Y,okeys):
    """
    wrapper for "vectorization" for T and ensure that the keys are well ordered and all
    """
    if isinstance(T,(np.ndarray)):
        #can be optimized as a vector version of the Henry coefficient function could be produced
        correction = np.array([acorr(T[i],Y=self.Y,Kh=np.array([Henry_data[k](T) for k in self.OK])) for i in range(len(T))])
    else :
        Kh = np.array([Henry_data[k](T) for k in okeys])
        correction = acorr(T,Y=Y,Kh=Kh)
    return(correction)
 

def basicDG0(T,DG0S,DH0S):
    """
    Provides a basic calculation of DG0 in simple cases

    Arguments
    ---------------
    T       : float
           absolute temperature (K)
    DG0S/DH0S are the standard gibbs free energy and enthalpy of the reaction
    """ 

    DG0 = DG0S*(T/TS) + DH0S*((TS-T)/TS)
    return(DG0)

methOK = np.array(['H2']+[k for k in hydrogenotrophy_dat["S"].keys() if k!= ['H2']])# ordered keys 
methY = np.array([hydrogenotrophy_dat['S'][k] for k in methOK])

def methanogenDG0(T,pH):
    DG0 = basicDG0(T,hydrogenotrophy_dat['DG0S'],hydrogenotrophy_dat['DH0S'])
    DG0 += SolutionCorrection(T,methY,methOK)
    return(DG0)

def GlyFDG0(T,pH):
    DG0 = basicDG0(T,glyFermentation_dat['DG0S'],glyFermentation_dat['DH0S'])
    Hp = 10**-pH
    DG0 += DIN_correction(T,Hp)
    DG0 += DIC_correction(T,Hp)
    DG0 += pH_correction(T,Hp,Yh=glyFermentation_dat['Hp'])
    return(DG0)

hydrogenotrophy_dat['DeltaG0']=methanogenDG0
glyFermentation_dat['DeltaG0'] = GlyFDG0

class Reaction:
    
    def __init__(self,S,eD,DeltaG0=None,DG0S=None,DH0S=None,name=None,**kwargs):
        self.name = name
        self.S = S # dictionnary containing the chemical species as keys and the stoichiometry as values
        if DeltaG0 is None:
            assert DG0S is not None and DH0S is not None
            self.DeltaG0 = lambda T,pH : basicDG0(T,DG0S=DG0S,DH0S=DH0S)
        else:
            self.DeltaG0 = DeltaG0 # Function of T,pH that returns the DG0
        self.name = name # reaction name
        self.eD = eD # Name of the electron donor
        # In the case where DG0S and DH0s are given in the gas phase and the reaction occurs in the aqueous phase, a correction needs to be made
        self.OK = np.array([self.eD]+[k for k in self.S.keys() if k!= self.eD])# ordered keys 
        self.Y = np.array([self.S[k] for k in self.OK])
    
    
    def ReactionQuotient(self,concentrations):
        """
        Concentrations as a dictionary
        """
        return(np.product([concentrations[k]**self.S[k] for k in self.S.keys()]))
    
    def DeltaG(self,T,pH,concentrations):
        
        Q = self.ReactionQuotient(concentrations)
        return(self.DeltaG0(T,pH)+R*T*np.log(Q))