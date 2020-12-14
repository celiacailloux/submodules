# -*- coding: utf-8 -*-

''' --------------------------------------- '''
'''   Created on Thu Dec  5 08:44:11 2019   '''
'''                                         '''
'''    Updated Dec 04 2019                  '''
'''                                         '''
'''    @author: ceshuca                     '''
''' --------------------------------------  '''
from submodules import plot_misc as pltF

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors


# ---------------------- color lists
blue10_wulff = ['#000000','#1d616d','#1e707e','#1e7f8f','#1e8ea1','#1d9eb3','#1aaec5','#16bed8','#0eceeb','#00dfff']
blue10dark = ['#000000','#0b232b','#1e3842','#314f5a','#456773','#5a7f8d','#7099a9','#86b4c5','#9dcfe2','#b5ebff']
blue10 = ['#000000', '#003247', '#1c465c', '#335b71', '#497187', '#60879e', '#779eb6', '#8eb6cd', '#a6cfe6', '#bee8ff'] 
blue10darkest = ['#000000','#00405c','#1b4e6a','#2e5c79','#3f6a88','#4f7997','#6088a6','#7098b6','#81a8c6','#92b8d6']
# https://learnui.design/tools/data-color-picker.html#single
# ---------------------- color lists


def make_color_map_hex_to_rgb(color_list_hex = None, bpy = False, test_color_list = False):
    norm = matplotlib.colors.Normalize(-1,1)
    if  not color_list_hex:
        color_list_hex = ['#00425c', '#00586e', '#006e72', '#008265',
                         '#1b944c', '#6ea228', '#b4a900', '#ffa600']
    c_hex = []
    color_list_rgb  = []
    color_list_bpy_rgb = []
    for col in color_list_hex:
        color_list_rgb.append(matplotlib.colors.to_rgba(matplotlib.colors.to_hex(col)))
        c_hex.append(matplotlib.colors.to_hex(col))
        l = list(matplotlib.colors.to_rgb(col))
        l.append(1)
        color_list_bpy_rgb.append(tuple(l))
    #3print(color_list_rgb)
    #print(color_list_bpy_rgb)
    #print(c_hex)
    
    #print(color_list_rgb)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", color_list_rgb)
    
    if test_color_list:
        fig, ax=plt.subplots()
        x = np.arange(10)
        y = np.linspace(-1,1,10)
        sc = ax.scatter(x,y, c=y, norm=norm, cmap=cmap)
        fig.colorbar(sc, orientation="horizontal")
        plt.show()
    if bpy:    
        return color_list_bpy_rgb
    else:
        return cmap
# color from
# https://sciencenotes.org/molecule-atom-colors-cpk-colors/
C = ['#505050']
O = ['#FF0D0D']
H = ['#FFFFFF']
color_list_hex = H#blue10darkest                        
rgb = make_color_map_hex_to_rgb(color_list_hex, bpy = False )

def view_colormap(cmap, raw_file_path):
    """Plot a colormap with its grayscale equivalent"""
    # cmap = plt.cm.get_cmap(cmap)
    colors = cmap(np.arange(cmap.N))
    
    # cmap = grayscale_cmap(cmap)
    # grayscale = cmap(np.arange(cmap.N))
    
    fig, ax = plt.subplots(1, figsize=(6, 2),
                           subplot_kw=dict(xticks=[], yticks=[]))
    ax.imshow([colors], extent=[0, 10, 0, 1])
    
    pltF.GCPE_savecolorbar(fig, raw_file_path)
    # ax[1].imshow([grayscale], extent=[0, 10, 0, 1])
    




                         