# -*- coding: utf-8 -*-

''' --------------------------------------- '''
'''   Created on Thu Dec  5 08:44:11 2019   '''
'''                                         '''
'''    Updated Dec 04 2019                  '''
'''                                         '''
'''    @author: ceshuca                     '''
''' --------------------------------------  '''

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors

norm = matplotlib.colors.Normalize(-1,1)

color_list_hex = ['#00425c', '#00586e', '#006e72', '#008265',
                         '#1b944c', '#6ea228', '#b4a900', '#ffa600']
color_list_rgb  = []
colors = []
for col in color_list_hex:
    color_list_rgb.append(matplotlib.colors.to_rgb(col))
print(color_list_rgb)

#colors = [[norm(-1.0), "darkblue"],
#          [norm(-0.6), "lightgrey"],
#          [norm( 0.6), "lightgrey"],
#          [norm( 1.0), "red"]]
#
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", color_list_rgb)


fig, ax=plt.subplots()
x = np.arange(10)
y = np.linspace(-1,1,10)
sc = ax.scatter(x,y, c=y, norm=norm, cmap=cmap)
fig.colorbar(sc, orientation="horizontal")
plt.show()

#    elif color_map == 'darkbluegreenyellow':
#        color = [
#                