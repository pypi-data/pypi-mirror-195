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
opts.flux_type = 'model_flux'
fff = fff.Flux('KM','Numu_H3a+KM_E2.DAT',3)
Ind = np.array([0,0.5,1,1.5,2])
fig = plt.figure(figsize = (18,12))
opts.flux_type = 'stupid_ind'
a = fff.get_spectra_points(opts)
counts, bins = np.histogram(a, bins=np.logspace(np.log10(opts.energy_min),np.log10(opts.energy_max), 200))
plt.stairs(counts, bins,label = r'ind')
opts.flux_type = 'model_flux'
for i in range(len(Ind)):
    opts.flux_indicator= Ind[i]
    #a = 0
    a = fff.get_spectra_points(opts)
    counts, bins = np.histogram(a, bins=np.logspace(np.log10(opts.energy_min),np.log10(opts.energy_max), 200))
    #counts, bins = np.histogram(a, bins =200)
    plt.stairs(counts, bins,label = r'$\gamma$ = '+str(Ind[i]))
#plt.xscale('log')
plt.yscale('log')
plt.legend(fontsize = 15)
plt.grid(True)
plt.xlabel(r'$E_{\nu}$, GeV',fontsize = 20)
#plt.xlabel(r'$\log_{10}(E_{\nu}/GeV)$',fontsize = 20)


import importlib
path = importlib.util.find_spec('nupropagator').submodule_search_locations[0]
plt.savefig(path+'/flux/model_flux_log1.pdf')
plt.show()

