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
opts.vegas_neval = 1000
opts.flux_indicator = 1
opts.energy_min = 10
opts.energy_max = 10**8
opts.flux_type = 'flux_xs_data'
opts.N_protons = 10
opts.N_neutrons = 8
opts.neutrinoPrimary_pdf_model = 'CT10nlo'
opts.neutrinoPrimary_pdgid = 14


N_E = 1000
N_cos = 1000
ff = np.zeros([N_E,N_cos])

fff = fff.Flux('KM','Numu_H3a+KM_E2.DAT',3)
fff.get_rect_splain()
a = fff.get_spectra_points(opts)

fig = plt.figure(figsize = (18,12))
X = np.log10(a[0])
Z = np.log10(a[3])
Y = a[1]
E = fff.energy
cos = fff.cos_theta
ax = fig.add_subplot(projection='3d')
ax.scatter(X,Y,Z,s = 0.5)
x = np.log10(np.logspace(1,8,N_E))
y = np.linspace(0,1,N_cos)
ff = fff.I3(10**x,y)
z = np.log10(ff)
ax.set_xlabel(r'$\lg(E_{\nu}/GeV)$')
ax.set_ylabel(r'$\cos\theta$')
ax.set_zlabel(r'$\lg(F_{\nu}/cm^2/srad/s/GeV)$')
plt.savefig('/home/vlad/flux_xs_vegas.pdf')
plt.show()
