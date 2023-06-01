from enum import Enum

class Comp(Enum):
    """Enumeration of the different methods of analysis"""
    RANDOM = 1
    MANUAL = 2

class Round(Enum):
    """Enumeration of the different strategies of analysis"""
    MANUAL = 1
    AL = 2

    