from typing import Union, List, Dict

# Defining data types constant
## Generic data types
NUMERIC = Union[int, float]
INT = int
FLOAT = float
STRING = str
BOOLEAN = bool

## Optional data types
OPTIONAL_NUMERIC = Union[NUMERIC, None]

## Specific data types
FLOWRATE_PRESSURE_SINGLE_DATA = Dict[NUMERIC, NUMERIC]
FLOWRATE_PRESSURE_DATA = List[FLOWRATE_PRESSURE_SINGLE_DATA]