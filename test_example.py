#!/usr/bin/env python3
"""
A simple script to test the example script's file finding logic.
"""

import os
import sys
from example import find_sample_data

def mock_load_file(filename):
    """Mock the load_file function to test the example script."""
    print(f"Would load file: {filename}")
    print(f"File size: {os.path.getsize(filename) / (1024*1024):.2f} MB")
    # Return a mock result and data_present
    return {"mock": "result"}, True

if __name__ == "__main__":
    # Override sys.argv if no arguments were provided
    if len(sys.argv) < 2:
        filename = find_sample_data()
        if not filename:
            print("No RHS file specified and no sample data found.")
            print("Usage: python test_example.py <path/to/file.rhs>")
            print("Or place RHS files in the data/ directory for automatic detection.")
            sys.exit(1)
    else:
        filename = sys.argv[1]
    
    print(f"Found file: {filename}")
    # Call our mock load_file function
    result, data_present = mock_load_file(filename)
    print(f"Data present: {data_present}")
    print("Test completed successfully!")