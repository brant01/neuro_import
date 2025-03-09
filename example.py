#!/usr/bin/env python
"""
Example usage of neuro_import library for loading RHS data.

This script demonstrates how to:
1. Load an Intan RHS file using the Rust-based importer
2. Access properties of the loaded RHS data

Note: This example uses files in the 'data' directory which is not included in
the package distribution. You'll need to provide your own RHS data files.
"""

import sys
import os
import glob

# Import the RHS file loader
from neuro_import import load_rhs_file


def find_sample_data():
    """
    Find sample RHS files in the data directory.
    
    Returns:
        str: Path to an RHS file if found, None otherwise
    """
    # Look for RHS files in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if not os.path.exists(data_dir):
        return None
        
    # Find all RHS files
    rhs_files = glob.glob(os.path.join(data_dir, '**', '*.rhs'), recursive=True)
    
    # Return the first one if any are found
    return rhs_files[0] if rhs_files else None


def main():
    # If a filename was provided as an argument, use that
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # Otherwise try to find a sample file in the data directory
        filename = find_sample_data()
        if not filename:
            print("No RHS file specified and no sample data found.")
            print("Usage: python example.py <path/to/file.rhs>")
            print("Or create a 'data' directory with RHS files for automatic detection.")
            return 1
    
    print(f"Loading file: {filename}")
    
    # Load the file using the Rust-based importer
    try:
        # This directly calls the Rust function through Python bindings
        result = load_rhs_file(filename)
    except Exception as e:
        print(f"Error loading file: {e}")
        return 1
    
    # Check if data was found in the file
    if not result.data_present:
        print("No data found in the file.")
        return 0
    
    # Print some basic information about the file
    print(f"\nReference channel: {result.reference_channel}")
    print(f"Sample rate: {result.frequency_parameters['amplifier_sample_rate']} Hz")
    print(f"Number of amplifier channels: {len(result.amplifier_channels)}")
    
    # Print some notes from the file if available
    if result.notes:
        print("\nNotes:")
        for key, value in result.notes.items():
            if value.strip():  # Only print non-empty notes
                print(f"  {key}: {value}")
    
    # Print information about the first channel if available
    if result.amplifier_channels:
        channel = result.amplifier_channels[0]
        print(f"\nFirst channel: {channel['custom_channel_name']}")
        
        # Print data dimensions if available
        if result.amplifier_data:
            print(f"Data shape: {len(result.amplifier_data)} channels x {len(result.amplifier_data[0])} samples")
            print(f"First few values: {result.amplifier_data[0][:5]}")
            print(f"Time (s): {result.t[:5]}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())