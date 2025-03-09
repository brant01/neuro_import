# NeuroImport

A fast and flexible Python library for importing neurophysiology data, built on Rust.

## Features

- **High Performance**: Uses Rust for fast file parsing and data handling
- **File Format Detection**: Automatically selects the appropriate importer based on file extension
- **Extensible**: Designed to easily support additional file formats 
- **Pythonic Interface**: Clean, well-documented API with NumPy integration

## Currently Supported Formats

- Intan RHS files (.rhs) - Using a custom Rust implementation for speed

## Installation

```bash
pip install neuro_import
```

## Quick Start

```python
import neuro_import as ni
import matplotlib.pyplot as plt

# Load a file
result, data_present = ni.load_file("path/to/your/file.rhs")

# Print all channel names
ni.print_all_channel_names(result)

# Plot a specific channel
fig, ax = ni.plot_channel("channel_name", result)
plt.show()
```

## Example Usage

The package includes an example script that demonstrates basic usage:

```bash
# Run with your own data file
python example.py /path/to/your/file.rhs

# Or place data files in the data/ directory and run without arguments
python example.py
```

## Development and Testing

For development and testing, you can store sample data files in the `data/` directory. 
This directory is excluded from version control and package distribution.

## Python Requirements

- Python 3.8+
- NumPy
- Matplotlib

## Performance

NeuroImport's Rust-based implementation offers significant performance improvements over pure Python implementations:

- Faster file loading 
- Reduced memory overhead
- Efficient data processing

## Documentation

For full documentation, visit [neuro-import.readthedocs.io](https://neuro-import.readthedocs.io).

## Contributing

Contributions are welcome! If you'd like to add support for additional file formats or improve the existing code, please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.