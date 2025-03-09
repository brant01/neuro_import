"""
File type registry that maps file extensions to importers.

This module provides a registry for file importers and functions to
get the appropriate importer for a given file type.
"""

from .base_importer import BaseImporter
from .intan_rhs_importer import IntanRHSImporter

# Registry of file extensions to importers
_IMPORTERS = {
    '.rhs': IntanRHSImporter(),
    # Add more importers as they become available
    # '.ext': ImporterClass(),
}


def register_importer(extension: str, importer: BaseImporter):
    """
    Register a new importer for a file extension.
    
    Parameters
    ----------
    extension : str
        The file extension (including the dot, e.g., '.ext')
    importer : BaseImporter
        The importer instance to use for this file type
    """
    global _IMPORTERS
    _IMPORTERS[extension.lower()] = importer


def get_importer_for_file(extension: str) -> BaseImporter:
    """
    Get the appropriate importer for a file extension.
    
    Parameters
    ----------
    extension : str
        The file extension (including the dot, e.g., '.ext')
        
    Returns
    -------
    BaseImporter or None
        The importer for this file type, or None if no importer is registered
    """
    return _IMPORTERS.get(extension.lower())