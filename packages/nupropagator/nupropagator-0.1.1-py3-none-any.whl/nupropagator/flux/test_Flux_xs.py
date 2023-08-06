import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import nupropagator.flux.Flux as fff
from types import SimpleNamespace

opts = SimpleNamespace()
opts.neutrinoPrimary_energy_mode = 'random'
opts.neutrinoPrimary_direction_mode = 'r'
opts.neutrinoPrimary_target_mode = 'random'
opts.neutrinoPrimary_current_mode = 'random'
opts.neutrinoPrimary_pdgid = 14
opts.neutrinoPrimary_pdf_model = 'CT10nlo'
opts.N_event = 1000000000
opts.vegas_neval = 1000
opts.flux_indicator = 1
opts.energy_min = 10
opts.energy_max = 10**8
opts.flux_type = 'flux_xs_data'
opts.N_protons = 10
opts.N_neutrons = 8
opts.neutrinoPrimary_pdf_model = 'CT10nlo'
opts.neutrinoPrimary_pdgid = 14


name = ['Numu_H3a+KM_E2.DAT']
model = ['H3a+KM']
color = ['k','g','r']
X = np.logspace(1,8,100)
Y = np.linspace(0,1,100)
x,y = np.meshgrid(X,Y)
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
x = np.log10(x)
y = y
i = 0
fff1 = fff.Flux('KM',name[i],3)
fff1.prepare_total_weight(opts)
a = fff1.get_rect_splain()
z1 = np.log10(fff1.total_weight([X,Y]))
z = np.log10(fff1.I3(Y, X))

ax.plot_wireframe(x,y,z, color=color[0],label= model[i])
ax.plot_wireframe(x,y,z1, color=color[1],label= 'with xs')
ax.set_xlabel(r'$\lg(E_{\nu}/GeV)$')
ax.set_ylabel(r'$\cos\theta$')
ax.set_zlabel(r'$\lg(F_{\nu}/cm^2/srad/s/GeV)$')
plt.legend()
fig.tight_layout()
plt.savefig('/home/vlad/flux_and_xs.pdf')
plt.show()


