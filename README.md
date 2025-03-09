# NeuroImport

A lightweight Python wrapper for loading Intan RHS neurophysiology data files using a Rust backend.

## Features

- **High Performance**: Uses Rust for fast file parsing and data handling
- **Simple Interface**: Direct access to RHS file contents through a clean Python interface
- **Memory Efficient**: Optimized data structures to minimize memory usage

## Installation

```bash
pip install neuro_import
```

## Quick Start

```python
from neuro_import import load_rhs_file

# Load an RHS file
result = load_rhs_file("path/to/your/file.rhs")

# Check if data is present
if result.data_present:
    # Access header information
    print(f"Sample rate: {result.frequency_parameters['amplifier_sample_rate']} Hz")
    print(f"Number of channels: {len(result.amplifier_channels)}")
    
    # Access data
    if result.amplifier_data:
        # First channel, first 5 samples
        print(result.amplifier_data[0][:5])
        # Timestamps in seconds
        print(result.t[:5])
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

For development and testing:

1. Clone the repository
2. Place sample RHS files in the `data/` directory
3. Build the extension module:
   ```bash
   maturin develop
   # OR to build for release
   maturin build --release
   ```
4. Run the example script:
   ```bash
   python example.py
   ```

## Requirements

- Python 3.8+
- NumPy

## Performance

NeuroImport's Rust-based implementation offers significant performance improvements over pure Python implementations:

- Fast file loading with minimal memory overhead
- Efficient data processing and conversion

## License

This project is licensed under the MIT License - see the LICENSE file for details.