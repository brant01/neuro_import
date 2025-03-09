"""
Intan RHS file importer using Rust-based high-performance implementation.
"""

import numpy as np
from .base_importer import BaseImporter

# Import the Rust bindings for the intan_importer
try:
    from neuro_import import _intan_rhs
except ImportError:
    raise ImportError(
        "Could not import the Rust-based RHS importer. "
        "Make sure the neuro_import package is properly installed."
    )


class IntanRHSImporter(BaseImporter):
    """
    Importer for Intan RHS files using a Rust-based implementation.
    
    This importer provides a fast implementation for reading and parsing
    Intan RHS files using a Rust backend.
    """
    
    def load(self, filename):
        """
        Load an Intan RHS file using the Rust-based importer.
        
        Parameters
        ----------
        filename : str
            The path to the RHS file to load
            
        Returns
        -------
        tuple
            (result, data_present) where:
            - result is a dictionary containing all parsed data and metadata
            - data_present is a boolean indicating if data was found in the file
        """
        print(f"Loading RHS file: {filename}")
        
        # Call the Rust implementation to load the file
        rust_result = _intan_rhs.load_rhs_file(filename)
        
        # Convert the Rust result to a Python dictionary with the same structure
        # as the original importrhsutilities.py implementation
        result = {}
        data_present = rust_result.data_present
        
        # Convert header information
        self._convert_header(rust_result, result)
        
        # Convert data if present
        if data_present:
            self._convert_data(rust_result, result)
            
        return result, data_present
    
    def _convert_header(self, rust_result, result):
        """
        Convert header information from Rust result to Python dictionary.
        
        Parameters
        ----------
        rust_result : RustRHSResult
            The result from the Rust implementation
        result : dict
            The Python dictionary to populate
        """
        # This will be implemented to match the structure expected by the Python code
        # For now, we assume the Rust implementation returns fields that match
        # the format needed by the Python code
        
        # Copy frequency parameters
        result['frequency_parameters'] = rust_result.frequency_parameters
        
        # Copy channel information
        channel_types = [
            'amplifier_channels',
            'board_adc_channels',
            'board_dac_channels',
            'board_dig_in_channels',
            'board_dig_out_channels'
        ]
        
        for channel_type in channel_types:
            if hasattr(rust_result, channel_type) and getattr(rust_result, channel_type):
                result[channel_type] = getattr(rust_result, channel_type)
        
        # Copy notes
        result['notes'] = rust_result.notes
        
        # Copy reference channel
        result['reference_channel'] = rust_result.reference_channel
        
        # Copy stim parameters
        result['stim_parameters'] = rust_result.stim_parameters
        
        # Copy spike triggers if present
        if hasattr(rust_result, 'spike_triggers') and rust_result.spike_triggers:
            result['spike_triggers'] = rust_result.spike_triggers
    
    def _convert_data(self, rust_result, result):
        """
        Convert data from Rust result to Python dictionary.
        
        Parameters
        ----------
        rust_result : RustRHSResult
            The result from the Rust implementation
        result : dict
            The Python dictionary to populate
        """
        # Copy time data
        result['t'] = np.array(rust_result.t)
        
        # Copy various data types if they exist
        data_types = [
            'amplifier_data',
            'dc_amplifier_data',
            'stim_data',
            'compliance_limit_data',
            'charge_recovery_data',
            'amp_settle_data',
            'board_adc_data',
            'board_dac_data',
            'board_dig_in_data',
            'board_dig_out_data'
        ]
        
        for data_type in data_types:
            if hasattr(rust_result, data_type) and getattr(rust_result, data_type) is not None:
                result[data_type] = np.array(getattr(rust_result, data_type))