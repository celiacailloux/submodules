#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# This modules contains functions for plotting using submodules
# 
# Tags: pyplot, subplots, all combinations
#
# @author: celiacailloux
# celiacailloux@gmail.com
# 
# Created on Mon Jan 25 2021
# ----------------------------------------------------------------------------

from matplotlib.pyplot import figure, plot, title, legend, xlabel, ylabel, \
    show, savefig, close, subplots
from itertools import combinations    

print('test')

def subplot_all_combinations():#M, title = None):
    print('test')
    # # M number of attributes / features

    # # Iterate over all possible 2D combinations of attributes and saveplot
    # combinations_ij     = list(combinations(range(M),2))
    # n_combinations_ij   = len(list(combinations_ij))
    
    # # Determine number of rows and columsn for subplot array
    # # nrows, ncols    = 3, ceil(n_combinations_ij/3)
    # nrows           = ceil(np.sqrt(n_combinations_ij))
    # ncols           = floor(np.sqrt(n_combinations_ij))  

    # # Initiate figure
    # fig, axs        = subplots(nrows = nrows, ncols = ncols)#, sharex=True)
    # # Each subplot is ca. 3x3
    # fig.set_figwidth(ncols*3) #no need to determine height
    # fig.set_figheight(nrows*3)
    # # fig.subplots_adjust(wspace = 0, hspace=0.5)    
