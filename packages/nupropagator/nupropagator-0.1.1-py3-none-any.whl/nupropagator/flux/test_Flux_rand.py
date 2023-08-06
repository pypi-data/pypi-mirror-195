import nupropagator.flux.Flux as fff
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from types import SimpleNamespace

opts = SimpleNamespace()
opts.neutrinoPrimary_energy_mode = 'random'
opts.neutrinoPrimary_direction_mode = 'r'
opts.neutrinoPrimary_target_mode = 'random'
opts.neutrinoPrimary_current_mode = 'random'
opts.neutrinoPrimary_pdgid = 14
opts.neutrinoPrimary_pdf_model = 'CT10nlo'
opts.N_event = 1000000000
opts.vegas_neval = 10000000
opts.flux_indicator = 1
opts.energy_min = 10
opts.energy_max = 10**8
opts.flux_type = 'flux_data'

N_E = 1000
N_cos = 1000
ff = np.zeros([N_E,N_cos])

fff = fff.Flux('KM','Numu_H3a+KM_E2.DAT',3)
fff.get_rect_splain()
a = fff.get_spectra_points(opts)
fig = plt.figure(figsize = (18,12))
X = np.log10(a[0])
Z = np.log10(a[3])
cos = fff.cos_theta
Y = a[1]
E = fff.energy
cos =  np.linspace(0,1,N_cos)
E = np.logspace(1,8,N_E)
print(fff.result.summary(extended = True,weighted = True))
#ff = fff.I3(cos,E)/np.array(fff.result.itn_results[-1].mean())
#print(ff,fff.mean,fff.mean*ff)
xx,yy = np.meshgrid(np.log10(E),cos)
H, xedges, yedges = np.histogram2d(X, Y, bins=[80, 100])
fig = plt.figure(figsize = (18,12))
ff = fff.I3(cos,E)/fff.mean*H.sum()/80
xpos, ypos = np.meshgrid(xedges[:-1] +(xedges[1]-xedges[0])/2, yedges[:-1] + (yedges[1]-yedges[0])/2, indexing="ij")
ax = fig.add_subplot(projection='3d')
ax.plot_wireframe(xpos,ypos,H, color='r')
ax.plot_wireframe(xx,yy,ff, color='g')
ax.set_xlabel(r'$\lg(E_{\nu}/GeV)$')
ax.set_ylabel(r'$\cos\theta$')
ax.set_zlabel(r'$\lg(F_{\nu}/cm^2/srad/s/GeV)$')
plt.savefig('/home/vlad/flux_vegas2d.pdf')
plt.show()
