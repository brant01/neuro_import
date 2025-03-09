"""
NeuroImport: Fast and flexible neurophysiology data import library

This package provides a high-performance interface for importing various
neurophysiology data formats, with an extensible architecture for adding
new file types.

Key components:
- File type detection and automatic importer selection
- Fast RHS file loading via Rust implementation
- Standardized data structures for neurophysiology data
- Processing utilities for common data transformations
"""

__version__ = "0.1.0"

from .core import load_file, print_all_channel_names, find_channel, plot_channel

__all__ = [
    "load_file",
    "print_all_channel_names",
    "find_channel",
    "plot_channel",
]