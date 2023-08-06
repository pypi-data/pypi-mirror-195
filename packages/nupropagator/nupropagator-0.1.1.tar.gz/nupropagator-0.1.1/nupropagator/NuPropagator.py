import matplotlib
#from nudisxs.disxs import *
from nupropagator.Global.pdg_constants import *
import matplotlib.pyplot as plt
import nupropagator.earth.Earth as Earth
import nupropagator.flux.Flux as flux
import nupropagator.cross_section.cross as xs
import nupropagator.Global.Global as g
import numpy as np
import time as time
#import zf as zfactor

mag =  lambda x: np.sqrt(np.sum(x**2))

class NuPropagator:
    def __init__(self,opts):
        self.r = 1
        N = 8
        Z = 10 
        print('Propogator is ready')
        self.flux = flux.Flux('KM','Numu_H3a+KM_E2.DAT',3)
        self.earth=Earth.Earth(self.r,'PREM',N,Z)
        self.Z = Z
        self.N = N
        self.i = 0
        flavor = opts.neutrinoPrimary_pdgid
        model = opts.neutrinoPrimary_pdf_model
        self.xs_p=xs.Cross_section(model=model,pdg=flavor,n_tt=2212)
        self.xs_n=xs.Cross_section(model=model,pdg=flavor,n_tt=2112)
        self.spectra = self.flux.get_spectra_points()

    def set_final_vertex(self,fvertex):
        self.fvertex = fvertex

    def set_event_number(self,i):
        self.i = i
    
    def prepare_propagation(self,i):
        #self.zfactor=zfactor.zf()
        self.set_event_number(i)
        self.energy = self.spectra[0][self.i]
        phi = np.random.random()
        cos = self.spectra[1][self.i]
        sin = (1-cos**2)**0.5
        self.n = np.array([np.cos(phi)*sin,np.sin(phi)*sin,cos])
        scalar = np.sum(self.fvertex*self.n)
        self.ivertex  = self.fvertex-self.n*(scalar+np.sqrt(scalar**2 - np.sum(self.fvertex**2)+g.R_E**2))

    
    def probability(self,v1,v2,energy,N):            
        dep=self.earth.column_depth_vegas(v1,v2,N)
        self.depth=dep[0]
        self.flux = self.spectra[2][self.i] 
        self.weight = self.spectra[3][self.i] 
        #self.zf=self.zfactor.f(g.g*dep/g.cm**2,energy)
        prob = -(self.Z*self.xs_p.tot(energy)+self.N*self.xs_n.tot(energy))
        prob = np.exp(prob/(self.Z+self.N)*g.N_A*self.depth/g.g)
        prob_zf = 0
        #prob_zf=np.exp(-(self.Z*self.xs_p.tot(energy)+self.N*self.xs_n.tot(energy))
        #prob_zf = prob_zf/(self.Z+self.N)*(1-self.zf)*g.N_A*self.depth/g.g)
        return prob_zf,self.energy, self.n, self.flux,self.weight

    def get_dragging(self):
        self.prepare_propagation(self.i)
        info = self.probability(self.ivertex,self.fvertex,self.energy,N = 1000)
        self.set_event_number(self.i+1)
        return info
