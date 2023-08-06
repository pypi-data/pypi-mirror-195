import numpy as np
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import nupropagator.flux.Flux as fff
name = ['Numu_H3a+KM_E2.DAT','Numu_H3a+QGS_E2.dat','Numu_H3a+SIBYLL_E2.dat']
model = ['H3a+KM','H3a+QGS','H3a+SIBYLL']
color = ['k','g','r']
X = np.logspace(1,8,100)
Y = np.linspace(0,1,100)
x,y = np.meshgrid(X,Y)
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
x = np.log10(x)
y = y
for i in range(len(name)): 
    fff1 = fff.Flux('KM',name[i],3)
    a = fff1.get_rect_splain()
    z = np.log10(fff1.I3(Y, X))
    ax.plot_wireframe(x,y,z, color=color[i],label= model[i])
ax.set_xlabel(r'lg(E_{\nu}/GeV)')
ax.set_ylabel(r'\cos\theta')
ax.set_zlabel(r'$\lg(F_{\nu}/cm^2/srad/s/GeV)$')
plt.legend()
fig.tight_layout()
plt.savefig('/home/vlad/flux_intepol.pdf')
plt.show()

