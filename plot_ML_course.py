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

# standard modules
from matplotlib.pyplot import (figure, plot, title, legend, xlabel, ylabel, \
                               show, savefig, close, subplots)
from os.path import basename, splitext, join
from itertools import combinations    
from math import ceil, floor
import numpy as np

# print('test')



def subplot_all_combinations(X, y, 
                             classNames, 
                             plot_labels,
                             n_attributes, 
                             n_classes, 
                             fig_title = None):
    # M number of attributes / features
    # C number of classes

    # Iterate over all possible 2D combinations of attributes and saveplot
    combinations_ij     = list(combinations(range(n_attributes),2))
    n_combinations_ij   = len(list(combinations_ij))
    
    # Determine number of rows and columsn for subplot array
    # nrows, ncols    = 3, ceil(n_combinations_ij/3)
    nrows           = ceil(np.sqrt(n_combinations_ij))
    ncols           = floor(np.sqrt(n_combinations_ij))  

    # Initiate figure
    fig, axs        = subplots(nrows = nrows, ncols = ncols)#, sharex=True)
    # Each subplot is ca. 3x3
    fig.set_figwidth(ncols*3) #no need to determine height
    fig.set_figheight(nrows*3)
    # fig.subplots_adjust(wspace = 0, hspace=0.5)    
    
    # assign counter
    k = 0
    for combination in combinations_ij:
        i = combination[0]
        j = combination[1]
    
        # iterate through all classes and make a mask
        for c in range(n_classes):
            # select indices belonging to class c:
            # (returns an df with Booleans)
            class_mask      = (y['class']==c) 
            X_attribute_i   = X.iloc[:, i][class_mask] # masking a pandas dataframe
            X_attribute_j   = X.iloc[:, j][class_mask]
            # plot(X_attribute_i, X_attribute_j, 'o')
            axs.flatten()[k].plot(X_attribute_i, X_attribute_j, 'o', label = classNames[c])
            # axs.flatten()[k].set_aspect('equal')    
       
        axs.flatten()[k].set_xlabel(plot_labels[i])
        axs.flatten()[k].set_ylabel(plot_labels[j])
        k += 1   
    # add legend and use tight_layout
    axs[0,0].legend(bbox_to_anchor=(-1, 1), loc='upper left', borderaxespad=0.)
    fig.tight_layout() 
    show()
    
def save_figure_as_script_title(exerciseName, comment):
    """
    This function saves the 
    Parameters
    ----------
    exerciseName : str
        name of the script where the figure is plotted that will be used for
        the figure file title
    comment : str
        additional comment to add to the figure title.

    Returns
    -------
    None.

    """
    # Save figure in the 'figures' directory
    # close('all')    
    saveFigTitle    = exerciseName + '_' + comment
    saveFigPath     = join('../figures/',saveFigTitle)
    savefig(saveFigPath, dpi = 200)
    print('\'{}\' saved as figure'.format(saveFigTitle))      
    
    
         

