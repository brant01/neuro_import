"""
NeuroImport: A Python wrapper for Rust-based RHS file loading

This package provides a high-performance interface for importing
Intan RHS neurophysiology data files using a Rust backend.
"""

__version__ = "0.1.0"

# Import the core functionality
from neuro_import import load_rhs_file

__all__ = ["load_rhs_file"]