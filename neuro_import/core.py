"""
Core functionality of the NeuroImport package.

This module provides the main entry points for the package, including
functions for loading data files, finding channels, and plotting data.
"""

import os
import time
import matplotlib.pyplot as plt

from .utils.channel_utils import (
    print_names_in_group,
    find_channel_in_group,
    find_channel_in_header
)
from .importers.file_registry import get_importer_for_file


def load_file(filename):
    """
    Load a neurophysiology data file.
    
    This function detects the file type based on extension and automatically
    selects the appropriate importer. Currently supports:
    - .rhs (Intan RHS) files using a Rust-based high performance importer
    
    Parameters
    ----------
    filename : str
        The path to the file to load
        
    Returns
    -------
    tuple
        (result, data_present) where:
        - result is a dictionary containing all parsed data and metadata
        - data_present is a boolean indicating if data was found in the file
    """
    # Start timing
    tic = time.time()
    
    # Determine file extension
    _, ext = os.path.splitext(filename)
    
    # Get the appropriate importer for this file type
    importer = get_importer_for_file(ext)
    if importer is None:
        raise ValueError(f"No importer found for file type: {ext}")
    
    # Load the file using the selected importer
    result, data_present = importer.load(filename)
    
    # Report how long the read took
    print(f'Done! Elapsed time: {time.time() - tic:.1f} seconds')
    
    return result, data_present


def print_all_channel_names(result):
    """
    Print the names of all available channels in the result dictionary.
    
    This function is useful for discovering which channels are available for
    plotting or further analysis.
    
    Parameters
    ----------
    result : dict
        The result dictionary returned by load_file()
    """
    channel_groups = [
        'amplifier_channels',
        'dc_amplifier_channels',
        'stim_channels',
        'amp_settle_channels',
        'charge_recovery_channels',
        'compliance_limit_channels',
        'board_adc_channels',
        'board_dac_channels',
        'board_dig_in_channels',
        'board_dig_out_channels'
    ]
    
    for group in channel_groups:
        if group in result:
            print(f"\n{group.replace('_', ' ').title()}:")
            print_names_in_group(result[group])


def find_channel(channel_name, result):
    """
    Find a channel by name in the result dictionary.
    
    Parameters
    ----------
    channel_name : str
        The name of the channel to find
    result : dict
        The result dictionary returned by load_file()
        
    Returns
    -------
    tuple
        (found, signal_group_name, channel_index) where:
        - found is a boolean indicating if the channel was found
        - signal_group_name is the name of the signal group containing the channel
        - channel_index is the index of the channel in the signal group
    """
    return find_channel_in_header(channel_name, result)


def plot_channel(channel_name, result):
    """
    Plot data for a specific channel.
    
    Parameters
    ----------
    channel_name : str
        The name of the channel to plot
    result : dict
        The result dictionary returned by load_file()
    
    Returns
    -------
    tuple
        (fig, ax) The matplotlib figure and axis objects created for the plot
    
    Raises
    ------
    ValueError
        If the channel is not found or cannot be plotted
    """
    # Find channel that corresponds to this name
    channel_found, signal_type, signal_index = find_channel_in_header(
        channel_name, result)
    
    # Plot this channel
    if channel_found:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(channel_name)
        ax.set_xlabel('Time (s)')
        
        signal_data_map = {
            'amplifier_channels': ('amplifier_data', 'Voltage (microVolts)'),
            'dc_amplifier_channels': ('dc_amplifier_data', 'Voltage (Volts)'),
            'stim_channels': ('stim_data', 'Current (microAmps)'),
            'amp_settle_channels': ('amp_settle_data', 'Amp Settle Events (High or Low)'),
            'charge_recovery_channels': ('charge_recovery_data', 'Charge Recovery Events (High or Low)'),
            'compliance_limit_channels': ('compliance_limit_data', 'Compliance Limit Events (High or Low)'),
            'board_adc_channels': ('board_adc_data', 'Voltage (Volts)'),
            'board_dac_channels': ('board_dac_data', 'Voltage (Volts)'),
            'board_dig_in_channels': ('board_dig_in_data', 'Digital In Events (High or Low)'),
            'board_dig_out_channels': ('board_dig_out_data', 'Digital Out Events (High or Low)')
        }
        
        if signal_type not in signal_data_map:
            raise ValueError(f"Signal type {signal_type} not supported for plotting")
            
        signal_data_name, ylabel = signal_data_map[signal_type]
        ax.set_ylabel(ylabel)
        
        if signal_data_name not in result:
            raise ValueError(f"Data for {signal_data_name} not found in result")
            
        ax.plot(result['t'], result[signal_data_name][signal_index, :])
        ax.margins(x=0, y=0)
        plt.tight_layout()
        
        return fig, ax
    else:
        raise ValueError(f"Channel '{channel_name}' not found")