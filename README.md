# Network file parser
A python package parsing gaia files. It takes a gaia file as input and parses the data in pandas data frames.

Example usage:

```python
from ElectricityNetworFileParser.GnfParser import GnfParser

gnf_parser = GnfParser("test.gnf")
gnf_parser.parse_file()

# To acces the dataframe of a single entity type
gnf_parser.data_frames["CABLE"]

# Write all data to a single excel file each tab in the excel file represents an entity in the gaia file
gnf_parser.write_all_data_frames()
```

## Installation

Create a new python environment and run the following command:

`pip install ElectricityNetworFileParser `
