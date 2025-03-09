"""
Utility functions for neurophysiology data processing.
"""

from .channel_utils import (
    print_names_in_group,
    find_channel_in_group,
    find_channel_in_header
)

from .filter_utils import notch_filter

from .signal_utils import (
    scale_timestamps,
    scale_amplifier_data,
    scale_stim_data,
    scale_dc_amplifier_data,
    scale_board_adc_data,
    scale_board_dac_data,
    extract_digital_data,
    extract_stim_data,
    apply_notch_filter_to_data
)

__all__ = [
    # Channel utilities
    'print_names_in_group',
    'find_channel_in_group',
    'find_channel_in_header',
    
    # Filter utilities
    'notch_filter',
    
    # Signal processing utilities
    'scale_timestamps',
    'scale_amplifier_data',
    'scale_stim_data',
    'scale_dc_amplifier_data',
    'scale_board_adc_data',
    'scale_board_dac_data',
    'extract_digital_data',
    'extract_stim_data',
    'apply_notch_filter_to_data'
]