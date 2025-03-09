"""
Utility functions for working with channels in neurophysiology data.
"""


def print_names_in_group(signal_group):
    """
    Print the names of all channels in a signal group.
    
    Parameters
    ----------
    signal_group : list
        A list of channel dictionaries in a signal group
    """
    for this_channel in signal_group:
        print(this_channel['custom_channel_name'])


def find_channel_in_group(channel_name, signal_group):
    """
    Find a channel with a specific name in a signal group.
    
    Parameters
    ----------
    channel_name : str
        The name of the channel to find
    signal_group : list
        A list of channel dictionaries in a signal group
        
    Returns
    -------
    tuple
        (found, channel_index) where:
        - found is a boolean indicating if the channel was found
        - channel_index is the index of the channel in the signal group
    """
    for count, this_channel in enumerate(signal_group):
        if this_channel['custom_channel_name'] == channel_name:
            return True, count
    return False, 0


def find_channel_in_header(channel_name, header):
    """
    Find a channel with a specific name across all signal groups in a header.
    
    Parameters
    ----------
    channel_name : str
        The name of the channel to find
    header : dict
        The header dictionary containing signal groups
        
    Returns
    -------
    tuple
        (found, signal_group_name, channel_index) where:
        - found is a boolean indicating if the channel was found
        - signal_group_name is the name of the signal group containing the channel
        - channel_index is the index of the channel in the signal group
    """
    # Define all possible signal groups to search
    signal_groups = [
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
    
    # Search through each signal group
    for group_name in signal_groups:
        if group_name in header:
            channel_found, channel_index = find_channel_in_group(
                channel_name, header[group_name])
            if channel_found:
                return True, group_name, channel_index
    
    # Channel not found in any group
    return False, '', 0