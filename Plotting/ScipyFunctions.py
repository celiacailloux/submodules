# -*- coding: utf-8 -*-
"""
Created on Fri May 15 08:07:44 2020

@author: ceshuca
"""
import numpy as np
from lmfit import Minimizer, Parameters
from lmfit.lineshapes import gaussian, lorentzian
from lmfit.models import GaussianModel, LinearModel, SkewedGaussianModel, LognormalModel
from scipy.special import erf

def locateErrorFunctionCenter(x, y, center = 'peak maximum'):
    """
    Parameters
    ----------
    x : numpy array
        x data set
    y : numpy array
        y data set
    center : string, optional
        Option to choose which type of center you want for your error function. 
        The default is 'peak maximum'.

    Returns
    -------
    erf_center : float
        The x-value for which the y-value has a maximum

    """

    " the step of the error-function is placed at peak-maximum "
    erf_center_idx = [i for i, j in enumerate(y) if j == np.amax(y)]            # index for y-max (as list)
    erf_center = x[erf_center_idx[0]]                                           # single value instead of a vector
    return erf_center

def get_maskedXY(x_min, x_max, x, y):
    idx_range = np.ma.masked_outside(x, x_min, x_max).mask                      # Boolean list. True for all values outside the x_min, x_max limit
    x_masked = x[~idx_range]                                                    # The tilde operator means inverted.
    y_masked = y[~idx_range]
    return x_masked, y_masked

def get_maskedXY_inverted(x_min, x_max, x, y):
    idx_range = np.ma.masked_outside(x, x_min, x_max).mask                      # Boolean list. True for all values outside the x_min, x_max limit
    x_masked = x[idx_range]                                                    # The tilde operator means inverted.
    y_masked = y[idx_range]
    return x_masked, y_masked

def residual_GC(pars, x, sigma = None, data = None):
    yg = gaussian(x)#, pars['amp_g'], pars['cen_g'], pars['wid_g'])
    yl = lorentzian(x)#, pars['amp_l'], pars['cen_l'], pars['wid_l'])

    slope = pars['line_slope']
    offset = pars['line_off']
    model = yg + yl + offset + x*slope
    
    if data is None:
        return model
    if sigma is None:
        return (model - data / sigma)
    

def fit_GC_residual_(x, y, peak, peak_center):
    mod = GaussianModel(prefix='peak_') + LinearModel(prefix='bkg_')
    
    pars = mod.make_params()
    #pars['peak_amplitude'].value = 1e8
    pars['peak_center'].value = peak_center
    #pars['peak_sigma'].value = 2.0
    pars['bkg_intercept'].value = 1e6#
    pars['bkg_slope'].value = 0.0

    out = mod.fit(y, pars, x=x)#, iter_cb=per_iteration)  
    
    if peak == 'H2':
        #print('Nfev = ', out.nfev)
        print(out.fit_report())
        #print(out.pars['peak_amplitude'].value)

    return out

def fit_GC_residual__(x, y, peak, peak_center):
    mod =  SkewedGaussianModel(prefix='peak_') + LinearModel(prefix='bkg_')
    
    pars = mod.make_params()
    pars['peak_amplitude'].value = 1e6
    pars['peak_center'].value = peak_center
    pars['peak_gamma'].value = 4
    pars['peak_sigma'].value = 0.4
    pars['bkg_intercept'].value = 1e5#
    pars['bkg_slope'].value = 500

    out = mod.fit(y, pars, x=x)#, iter_cb=per_iteration)  
    
    if peak == 'H2':
        #print('Nfev = ', out.nfev)
        print(out.fit_report())
        #print(out.pars['peak_amplitude'].value)

    return out

def fit_GC_residual(x, y, peak, peak_center):
    mod =  LinearModel(prefix='bkg_')
    
    pars = mod.guess(y,x)# mod.make_params()
    #pars['bkg_intercept'].value = 1e5#
    #pars['bkg_slope'].value = 500

    out = mod.fit(y, pars, x=x)
    
    # if peak == 'H2':
    #     #print('Nfev = ', out.nfev)
    #     print(out.fit_report())
    #     #print(out.pars['peak_amplitude'].value)

    return out

def linfunc(x, out):
    alpha = out.best_values['bkg_slope']
    beta = out.best_values['bkg_intercept']
    return alpha*x + beta

def per_iteration(pars, iteration, resid, *args, **kws):
    print(" ITER ", iteration, ["%.5f" % p for p in pars.values()])
    
def errorfunc(time, center, size, height):
    """ error function """
    step_speed = 10000 #making the erf-function a almost step-function
    return height+size*erf(step_speed*(time-center))
    
    

    
