import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nudisxs.disxs import *
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d
import math as m
import nupropagator.Global.Global as g
import vegas 
import nupropagator.cross_section.cross as cs

class Flux:
    def __init__(self, model_name, file, dim):
        import importlib
        path = importlib.util.find_spec('nupropagator').submodule_search_locations[0]
        df = pd.read_csv(path + '/flux/flux_data/' + str(file),header=None, sep ='\t')
        self.energy = []
        self.Ncos=11
        if dim == 2:
            self.Ncos=1
        self.NPoint=len(df)
        self.cos_theta = [1-float(j)/(self.Ncos-1.) for j in range(0,self.Ncos,1)]
        self.cos_theta1 = self.cos_theta[::-1] 
        self.flux = np.zeros((self.Ncos,self.NPoint))
        self.model_name = model_name
        self.dim=dim
        self.energy = np.array(df[0])
        for i in range(self.Ncos-1,-1,-1):
            self.flux[i]=np.array(df[i+1])/np.array(df[0])/np.array(df[0])
        return
    
    def prepare_total_weight(self,opts):
        self.N_p = opts.N_protons
        self.N_n = opts.N_neutrons
        model = opts.neutrinoPrimary_pdf_model
        flavor = opts.neutrinoPrimary_pdgid
        self.cs_p=cs.Cross_section(model=model,pdg=flavor,n_tt=2212)
        self.cs_n=cs.Cross_section(model=model,pdg=flavor,n_tt=2112)

    def flux_x(self,E):
        a=0
        for i in range(self.Ncos):
            a+=2*np.pi*self.flux[i]*0.1
        f = interp1d(self.energy, a, kind='cubic')
        return f(E)
    
    def get_3D_data_points(self):
        return self.flux
    
    def get_rect_splain(self):
        from scipy.interpolate import RectBivariateSpline
        E,cos = np.meshgrid(self.energy,self.cos_theta1)
        self.I3 = RectBivariateSpline(self.cos_theta1, self.energy, self.flux)
        return self.I3,E,cos
    
    @vegas.batchintegrand
    def get_vegas_flux(self,xx):
        z = self.I3(xx[:,1],xx[:,0],grid = False)
        return np.array(z)
   
    @vegas.batchintegrand
    def get_vegas_flux1(self,xx):
        z = (self.I3(xx[:,1],10**xx[:,0],grid = False))*10**xx[:,0]*np.log(10)
        return np.array(z)


    def total_weight(self,xx):
        return (self.N_n*self.cs_n.tot(xx[0])+self.N_p*self.cs_p.tot(xx[0]))*self.get_vegas_flux(xx)

    def get_spectra_points(self,opts):
        if opts.flux_type == 'flux_data':#Sinegovsky flux
            #self.integrator = vegas.Integrator([[self.energy.min(),self.energy.max()], [0,1]], nhcube_batch=2000, sync_ran=False)
            self.integrator = vegas.Integrator([[self.energy.min(),self.energy.max()], [0,1]])
            #self.integrator = vegas.Integrator([[np.log10(self.energy.min()),np.log10(self.energy.max())], [0,1]])
            self.result = self.integrator(self.get_vegas_flux, nitn = 10,neval = opts.vegas_neval)
            E = []
            cos = []
            weight = []
            flux = []
            integral = 0
            for x,wgt in self.integrator.random():
                E.append(x[0])
                cos.append(x[1])
                weight.append(wgt)
                flux.append(self.I3(x[1],x[0]))
                integral = integral + wgt*self.I3(x[1],x[0])
            E = np.array(E)
            cos = np.array(cos)
            weight = np.array(weight)
            flux = np.array(flux)
            print(flux[0])
            print('mean', integral)
            print('sp',np.shape(flux),np.shape(weight))
            self.mean = (weight*flux[:,0,0]).sum()
            return E,cos,weight,flux
        N_flux_number = int(np.ceil(opts.N_event/1000))
        eps = opts.energy_min/opts.energy_max
        if opts.flux_type == 'model_flux':#uniform
            g = opts.flux_indicator
            print('N',N_flux_number, g)
            if g == 1:
                E = np.random.random(N_flux_number)
                #print(E,g)
                E = opts.energy_min*(1/eps)**E
                return E
            if g != 1:
                E = np.random.random(N_flux_number)
                E = opts.energy_max*(eps**(1-g)+E*(1 - eps**(1-g)))**(1/(1-g))
                #print(E,g)
                return E
        if opts.flux_type =='stupid_ind':
            E = np.log10(opts.energy_min) -np.log10(eps)*np.random.random(N_flux_number)
            E = 10**(E) 
            return E
        if opts.flux_type == 'flux_xs_data':
            self.prepare_total_weight(opts)
            self.integrator = vegas.Integrator([[self.energy.min(),self.energy.max()], [0,1]], nhcube_batch=2000, sync_ran=False)
            
            result = self.integrator(self.total_weight, nitn = 10,neval = 1000)
            E = []
            cos = []
            weight = []
            flux = []
            for x,wgt in self.integrator.random():
                E.append(x[0])
                cos.append(x[1])
                weight.append(wgt)
                flux.append(self.total_weight(x))
            E = np.array(E)
            cos = np.array(cos)
            weight = np.array(weight)
            flux = np.array(flux)
            return E,cos,weight,flux











