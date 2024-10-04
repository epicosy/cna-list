# cna-list
The CNA Loader is a Python module designed to load and validate CVE Numbering Authority (CNA) data from 
JSON files. This module uses the Pydantic library for data validation and supports loading data from both local and 
external directories.

## Installation
You can install the CNA Loader using pip.

```bash
pip install cna-list
```

## Usage

### Basic Usage
You can load CNA data by initializing the CNALoader class. By default, it will look for JSON files in the directory 
specified by the `CNA_DATA_PATH` environment variable.

```python
from cna_list import CNALoader

cna_loader = CNALoader()
```

You can also load CNA data from a specific directory by passing the path to the load method.

```python
from cna_list import CNALoader

cna_loader = CNALoader('/path/to/cna/data')
```

### Load from Specific File
You can load CNA data from a specific file by passing the path to the load_from_external method.

```python
from cna_list import CNALoader

cna = CNALoader.load_from_external('cna2.json')

print(cna)
```

## Testing
You can run the tests using the following command.

```bash
python -m unittest discover tests/
```
