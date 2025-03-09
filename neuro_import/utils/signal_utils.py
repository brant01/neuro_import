"""
Signal processing utilities for neurophysiology data.
"""

import numpy as np
from .filter_utils import notch_filter


def scale_timestamps(timestamps, sample_rate):
    """
    Scale timestamps to seconds.
    
    Parameters
    ----------
    timestamps : array_like
        Array of integer timestamps
    sample_rate : float
        Sampling rate in Hz
        
    Returns
    -------
    numpy.ndarray
        Timestamps in seconds
    """
    return np.array(timestamps) / sample_rate


def scale_amplifier_data(data):
    """
    Scale amplifier data to microvolts.
    
    Parameters
    ----------
    data : array_like
        Raw amplifier data
        
    Returns
    -------
    numpy.ndarray
        Amplifier data in microvolts
    """
    return np.multiply(0.195, (data.astype(np.int32) - 32768))


def scale_stim_data(data, stim_step_size):
    """
    Scale stimulation data to microamps.
    
    Parameters
    ----------
    data : array_like
        Raw stimulation data
    stim_step_size : float
        Stimulation step size
        
    Returns
    -------
    numpy.ndarray
        Stimulation data in microamps
    """
    return np.multiply(stim_step_size, data / 1.0e-6)


def scale_dc_amplifier_data(data):
    """
    Scale DC amplifier data to volts.
    
    Parameters
    ----------
    data : array_like
        Raw DC amplifier data
        
    Returns
    -------
    numpy.ndarray
        DC amplifier data in volts
    """
    return np.multiply(-0.01923, (data.astype(np.int32) - 512))


def scale_board_adc_data(data):
    """
    Scale board ADC data to volts.
    
    Parameters
    ----------
    data : array_like
        Raw board ADC data
        
    Returns
    -------
    numpy.ndarray
        Board ADC data in volts
    """
    return np.multiply(312.5e-6, (data.astype(np.int32) - 32768))


def scale_board_dac_data(data):
    """
    Scale board DAC data to volts.
    
    Parameters
    ----------
    data : array_like
        Raw board DAC data
        
    Returns
    -------
    numpy.ndarray
        Board DAC data in volts
    """
    return np.multiply(312.5e-6, (data.astype(np.int32) - 32768))


def extract_digital_data(data_raw, channels, channel_count):
    """
    Extract digital data from raw format.
    
    Parameters
    ----------
    data_raw : array_like
        Raw digital data
    channels : list
        List of channel dictionaries
    channel_count : int
        Number of channels
        
    Returns
    -------
    numpy.ndarray
        Extracted digital data
    """
    result = np.zeros((channel_count, len(data_raw)), dtype=np.bool_)
    
    for i in range(channel_count):
        result[i, :] = np.not_equal(
            np.bitwise_and(
                data_raw,
                (1 << channels[i]['native_order'])
            ),
            0
        )
    
    return result


def extract_stim_data(stim_data_raw):
    """
    Extract stimulation data components from raw data.
    
    Parameters
    ----------
    stim_data_raw : array_like
        Raw stimulation data
        
    Returns
    -------
    dict
        Dictionary containing extracted components:
        - compliance_limit_data
        - charge_recovery_data
        - amp_settle_data
        - stim_polarity
        - stim_data (current amplitude with sign)
    """
    result = {}
    
    # Extract boolean flags
    result['compliance_limit_data'] = np.bitwise_and(stim_data_raw, 32768) >= 1
    result['charge_recovery_data'] = np.bitwise_and(stim_data_raw, 16384) >= 1
    result['amp_settle_data'] = np.bitwise_and(stim_data_raw, 8192) >= 1
    
    # Extract polarity (sign)
    result['stim_polarity'] = 1 - (2 * (np.bitwise_and(stim_data_raw, 256) >> 8))
    
    # Extract current amplitude
    curr_amp = np.bitwise_and(stim_data_raw, 255)
    
    # Apply polarity to get signed current amplitude
    result['stim_data'] = curr_amp * result['stim_polarity']
    
    return result


def apply_notch_filter_to_data(data, sample_rate, notch_freq, bandwidth=10):
    """
    Apply notch filter to all channels in amplifier data.
    
    Parameters
    ----------
    data : array_like
        Amplifier data, shape (num_channels, num_samples)
    sample_rate : float
        Sampling rate in Hz
    notch_freq : float
        Notch filter frequency in Hz
    bandwidth : float, optional
        Notch filter bandwidth in Hz, default is 10
        
    Returns
    -------
    numpy.ndarray
        Filtered amplifier data
    """
    if notch_freq == 0:
        return data
    
    filtered_data = np.copy(data)
    num_channels = data.shape[0]
    
    for i in range(num_channels):
        filtered_data[i, :] = notch_filter(
            data[i, :],
            sample_rate,
            notch_freq,
            bandwidth
        )
    
    return filtered_data