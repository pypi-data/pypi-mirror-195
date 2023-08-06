#
# Product:   Macal
# Author:    Marco Caspers
# Date:      07-09-2022
#

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SourceLocation:
    """Contains the location in the source code."""
    Line: int
    Column: int

    def __repr__(self):
        return f"SourceLocation(line={self.Line}, column={self.Column})"

    def __str__(self):
        return f"@({self.Line}, {self.Column})"
