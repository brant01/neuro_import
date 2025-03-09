#!/usr/bin/env python3
"""
A simple script to test if we can find RHS files in the data directory.
"""

import os
import glob

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

if __name__ == "__main__":
    data_file = find_sample_data()
    if data_file:
        print(f"Found data file: {data_file}")
        print(f"File size: {os.path.getsize(data_file) / (1024*1024):.2f} MB")
    else:
        print("No data files found in the data directory.")