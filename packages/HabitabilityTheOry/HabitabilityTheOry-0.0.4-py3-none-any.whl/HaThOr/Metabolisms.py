### Nmotes and to-dos

## A problem with the heterotroph predators modelling is the Keq parameter... how does it connect with enzymes ??

import numpy as np


#import HaThOr.pH_mtn_gen as pHrate # This is to add the pH calculations, future work using the results from P. Higgins


R     = 8.314             # Perfect gas constant J/mol/K
TS    = 298               # Standard temperature


def Dgdiss(NoC,gamma):
    """
    Returns the dissipaed energy during metabolism from Kleerebezem 2010

    Arguments
    ------------------------------------
    NoC : int
        length of carbon source chain
    gamma : int
        oxydation level of carbon in carbon source
    """
    return((200 + 18*(6 - NoC)**1.8 + np.exp((((-0.2 - gamma)**2)**(0.16))*(3.6 + 0.4*NoC)))*1000)
    
class Metabolism:
    
    """
    This class could be called metabolism since the anabolic energy is parameterized, but the day the anabolic energy will be better calculated there will be an explicit metabolism class
    """
    
    def __init__(self,reaction,autotrophy=True,strong_ed=True,NoC=None,gamma=None):
        """
        If the anabolism is autotrophic, then there is two options:
        - strong electron donor (eg H2, organic carbon, reduced S), RET is not required
        - weak electron donor (N and Fe based), RET is required
        
        If the carbon source is organic, then the dissipation energy is calculated using a funciton of the carbon chain length NoC and carbon degree of oxidation gamma
        """
        self.cat_reaction = reaction
        if autotrophy:
            if strong_ed:
                self.Eana = 1e6
            else:
                self.Eana = 3.5e6
        else:
            self.Eana = Dgdiss(NoC=NoC,gamma=gamma)
    
    def catyield(self,T,pH,concentrations):
        return(-self.cat_reaction.DeltaG(T,pH,concentrations)/self.Eana)
    
            
class Organism:
    
    
    def __init__(self,metabolism,A,tau,DGac,DGam,d=0,s=1e-6,rmax=50,theta=10,name=None):
        self.name = name
        self.metabolism = metabolism
        self.A = A
        self.tau = tau
        self.DGac = DGac
        self.DGam = DGam
        self.d = d
        self.s = s # cell diameter in meters
        self.V = (4/3)*np.pi*(self.s/2)**3
        self.Srf = 4*np.pi*self.s**2 # In m2
        self.Bs = 18*self.V**(0.94) #Power law from Sauterey et al 2020, in molC
        self.Bc = self.Bs # cellular biomass
        self.theta = theta # sensitivity parameter
        self.rmax  = rmax # 50 is in d-1 for methanogens, the absolute max max; see the biomass paper
        
        # in the future
        #self.pHrate = lambda pH : pHrate.phr(pH)*self.Srf/(self.Bc*self.metabolism.Eana) # Be careful, that is an interpolated function
        
        
    def catrate(self,T):
        return(self.A*self.tau*np.exp(-self.DGac/(R*T)))
    
    def molecular_maintrate(self,T): # This is the rate of molecules that are lost and need to be replaced.
        return(self.A*np.exp(-self.DGam/(R*T)))
    
    ## Here, we should add the pH maintenance calculations from Higgins.
    
    def maintrate(self,T,pH):
        return(self.molecular_maintrate(T)) #+self.pHrate(pH)) in the future
    
    def growthrate(self,T,pH,concentrations):
        lam = self.metabolism.catyield(T,pH,concentrations)
        kg  = lam*self.catrate(T) - self.maintrate(T,pH)
        return(kg)
    
    def DeltaGstar(self,T,pH):
        """
        Actually DGstar
        """
        return(-self.metabolism.Eana*(self.maintrate(T,pH)+self.d)/self.catrate(T))
    
    def Qstar(self,T,pH):
        # Be careful that dgstar is actually -dgstar
        return(np.exp((-1/(R*T))*(self.metabolism.cat_reaction.DeltaG0(T,pH)-self.DeltaGstar(T,pH))))
    
    def viable(self,T,pH,concentrations):
        # An alternative
        #return(self.growthrate(concentrations,T)>0)
        # DGstar is calculated positive actually
        return(self.metabolism.cat_reaction.DeltaG(T,pH,concentrations)<self.DeltaGstar(T,pH))
    
    def Bstar(self,T,pH,concentrations):
        """
        Returns the internal biomass equilibrium (it is really only useful if we want the number of cells)

        Arguments
        ----------------------
        qana : float
            anabolic rate per unit of biomass (molC/molC.day)
        bstruct : float
            internal biomass quantity (molC)
        rmax : float
            maximal division rate (d-1)
        theta : integer
            steepness of division function parameter

        Returns
        -----------------------
        bstar : float
            internal biomass at equilibrium (molC)
        """
        qana = self.growthrate(T,pH,concentrations)
        if qana == 0:
            bstar = 2*self.Bs
        elif qana < 0:
            bstar = 0
        else:
            bstar = self.Bs*((np.divide(self.rmax,qana)-1)**(-(1/self.theta))+2)
        return(bstar)
        
        