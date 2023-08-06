import numpy as np
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import nupropagator.flux.Flux as fff
name = ['Numu_H3a+KM_E2.DAT','Numu_H3a+QGS_E2.dat','Numu_H3a+SIBYLL_E2.dat']
model = ['H3a+KM','H3a+QGS','H3a+SIBYLL']
color = ['k','g','r']
E = np.logspace(1,8,8)
cos = np.linspace(0,1,100)
for j in range(len(E)):
    fig = plt.figure(figsize = (18,12)) 
    for i in range(len(name)): 
        fff1 = fff.Flux('KM',name[i],3)
        a = fff1.get_rect_splain()
        z = np.log10(fff1.I3(cos, E[j]))
        plt.plot(cos,z,label = model[i])
    plt.title(r'$(E_{\nu}$ = '+str('{:.2E}'.format(E[j]))+' GeV)')
    plt.xlabel(r'\cos\theta')
    #plt.yscale('log')
    plt.ylabel(r'$\lg(F_{\nu}/cm^2/srad/s/GeV$)')
    plt.legend()
    plt.savefig('/home/vlad/flux_slice_E='+str('{:.2E}'.format(E[j]))+'GeV.pdf')
    plt.show()

