#!/usr/bin/env python
"""
Example usage of neuro_import library for loading and plotting RHS data.

This script demonstrates how to:
1. Load an Intan RHS file
2. List available channels
3. Plot data from a specific channel

Note: This example uses files in the 'data' directory which is not included in
the package distribution. You'll need to provide your own RHS data files.
"""

import sys
import os
import glob

# Import these conditionally so the file-finding function can be imported alone
# for testing without needing matplotlib or neuro_import installed
if __name__ == "__main__":
    import neuro_import as ni
    import matplotlib.pyplot as plt


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
    
    # Load the file
    try:
        result, data_present = ni.load_file(filename)
    except Exception as e:
        print(f"Error loading file: {e}")
        return 1
    
    # Check if data was found in the file
    if not data_present:
        print("No data found in the file.")
        return 0
    
    # Print all available channels
    print("\nAvailable channels:")
    ni.print_all_channel_names(result)
    
    # Plot a channel (if available)
    if 'amplifier_channels' in result and len(result['amplifier_channels']) > 0:
        channel_name = result['amplifier_channels'][0]['custom_channel_name']
        print(f"\nPlotting channel: {channel_name}")
        
        fig, ax = ni.plot_channel(channel_name, result)
        plt.title(f"Channel: {channel_name}")
        plt.show()
    else:
        print("\nNo amplifier channels found to plot.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())