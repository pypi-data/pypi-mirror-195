import numpy as np
import plotly.graph_objects as go
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
i = 0
fff1 = fff.Flux('KM',name[i],3)
a = fff1.get_rect_splain()
z = np.log10(fff1.I3(Y, X))

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])

fig.update_layout(title=model[i], autosize=False,
                  width=1000, height=1000,
                  margin=dict(l=65, r=50, b=65, t=90))

fig.show()

