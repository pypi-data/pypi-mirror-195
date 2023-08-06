from types import SimpleNamespace
opts = SimpleNamespace()
opts.neutrinoPrimary_energy_mode = 'random'
opts.neutrinoPrimary_direction_mode = 'r'
opts.neutrinoPrimary_target_mode = 'random'
opts.neutrinoPrimary_current_mode = 'random'
opts.neutrinoPrimary_pdgid = 14
opts.neutrinoPrimary_pdf_model = 'CT10nlo'
opts.N_event = 1
opts.vegas_neval = 1000 
import time as time
import nupropagator.nugen as  nugen
import numpy as np
import nupropagator.NuPropagator as nuprop
import nupropagator.Global.Global as g
nu = nugen.NuGen()
#M = np.array([1,10]) 
M = np.array([1,10,100,1000,3000,7000,10000]) 
nuprop = nuprop.NuPropagator(opts)
print('start')
#N = len(nuprop.spectra[0])
N = 10
tt1 = np.zeros(N)
tt2 = np.zeros(N)
tt1_t = np.zeros(len(M))
tt2_t = np.zeros(len(M))
n1 = 0
n2 = 0

nuprop.set_final_vertex(np.array([0,0,g.R_E - 1000]))
for m in range(len(M)):
    for i in range(N):
        #print('EVENT ', i)
        print(m,i)
        nuprop.set_event_number(i)
        info_drag = nuprop.get_dragging()
        opts.neutrinoPrimary_energy_GeV = info_drag[1] 
        opts.neutrinoPrimary_direction = info_drag[2]
        tt1[i] = time.time()
        opts.N_event = 1
        for k in range(M[m]):
            n1 = nu.get_event(opts)# 0.03s per event
        tt1[i] = (time.time()-tt1[i])/M[m]
        tt2[i] = time.time()
        if M[m]>=1000:
            opts.vegas_neval = M[m]
        opts.N_event = 1000
        n2 = nu.get_event_fix_en(opts)# 0.17s per 1000 event
        tt2[i] = (time.time()-tt2[i])/opts.N_event
    tt1_t[m] = tt1.mean()
    tt2_t[m] = tt2.mean()
import matplotlib.pyplot as plt
fig = plt.figure(figsize = (18,12))
plt.scatter(M,tt1_t, label = 'monocall')
plt.scatter(M,tt2_t,label ='multicall')
plt.xscale('log')
plt.xlabel('number of events')
plt.ylabel('CPU time, s')
plt.grid(True)
plt.legend()
plt.savefig('/home/vlad/CPU_time.pdf')
plt.show()
