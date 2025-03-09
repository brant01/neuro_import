"""
Base importer class that defines the interface for all file importers.
"""

from abc import ABC, abstractmethod


class BaseImporter(ABC):
    """
    Abstract base class for all file importers.
    
    This class defines the interface that all importers must implement.
    """
    
    @abstractmethod
    def load(self, filename):
        """
        Load a file and return the parsed data.
        
        Parameters
        ----------
        filename : str
            The path to the file to load
            
        Returns
        -------
        tuple
            (result, data_present) where:
            - result is a dictionary containing all parsed data and metadata
            - data_present is a boolean indicating if data was found in the file
        """
        pass