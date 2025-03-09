"""
Filter utilities for processing neurophysiology data.
"""

import math
import numpy as np


def notch_filter(signal_in, f_sample, f_notch, bandwidth):
    """
    Apply a notch filter to remove power line noise.
    
    This function implements a notch filter (e.g., for 50 or 60 Hz) on the input
    signal. A bandwidth of 10 Hz is recommended for 50 or 60 Hz notch filters;
    narrower bandwidths lead to poor time-domain properties with an extended
    ringing response to transient disturbances.
    
    Parameters
    ----------
    signal_in : array_like
        Input signal
    f_sample : float
        Sample rate of data (in Hz or Samples/sec)
    f_notch : float
        Filter notch frequency (in Hz)
    bandwidth : float
        Notch 3-dB bandwidth (in Hz)
        
    Returns
    -------
    numpy.ndarray
        Filtered signal
    
    Example
    -------
    If neural data was sampled at 30 kSamples/sec
    and you wish to implement a 60 Hz notch filter:
    
    out = notch_filter(signal_in, 30000, 60, 10)
    """
    # Calculate parameters used to implement IIR filter
    t_step = 1.0 / f_sample
    f_c = f_notch * t_step
    signal_length = len(signal_in)
    parameters = _calculate_iir_parameters(bandwidth, t_step, f_c)
    
    # Create empty signal_out NumPy array
    signal_out = np.zeros(signal_length)
    
    # Set the first 2 samples of signal_out to signal_in.
    signal_out[0] = signal_in[0]
    signal_out[1] = signal_in[1]
    
    # Run filter.
    for i in range(2, signal_length):
        signal_out[i] = _calculate_iir(i, signal_in, signal_out, parameters)
    
    return signal_out


def _calculate_iir_parameters(bandwidth, t_step, f_c):
    """
    Calculate parameters for IIR filter.
    
    Parameters
    ----------
    bandwidth : float
        Notch 3-dB bandwidth (in Hz)
    t_step : float
        Time step between samples
    f_c : float
        Normalized frequency of the notch
        
    Returns
    -------
    dict
        Dictionary of IIR filter parameters
    """
    parameters = {}
    parameters['d'] = math.exp(-2.0 * math.pi * (bandwidth/2.0) * t_step)
    parameters['b'] = (1.0 + parameters['d']**2) * math.cos(2.0 * math.pi * f_c)
    parameters['a0'] = 1.0
    parameters['a1'] = -parameters['b']
    parameters['a2'] = parameters['d']**2
    parameters['a'] = (1.0 + parameters['d']**2) / 2.0
    parameters['b0'] = 1.0
    parameters['b1'] = -2.0 * math.cos(2.0 * math.pi * f_c)
    parameters['b2'] = 1.0
    
    return parameters


def _calculate_iir(i, signal_in, signal_out, parameters):
    """
    Calculate one sample of IIR filter output.
    
    Parameters
    ----------
    i : int
        Current index in signal
    signal_in : array_like
        Input signal
    signal_out : array_like
        Output signal (values up to i-1 are used)
    parameters : dict
        IIR filter parameters
        
    Returns
    -------
    float
        Filtered value for index i
    """
    return (
        (parameters['a'] * parameters['b2'] * signal_in[i - 2] +
         parameters['a'] * parameters['b1'] * signal_in[i - 1] +
         parameters['a'] * parameters['b0'] * signal_in[i] -
         parameters['a2'] * signal_out[i - 2] -
         parameters['a1'] * signal_out[i - 1]) /
        parameters['a0']
    )