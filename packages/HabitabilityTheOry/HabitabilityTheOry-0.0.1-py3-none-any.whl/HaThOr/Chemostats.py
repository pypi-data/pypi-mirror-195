# Here, I intend to transfer the classes Chemostat and Population. 
# There, I also want to transfer the ecosystem solving routines from the ThermoEcoFast project.

import numpy as np
from scipy import optimize

class Chemostat:
    """
    Description of the chemostat environment with dilution rate
    D and input concentrations C0 (a dictionary)
    D is a dilution rate (s-1) # SHOULD IT NOT BE IN DAYS ???????
    F is the flux into and out of the chemostat (L/s or kg/s)
    V is the chemostat volume (L or kg)
    There must be D = F/V
    user must provide either only D or 2 of (D,F,V)
    """
    def __init__(self,C0,T,pH,D=None,F=None,V=None):
        nc = (D,F,V).count(None)
        assert nc!=3 and (D is not None) or (F is not None and V is not None)
        
        if nc==2 and D is not None:
            self.D = D
            self.F = None
            self.V = None
        
        elif nc == 1:
            if  D is None:
                self.D = F/V
                self.F = F
                self.V = V
            elif F is None:
                self.D = D
                self.V = V
                self.F = D*V
            elif V is None:
                self.D = D
                self.F = F
                self.V = F/D
        else:
            assert D ==F/V 
            self.D = D
            self.F = F
            self.V = V
                
        
        self.F = F # Flux   L/s
        self.V = V # Volume L
        self.C0 = C0 # Concentrations in the advected flux
        self.T  = T
        self.pH = pH
        self.C  = C0 # steady state if no chemistry/biology in the chemostat
        self.forced = False
        
        
    def is_habitable(self,organism):
        # The abiotic steady-state is C0
        return(organism.viable(self.T,self.pH,self.C))
    
    def outflux(self):
        """
        Returns the flux of chemical species in a dict with the same keys as in C
        ONLY POSSIBLE IF F IS GIVEN
        """
        return({k:self.F*self.C[k] for k in self.C.keys()})
        
    
        
    

class Population:
    
    # For now works with a chemostat with a single species
    
    def __init__(self,chemostat,organism=None):
        self.ftype  = organism # why default to None ?
        #self.bmass  = bmass # pop size in terms of biomass
        #self.popsize= bmass/organism.Bc
        self.chemostat = chemostat
        self.viable = self.chemostat.is_habitable(self.ftype)
        # Maybe we should calculate the quantities directly at instanciation?
    
    # Not useful if we are solving things analytically
    def net_growth_rate(self):
        return(self.bmass*self.organism.growthrate(T=self.chemostat.T,pH=self.chemostat.pH,
                                                   concentrations=self.chemostat.C))
    
    def conc_steady_state(self):
        Qstar = self.ftype.Qstar(self.chemostat.T,self.chemostat.pH)
        C = self.chemostat.C
        neD = self.ftype.metabolism.cat_reaction.eD
        keys = self.ftype.metabolism.cat_reaction.OK
        Stoi = self.ftype.metabolism.cat_reaction.S
        Y = {k:Stoi[k] for k in keys if Stoi[k]<0}#self.ftype.metabolism.cat_reaction.Y
        CeD0 = C[neD]
        if self.viable:
            
            def eq(CeD):
                return(Qstar - np.product(np.array([(C[k]-Stoi[k]*(CeD-CeD0))**(Stoi[k]) for k in keys])))

            infbd = np.max([CeD0+(1/Y[k])*C[k]+1e-10 for k in Y.keys()]+[1e-10]) #HOPEFULLY IT WORKS FOR A 1 COMPOUND REACTION
            if eq(CeD0)*eq(infbd) < 0 :
                eDsol = optimize.root_scalar(eq,bracket=[infbd,CeD0],method='brentq')
                converged = eDsol.converged
                eDstar = eDsol.root
                forced = True

            else: # This is a problem of no solution in the bounds - a nightmare -
                eDstar = CeD0
                converged = False
                forced = False
            success = converged
            
        else:
            success = True
            eDstar = CeD0
            forced = False
        Concstar = {k : Stoi[k]*(CeD0-eDstar)+C[k] for k in keys} # Need to add the concentrations that are not affected
        self.chemostat.forced = forced
        self.chemostat.C = Concstar
        return(Concstar,success)
    
    def cells_steady_state(self):
        if self.chemostat.forced:
            eD = self.ftype.metabolism.cat_reaction.eD
            ch = self.chemostat
            bstar = self.ftype.Bstar(self.chemostat.T,self.chemostat.pH,self.chemostat.C)
            nstar = (1/(bstar*self.ftype.catrate(ch.T)))*(ch.D*(ch.C0[eD]-ch.C[eD])) #to check, is cells
        else:
            nstar=0
            bstar = 0
        self.nstar = nstar
        self.bstar = bstar
        return(nstar,bstar*nstar)
    
    def steady_production(self):
        pstar = self.nstar*self.bstar*self.ftype.catrate(self.chemostat.T)
        self.pstar = pstar
        return(pstar) #this is molC/ the time units of the rates (should be days)