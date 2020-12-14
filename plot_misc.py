#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 12:43:58 2019

@author: celiacailloux
"""
from submodules import file_manage_misc as OSfunc
from submodules import plot_colors

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os
from datetime import date
from scipy.integrate import trapz
from matplotlib.ticker import AutoMinorLocator, AutoLocator, MultipleLocator, \
    LogLocator, SymmetricalLogLocator,FormatStrFormatter,  ScalarFormatter

import math

" ___________________________________________________________ GLOBAL SETTINGS "

def color_maps(color_map = None):
    if color_map == 'greenblue':
        color = plt.get_cmap('ocean') 
    elif color_map == 'ocean':
        color = plt.get_cmap('ocean')
    elif color_map == 'blackbluegreen':
        color = plt.get_cmap('gist_earth')    
    elif color_map == 'terrain':
        color = plt.get_cmap('terrain') 
    elif color_map == 'Pastel1':
        color = plt.get_cmap('Pastel1') 
    elif color_map == 'cubehelix':
        color = plt.get_cmap('cubehelix') 
    elif color_map == 'color_coded':
        color = plt.get_cmap('tab20c')
    elif color_map == 'tab10':
        color = plt.get_cmap('tab10')
    elif color_map == 'jkib':
        color_list_hex = ['#0675a1','#0086a7','#00969d','#00a383','#28ad5e','#7ab332','#bcb100','#ffa600']
        color = make_color_map_hex_to_rgb( color_list_hex =  color_list_hex, test_color_list = False)
    elif color_map == 'inv_jkib':
        color_list_hex = ['#0675a1','#0086a7','#00969d','#00a383','#28ad5e','#7ab332','#bcb100','#ffa600']
        color = make_color_map_hex_to_rgb( color_list_hex = color_list_hex[::-1], test_color_list = False)
    elif color_map == 'FE_gb':
        color_list_hex = ['#5fb35b', '#4ac195', '#5ecbc2', '#8ed1dc', '#5993ad', '#32597a', '#172345']
        color = make_color_map_hex_to_rgb( color_list_hex = color_list_hex[::-1], test_color_list = False)
        # https://learnui.design/tools/data-color-picker.html#divergent
    else:
        print('color map not recognized (see module: PlottingFunctions)')
        color = make_color_map_hex_to_rgb['b', 'g','r','c','m','y','k']
    return color

def markers():
    return ['o', '^','D', 'X']

def global_settings(ax):
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)
        
    ax.tick_params(which = 'major',direction='inout', length=12, width=2, labelsize = 14)
    ax.tick_params(which = 'minor',direction='in', length=4, width = 1.2, labelsize = 14)
    
def global_minor_locator(ax, x_locator, y_locator):
    #if x_locator != 0 or y_locator = 0:
    if y_locator and x_locator is None:
        ax.yaxis.set_minor_locator(AutoMinorLocator(y_locator))          
    elif x_locator and y_locator is None:
        ax.xaxis.set_minor_locator(AutoMinorLocator(x_locator))
    else:
        ax.xaxis.set_minor_locator(AutoMinorLocator(x_locator))
        ax.yaxis.set_minor_locator(AutoMinorLocator(y_locator))  
    
def global_mayor_xlocator(ax, x_locator):
    ax.xaxis.set_major_locator(MultipleLocator(x_locator))

def global_mayor_ylocator(ax, y_locator):
    ax.yaxis.set_major_locator(MultipleLocator(y_locator))
        
def global_mayor_locator_auto(ax):
    ax.xaxis.set_major_locator(plt.AutoLocator())
    ax.yaxis.set_major_locator(plt.AutoLocator())

def global_lim(ax, x_lim, y_lim):
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    
def global_savefig(fig, plt_title, subdirectory = None, addcomment = None):
    directory = 'Figures'
    OSfunc.create_directory(directory)
    #save_title = directory + '/' + plt_title + '_' + addcomment
    if subdirectory:  
        OSfunc.create_directory(directory+ '/' + subdirectory)
        if addcomment:
            save_title = directory + '/' + subdirectory + '/' + plt_title + ', ' + addcomment
        else:
            save_title = directory + '/' + subdirectory + '/' + plt_title
    else:
        if addcomment:
            save_title = directory + '/' + plt_title + ', ' + addcomment
        else:
            save_title = directory + '/' + plt_title        
    #fig.savefig(save_title + '.png',bbox_inches='tight', dpi=200)
    #fig.set_size_inches(6, 4)
    fig.savefig(save_title + '.png',bbox_inches='tight', dpi=150)

def global_legendbox(ax, location = 'upper left', loc = 'to right' ):
    if loc == 'bottom':
        ax.legend(loc=location, fontsize = 14, bbox_to_anchor=(0, -0.15))
    elif loc == 'right':
        ax.legend(loc='upper left', fontsize = 16, bbox_to_anchor=(1.2, 1))
    elif loc == 'outside right':
        ax.legend(loc='upper left', fontsize = 14, bbox_to_anchor=(1.3, 0.5))
    elif loc == 'GC peak plotting':   
        leg = ax.legend(loc='upper left', fontsize = 14, bbox_to_anchor=(1.3, 2.35))
        for line in leg.get_lines():
            line.set_linewidth(8.0) 
        
        # ax.legend(loc=location, fontsize = 14, bbox_to_anchor=(xbox, ybox))
    
def global_exp_details(ax, exp_details_box, title = None, details_type = None):
    #trans = ax.get_xaxis_transform()
    if details_type is None:
        if title:
            details = title
            print('NOT NONE')
        else:
            details = ''
        
        for detail in exp_details_box:
            details += '\n' + str(detail)
    elif details_type == 'dict':
        for exp, exp_details in exp_details_box.items():
            details = exp + '\n' + str(exp_details)
        details + '** new exp'

    
    ax.annotate(details,xy=(0,-.15), xytext = (0,-.3), 
                    bbox=dict(boxstyle="square", fc="w"), 
                    horizontalalignment='left',verticalalignment='top', 
                    xycoords='axes fraction')   
    
def area_under_curve(x,y, stepsize,baseline = None):
    area_all = trapz(y, x=x, dx=stepsize)
    if baseline is None:
        AUC = np.abs(area_all) #area under curve 
    else:
        ytrapz = np.full_like(y, baseline)
        area_baseline = trapz(ytrapz,x=x, dx=stepsize)
        AUC = np.abs(area_all)-np.abs(area_baseline) #area under curve
    return round(AUC,0)


def global_annotation(ax, text_title, text_list = '', pos = 1):
    if pos == 1:
        xy = (0,-0.2)
        text = text_title #+ '\n' + str(text_list)
        ax.annotate(text,xy, xytext = xy, 
                            bbox=dict(boxstyle="square", fc="w"), 
                            horizontalalignment='left',verticalalignment='top', 
                            xycoords='axes fraction', size = 14)
    if pos == 'EDS/XPS':
        xy = (0.05,0.96)
        text = text_title #+ '\n' + str(text_list)
        ax.annotate(text,xy, xytext = xy, 
                            bbox=dict(boxstyle="square", fc="w"), 
                            horizontalalignment='left',verticalalignment='top', 
                            xycoords='axes fraction', size = 14)
    if pos == 'Gammy':
        xy = (0.97,0.04)
        text = text_title #+ '\n' + str(text_list)
        ax.annotate(text,xy, xytext = xy, 
                            bbox=dict(boxstyle="square", fc="w"), 
                            horizontalalignment='right',verticalalignment='bottom', 
                            xycoords='axes fraction', size = 14)
    if pos == 'Tafel Plot':
        # xy = (0.95,0.05)
        xy = (0.08,0.08)        
        text = text_title.split('-',1)[1].split(' ')[0]
        # ax.annotate(text,xy, xytext = xy, 
        #                     bbox=dict(boxstyle="square", fc="w"), 
        #                     horizontalalignment='right',verticalalignment='bottom', 
        #                     xycoords='axes fraction', size = 16)        
        ax.annotate(text,xy, xytext = xy, 
                            bbox=dict(boxstyle="square", fc="w"), 
                            horizontalalignment='left',verticalalignment='bottom', 
                            xycoords='axes fraction', size = 14)        
                
        
#    if pos == 'XRD':
#        #xy = (0.97,0.04)
#        text = text_title
#        ax.annotate(text,xy, xytext = xy, 
#                            bbox=dict(boxstyle="square", fc="w"), 
#                            horizontalalignment='right',verticalalignment='bottom', 
#                            xycoords='axes fraction', size = 14, color = color)
        
def global_text(ax, text, config = None, x = None, y = None , color = None, fontsize = None):
    if not config:
        ax.text(0.95, 0.01,'colored text in axes coords',
            verticalalignment='bottom', horizontalalignment='right',
            transform=ax.transAxes,
            color='green', fontsize=15)
    if config == 'XRD':
        """
        x and y refer to actual coordinates in the systems
        """
        ax.text(89.5, y, text, 
            verticalalignment='top', horizontalalignment='right',
            color=color, fontsize=12, zorder = 10)
    if config == 'XRD_zoom':
        ax.text(x, y, text, 
            verticalalignment='top', horizontalalignment='right',
            color=color, fontsize=12)
    if config == 'ARXPS':
        print('here0')
        ax.text(x, y, text, 
                verticalalignment='bottom', horizontalalignment='left',
                color=color, fontsize=12)
        print('here1')
def detail_annotation(ax, text, pos = 1):
    if pos == 1:
        xy = (0.05,0.9)
    ax.annotate(text,xy, xytext = xy, 
                        bbox=dict(boxstyle="square", fc="w"), 
                        horizontalalignment='left',verticalalignment='top', 
                        xycoords='axes fraction', size = 16)
        
def global_plt_table(ax, dataframe, config):
    if config == 'XPS Survey':
        ax.table(cellText=dataframe.values,
              colWidths = [0.1,0.15, 0.15],
              zorder=10,
              #rowLabels=row_labels,
              colLabels=dataframe.columns,
              cellLoc='left',
              colLoc ='left',
              #fontsize = 12,
              loc='upper right',)
    else:
        print('Configuration not detected in \"global_plt_table\"')
        
''' __________________INSTRUMENT SPECIFIC___________________________________'''

''' ICP settings '''

def ICP_global(ax):
    #ax.set_xlabel('Time / min ', fontsize=16)
    ax.set_ylabel('Concentration / ppb', fontsize=16) 
    ax.legend(loc='upper left', fontsize = 12)#, bbox_to_anchor=(1.3, 0.5))
    ax.grid(True, linestyle = '--', which='major', axis ='both', alpha = 0.5)
    
  
    ax.axhline(y = 0, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
    #ax.set_xlim(left = 0)
    ax.set_ylim([-5,15])
    
" ___________________________________________________________________ SEM/EDS "

''' EDS settings '''

def EDS_global(ax, element, x, x_tick_labels, legend = False, grid = False):
    #line = np.linspace(0, 100, 1000)
    #ax.plot(line,line, color = 'k', alpha = 0.4)
    #ax.set_xlabel('Intended Composition / %', fontsize = 16)
    ax.set_ylabel('at%', fontsize = 16)
    if legend:
        ax.legend(fontsize = 12, loc = 'lower right')
    ax.set_ylim(0,100)
    
    ax.set_xticks(x*100)
    ax.set_xticklabels(x_tick_labels, rotation = 45, fontsize = 14, ha='right')
    #ax.set_aspect('equal', adjustable='box')
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1 )


''' XRD settings'''

def XRD_global(ax, label = True, yticklabel = False):#

    ax.set_xlabel(r'2$\theta$ / $^\circ$', fontsize = 16)
    ax.set_ylabel('Intensity / arb. unit.', fontsize = 16)
    if yticklabel:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    else:
        ax.get_yaxis().set_ticks([])     
    
    if label:        
        ax.legend(loc='upper right')      
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))   s()               # put label outside the figure
#        handles, labels = ax.get_legend_handles_label
#        ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
#    # Shrink current axis by 20%
#    w = 0.8
#    box = ax.get_position()
#    ax.set_position([box.x0, box.y0, box.width * w, box.height])                                           # removes y ticks
#    if label:        
#        #ax.legend(loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
#        handles, labels = ax.get_legend_handles_labels()
#        ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
#    if yticklabel:
#        ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
#    else:
#        ax.yaxis.set_major_locator(plt.NullLocator())
" ___________________________________________________________ XPS "

''' XPS settings'''

def XPS_global(ax, x, 
               label = True, 
               yticklabel = True, 
               measurement_type = None):
    #ax.set_xlim([max(x),min(x)])

    if not ax.xaxis_inverted():
        ax.invert_xaxis()

    ax.set_xlabel('Binding Energy / eV ', fontsize = 16)
    ax.set_ylabel('Intensity / Counts/s', fontsize = 16)
    
    if label:        
        #ax.legend(loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='upper left', fontsize = 16, bbox_to_anchor=(1.3, 0.5))
    
    if yticklabel:
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    else:
        ax.yaxis.set_major_locator(plt.NullLocator())
        #ax.get_yaxis().set_ticks([])  
        
    if measurement_type == 'XPS Survey':
       ax.set_xlim(1350,0)
       ax.xaxis.set_minor_locator(AutoMinorLocator(4))
       ax.set_ylim(bottom = 0)
    elif measurement_type == 'Valence ARXPS':
        #legends = 
        ax.legend(loc='upper right', fontsize = 14)
        ax.set_xlim(20,-5)
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    elif measurement_type == 'V DP':
        # bbox anchor legend box outside figure.
        # ax.legend(loc='upper left', fontsize = 14, 
        #           bbox_to_anchor=(1, 1))
        ax.set_xlim(max(x),min(x))
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    elif measurement_type == 'Single Element ARXPS':
        #legends = 
        ax.legend(loc='upper right', fontsize = 14)
        ax.set_xlim(int(x.max()), int(round(x.min())))
        global_mayor_xlocator(ax, x_locator = 2)
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        #ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    elif measurement_type == 'SE ARXPS':
        #legends = 
        global_mayor_xlocator(ax, x_locator = 2)
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax.legend(loc='upper left', fontsize = 14)
        ax.set_xlim(int(math.floor(x.max())), int(math.ceil(x.min())))
        ax.set_ylabel('Intensity / Normalized', fontsize = 16)  
    elif measurement_type == 'SE DP':
        global_mayor_xlocator(ax, x_locator = 2)
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        # ax.legend(loc='upper left', fontsize = 14, 
        #          bbox_to_anchor=(1, 1))
        ax.set_xlim(int(math.floor(x.max())), int(math.ceil(x.min())))
        # ax.set_ylabel('Intensity / Normalized', fontsize = 16)
    elif measurement_type == 'SE std':
        global_mayor_xlocator(ax, x_locator = 2)
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        # ax.legend(loc='upper left', fontsize = 14, 
        #          bbox_to_anchor=(1, 1))
        ax.set_xlim(int(math.floor(x.max())), int(math.ceil(x.min())))
        # ax.set_ylabel('Intensity / Normalized', fontsize = 16)        
    else:
        print('XPS custom plotting functions not enabled')

def XPS_custom_plot_SE_settings(ax, 
                                element,
                                main_peak_only = False,
                                save_legend = True):
    if main_peak_only:
        if 'ZnLMM' in element:
            ax.set_xlabel('Kinetic Energy / eV ', fontsize = 16)  
            ax.set_xlim(982, 998)
        elif 'Pd' in element:
            # metallic Pd (Rodriguez, 1994)
            ax.axvline(x = 335.17, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0) 
            # PdZn (6.2:18.2) (Rodriguez, 1994)
            ax.axvline(x = 335.17+0.62, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)                
            
            # metallic bulk Pd (Bayer, 2006)
            ax.axvline(x = 335.04, linewidth=2, color='k', alpha = 1, linestyle = '--', zorder = 0) 
            # PdZn (6.2:18.2) (Bayer, 2006)
            ax.axvline(x = 335.92, linewidth=2, color='k', alpha = 1, linestyle = '--', zorder = 0)                
            
            ax.xaxis.set_minor_locator(AutoMinorLocator(5))
            ax.xaxis.set_major_locator(MultipleLocator(1))
            ax.set_xlim(339, 332)
            #pltF.global_mayor_xlocator(ax, x_locator = 2) 
        elif 'Zn'in element:
            # # metallic Zn (Rodriguez, 1994)
            # ax.axvline(x = 1044.92, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0) 
            # # PdZn (10.8:1), (Rodriguez, 1994)
            # ax.axvline(x = 1044.92-0.72, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)         
            # ax.set_xlim(1048, 1038)
            
            # metallic Zn (Bayer, 2006)
            ax.axvline(x = 1021.65, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0) 
            # PdZn (5 ML on Pd(111)), Bayer, 2006)
            ax.axvline(x = 1021.17, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)         
            ax.set_xlim(1025, 1016)
            
            ax.xaxis.set_minor_locator(AutoMinorLocator(4))
            ax.xaxis.set_major_locator(MultipleLocator(2)) 
            # ax.set_xlim(1027, 1017)
            
        elif 'Valence' in element:
            # metallic Zn            
            ax.xaxis.set_minor_locator(AutoMinorLocator(4))
            ax.xaxis.set_major_locator(MultipleLocator(2)) 
            
            # ax.set_xlim(1027, 1017)
            ax.set_xlim(14, -2)            
        elif 'OKL' in element:
            ax.set_xlabel('Kinetic Energy / eV ', fontsize = 16)
            ax.xaxis.set_minor_locator(AutoMinorLocator(5))
            ax.xaxis.set_major_locator(MultipleLocator(5)) 
            # ax.set_xticklabels(ax.get_xticklabels(), ha="right", rotation=45)
            ax.tick_params(labelrotation=45, right = True)
            ax.set_xlim(478, 531)
        elif 'C' in element:
            ax.axvline(x = 284.84, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)
            ax.set_xlim(296, 280) 
        elif 'Al' in element:
            # XPS simplified
            ax.axvline(x = 72.6, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)
            ax.axvline(x = 74.6, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)
            ax.set_xlim(82, 68)                
    else:
        if 'ZnLMM' in element:
            ax.set_xlabel('Kinetic Energy / eV ', fontsize = 16)
            # ax.legend(loc='upper left', fontsize = 12)
            ax.set_xlim(982, 998)
        elif 'Pd' in element:
            # metallic Pd
            ax.axvline(x = 335.17, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0) 
            # PdZn (6.2:18.2) 
            ax.axvline(x = 335.17+0.62, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)                
            ax.xaxis.set_minor_locator(AutoMinorLocator(4))
            ax.xaxis.set_major_locator(MultipleLocator(2))
            #pltF.global_mayor_xlocator(ax, x_locator = 2) 
        elif 'Zn' in element:
            # metallic Zn
            ax.axvline(x = 1044.92, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0) 
            # PdZn (10.8:1) 
            ax.axvline(x = 1044.92-0.72, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)                     
            ax.xaxis.set_minor_locator(AutoMinorLocator(5))
            ax.xaxis.set_major_locator(MultipleLocator(5))     
        elif 'OKL' in element:
            ax.set_xlabel('Kinetic Energy / eV ', fontsize = 16)
            ax.xaxis.set_minor_locator(AutoMinorLocator(5))
            ax.xaxis.set_major_locator(MultipleLocator(5)) 
            # ax.set_xticklabels(ax.get_xticklabels(), ha="right", rotation=45)
            ax.tick_params(labelrotation=45, right = True)  
            ax.set_xlim(478, 531)
        elif 'C' in element:
            ax.axvline(x = 284.84, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0) 
            ax.set_xlim(296, 280)  
        elif 'Al' in element:
            # XPS simplified
            ax.axvline(x = 72.6, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)
            ax.axvline(x = 74.6, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder = 0)
            ax.set_xlim(82, 68)  
    if save_legend:
        ax.legend(loc='upper left', fontsize = 14, 
                  bbox_to_anchor=(1, 1))   
           
        
    if 'NI' in element:
        ax.set_ylabel('Intensity / Normalized', fontsize = 16)
    else:
        ax.set_ylabel('Intensity / Counts/s', fontsize = 16)

           
            
       
        
''' _______________________________________ CA (chronoamperomtry settings) '''

' this function is to plot j vs. V '
def CA_global(ax, ylabel, xlabel, legend = True, grid = True, plot_type = None):
    print(ylabel)
    print(xlabel)
    if ylabel == 'Ewe/RHE':
        ax.set_ylabel('V / V vs. RHE ', fontsize=16)
    elif ylabel == 'Ewe/SHE':
        ax.set_ylabel('V / V vs. SHE ', fontsize=16)
    elif ylabel == 'Ewe/V':
       ax.set_ylabel('V / V vs. Ag/AgCl', fontsize=16)
    elif ylabel == 'I/mA':
        ax.set_ylabel('I / mA', fontsize=16)
    elif ylabel == 'I/mAcm-2':
        ax.set_ylabel('j$_{\mathrm{geo}}$ / mA cm$^{-2}$', fontsize=16)
    elif ylabel == 'Re(Z)/Ohm':
        ax.set_ylabel('R$_u$ / $\Omega$', fontsize=16)
    elif ylabel == 'Rcmp/Ohm':
        ax.set_ylabel('R$_{cmp}$ / $\Omega$', fontsize=16)
    elif ylabel == 'Ru/Ohm':
        ax.set_ylabel('R$_\mathrm{u}$ / $\Omega$', fontsize=16)        
    elif ylabel == 'V':
        ax.set_ylabel('Ohmic Drop / V', fontsize=16)
    else:
        ax.set_ylabel('no input - check!', fontsize=16)
    
    if xlabel == 'time/h':
        ax.set_xlabel('Time / h', fontsize = 16)
    elif xlabel == 'time/min':
        ax.set_xlabel('Time / min', fontsize = 16)
    elif xlabel == 'I/mAcm-2':
        ax.set_xlabel('j / mA cm$^{-2}$', fontsize = 16)
    elif xlabel == 'Ewe/RHE':
        ax.set_xlabel('V / V vs. RHE ', fontsize=16)
        
    if grid:        
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if grid and xlabel == 'time/h':    
        ax.grid(which='both', axis = 'x', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    elif grid and xlabel is None:        
        if ylabel == 'Ru/Ohm': #RvsV
            ax.grid(which='major', axis = 'y', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
            ax.grid(which='major', axis = 'x', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )            
        else:
            ax.grid(which='both', axis = 'x', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if legend:        
        leg = ax.legend(loc='upper left', fontsize = 14, bbox_to_anchor=(1.05, 1.0))
        for line in leg.get_lines():
            line.set_linewidth(4.0)            
    if plot_type == 'Tafel Plot':
        print('hej')

        
''' CP (chronopotentiometry) settings'''

def CP_global(ax, V, t, label = False, grid = True):

    ax.set_xlabel('Time / min', fontsize=16)#ax.set_xlabel('Time / s', fontsize=16)
    y_range = 3
    if V == 'Ewe/V':
        ax.set_ylabel('V / V vs. RHE ', fontsize=16)        
        ax.set_ylim(-1.5,-1.5+y_range)
    elif V == 'Ewe/SHE':
        ax.set_ylabel('V / V vs. SHE ', fontsize=16)
        ax.set_ylim(-2.5,0.5)#-2+y_range)
        
    if t == 'time/min':
        ax.set_xlabel('Time / min', fontsize=16)
    elif t == 'time/s':
        ax.set_xlabel('Time / s', fontsize=16)
    
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
        #ax.grid(True, linestyle = '--', which='both', axis ='both', alpha = 0.5)
    if label:        
        leg = ax.legend(loc='lower right', fontsize = 14) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)
''' CV (cyclic voltammetry) settings'''

def CV_global(ax, V, label = True, hline = True, grid = True):
    ax.yaxis.tick_right()
    ax.xaxis.tick_top()
    ax.yaxis.set_label_position('right')
    ax.xaxis.set_label_position('top')
    if V == 'Ewe/V':
        ax.set_xlabel('V / V vs. RHE ', fontsize=16)
    elif V == 'Ewe/SHE':
        ax.set_xlabel('V / V vs. SHE ', fontsize=16)

    ax.set_ylabel('j / mA cm$^{-2}$', fontsize=16) 
    if hline:
        ax.axhline(y = -5.00, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder=1)
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if label:        
        leg = ax.legend(loc='lower right', fontsize = 14) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)
            
def PEIS_global(ax, phase_ax, idx, N, grid = False, legend = False):
    if N != 1:
        if idx == N-1:
            ax.set_xlabel('f / Hz', fontsize=16)
        if idx == int((N-1)/2):
            ax.set_ylabel('|Z|/ Ohm', fontsize=16)
            phase_ax.set_ylabel('$\Phi/\degree$ ', fontsize = 16)
    else:
        ax.set_xlabel('f / Hz', fontsize=16)    
        ax.set_ylabel('|Z|/ Ohm', fontsize=16)
        phase_ax.set_ylabel('$\Phi/\degree$ ', fontsize = 16)
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if legend:        
        leg = ax.legend(loc='lower right', fontsize = 14) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)
    ax.ticklabel_format(axis='x', style='sci', scilimits=(3,3))   

def Nyquist_global(ax, grid = True, legend = False):

    ax.set_xlabel('Re(Z) / Ohm', fontsize=16)
    ax.set_ylabel('Im(Z) / Ohm', fontsize=16)
        
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if legend:        
        leg = ax.legend(loc='lower right', fontsize = 14) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)     

def TafelPlot_global(axs, 
                     V_major_locator,
                     j_major_locator,
                     grid = True, 
                     ):
    for ax in axs.flatten():
        ax.grid(which='major', 
                axis = 'both', 
                color = 'grey', 
                alpha=0.2, 
                linewidth = 1, 
                linestyle = '--' )
        # ax.set_yscale('symlog')        
        ax.set_yscale('log')        
        
        global_mayor_xlocator(ax, 
                              x_locator = V_major_locator)   
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        
        " ----- yaxis ticks "
        # locmaj = LogLocator(base=10,numticks=3) 
        # locmin = LogLocator(base=10.0,subs=(0.2,0.4,0.6,0.8),numticks=2)
        # ax.xaxis.set_minor_locator(locmin)
        # ax.yaxis.set_major_locator(locmaj)
        # ax.yaxis.set_minor_locator(SymmetricalLogLocator(transform=10, base = Locator(10)))
    # ylabel
    for ax in axs[:,0]:     
        ax.set_ylabel('j$_{\mathrm{geo}}$ / mA cm$^{-2}$', fontsize=16)
    for ax in axs[-1,:]:  
        ax.set_xlabel('V / V vs. RHE ', fontsize=16)
        ax.set_xticklabels(ax.get_xticks())
        xlabels = ax.get_xticklabels()
        ax.set_xticklabels(xlabels, rotation=40, ha = 'right')
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
         
            
            
# _______________________ GAMMY ______________________________________________

def CV_Gammy_global(ax, label = True, hline = True, grid = True):
    #ax.yaxis.tick_right()
    #ax.xaxis.tick_top()
    #ax.yaxis.set_label_position('right')
    #ax.xaxis.set_label_position('top')

    ax.set_xlabel('V / V vs. Ag/AgCl ', fontsize=16)

    ax.set_ylabel('j / mA cm$^{-2}$', fontsize=16) 
    if hline:
        ax.axhline(y = 0.00, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder=1)
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if label:        
        leg = ax.legend(loc='upper left', fontsize = 12) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)
            
def Randles_Secvik_global(ax, label = True, hline = True, grid = True):
    ax.set_xlabel(r'$ \nu^{1/2}$  /  (V/s)$^{1/2}$', fontsize=16)
    ax.set_ylabel('I$_p$ / A cm$^{-2}$', fontsize=16) 
    if hline:
        ax.axhline(y = 0.00, linewidth=2, color='k', alpha = 0.5, linestyle = '--', zorder=1)
    if grid:
        ax.grid(which='major', axis = 'both', color = 'grey', alpha=0.2, linewidth =1, linestyle = '--' )
    if label:        
        leg = ax.legend(loc='upper left', fontsize = 12) #bbox_to_anchor=(1.3, 0.5)   
        for line in leg.get_lines():
            line.set_linewidth(4.0)
    ax.set_ylim([0,0.00125])
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
            
# ________________________ Gas Conversion _____________________________________

def FlowControllerCalibrationCurve_global(ax):
    #ax.set_xlabel('Time / min ', fontsize=16)
    ax.set_xlabel('Scale Reading / mm', fontsize=16) 
    ax.set_ylabel('Flow / mL min$^{-1}$', fontsize=16) 
    ax.legend(loc='upper left', fontsize = 12)#, bbox_to_anchor=(1.3, 0.5))
    ax.grid(True, linestyle = '-', which='both', axis ='both', alpha = 0.5)
    
  
    #ax.axhline(y = 0, linewidth=2, color='k', alpha = 0.5, linestyle = '--')
    #ax.set_xlim(left = 0)
#    #ax.set_ylim(bottom = 0)
#    ax.set_ylim([80,130])
#    ax.set_xlim([0,100])
    ax.set_ylim([0,50])
    ax.set_xlim([0,100])
    
# ----------------------------------------------------------- GC Perkin Elmer "

def GC_show_background_fitting(ax, x, y, plt_title):
        ax.set_xlabel('time [min]')
        #background_spectrum.set_ylabel('a.u.')
        ax.tick_params('y', labelsize = 8)
        ax.yaxis.offsetText.set_fontsize(8)
        ax.axes.set_title(plt_title, loc = 'right', 
                                           fontdict = {'fontsize' : 8} )
        y_min, y_max = min(y), max(y)
        ax.set_xlim([min(x), max(x)])
        ax.set_ylim(bottom = y_min - (y_max-y_min)*0.1)
        ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
        
def GC_show_peak_plotting(ax, x, y, plt_title, detector):
    if detector == 'FID':
            ax.set_xlabel('time [min]')
    # background_spectrum.set_ylabel('a.u.')
    # ax.tick_params('y', labelsize = 8)
    # ax.yaxis.offsetText.set_fontsize(8)
    ax.axes.set_title(plt_title, loc = 'right', 
                                       fontdict = {'fontsize' : 16} )
    # ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0)) 
    yfmt = ScalarFormatterForceFormat(y)
    yfmt.set_powerlimits((0,0))
    ax.yaxis.set_major_formatter(yfmt)
    

def GC_show_all_spectra(ax, x, y, plt_title):
            
    ax.set_ylabel('a.u.')
    ax.tick_params('y', labelsize = 8)
    ax.yaxis.offsetText.set_fontsize(8)
    ax.axes.set_title(plt_title, loc = 'right', 
                                       fontdict = {'fontsize' : 8} )
    y_min, y_max = min(y), max(y)
    ax.set_ylim(bottom = y_min - (y_max-y_min)*0.1)
    ax.set_xlim([min(x), max(x)])
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))   
    # ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))    

def GCPE_savefig(fig,       
                 raw_file_path, 
                 detector, 
                 GC_plot_title = None, 
                 plot_type = 'entire chromatogram'):
    directory = os.path.basename(raw_file_path) + ' ' + 'Figures'
    OSfunc.create_directory(directory)
    
    if plot_type == 'single peak':
        detector += '_' + 'single'    

    if GC_plot_title:
        save_plot_title = GC_plot_title + '_' + detector + '.png'
        plt.savefig(OSfunc.join_paths(directory, save_plot_title), dpi=200, bbox_inches='tight')
        # plt.savefig(OSfunc.join_paths(raw_file_path, save_plot_title), dpi=200)
        print('plot of all {} chromatograms saved'.format(detector))
        # directory + '/' + plt_title + ', ' + addcomment
    else:
        save_plot_title = detector + '.png'                    
        plt.savefig(OSfunc.join_paths(directory, save_plot_title), dpi=200, bbox_inches='tight')
        # plt.savefig(join_paths(raw_file_path, save_plot_title), dpi=200)
        print('plot of all {} chromatograms saved'.format(detector))
    plt.close(fig)
    
def GCPE_savecolorbar(fig, raw_file_path):
    directory = os.path.basename(raw_file_path) + ' ' + 'Figures'
    OSfunc.create_directory(directory)

    save_plot_title = 'colormap.png'
    plt.savefig(OSfunc.join_paths(directory, save_plot_title ), dpi=200, bbox_inches='tight')
    plt.close(fig)    
    
class ScalarFormatterForceFormat(ScalarFormatter):
    def __init__(self, 
                  y):
        
        # attributes
        super().__init__()
        self.y = y
        self.y_diff = max(y)-min(y)
        
        # functions
        # print(type(self.y_diff))
        # print(self.y_diff)
        self.order_of_magnitude()
        # # print(self.y)
        # print(self.y_diff)
    
    def order_of_magnitude(self):
        self.order_of_magnitude = math.floor(math.log(self.y_diff, 10))
        # print(self.order_of_magnitude)    
        
    # from https://stackoverflow.com/questions/42142144/displaying-first-decimal-digit-in-scientific-notation-in-matplotlib
    def _set_format(self):      # Override function that finds format to use.
        # self.format = "%1.1f"   # Give format here
        order_of_magnitude_diff = self.y_diff/10**self.order_of_magnitude
        # print('difference: {}'.format(self.y_diff))
        # print('difference: {}'.format(order_of_magnitude_diff))
        if order_of_magnitude_diff < 2:    
            self.format = "%1.2f"   # Give format here
            # print(order_of_magnitude_diff)
        else:
            self.format = "%1.1f"   # Give format here
            # print('else')

        
        

" ______________________________________________________________ FE PLOTTING "
        
def FE_global(ax,
              ax_right,
              x,
              xtick_labels_df,
              plot_label = True):
    ax.tick_params(axis = 'x',
                   which = 'major',
                   bottom = False,      # ticks along the bottom edge are off
                   # top=False,         # ticks along the top edge are off
                   # labelbottom=False                   
                   # direction='out', 
                   # length=12, 
                   # width=2, 
                   # labelsize = 14
                   )
    xtick_labels = xtick_labels_df.tolist()
    ax.set_xticks(x)
    if len(x) != len(xtick_labels):
        print('Number of ticks: ({}) and number of labels ({})'\
              ' do not match'.format(len(x), len(xtick_labels)))
    else:
        ax.set_xticklabels(xtick_labels, rotation = 45, fontsize = 14, ha='right')    
        # ax.set_xticklabels([str(label) for label in xtick_labels], rotation = 45, fontsize = 14, ha='right')    
        # ax.set_xticklabels(ex, rotation = 45, fontsize = 14, ha='right')   
    if plot_label:
        ax.legend(loc='upper left', bbox_to_anchor=(1.2, 1.0))
    ax.set_ylabel('FE / %', fontsize = 16)
    ax_right.set_ylabel('j / mAcm$^{-2}$', fontsize = 16)
    global_minor_locator(ax, x_locator = 1, y_locator = 2)
    global_minor_locator(ax_right, x_locator = 1, y_locator = 5)
    
    
    if xtick_labels_df.name == 'V avg/RHE':
        ax.set_xlabel('V / V vs RHE', fontsize = 16)
    else:
        print('xlabel not reconized: {}'.format(xtick_labels_df.nam))
    

           
         