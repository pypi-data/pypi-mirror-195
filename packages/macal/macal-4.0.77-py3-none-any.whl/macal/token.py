#
# Product:   Macal
# Author:    Marco Caspers
# Date:      07-09-2022
#


from __future__ import annotations
import typing
import copy
from dataclasses import dataclass
from . import types
from . import location


@dataclass
class LexToken:
    Lexeme:   str
    Type:     types.LexTokenType
    Location: typing.Optional[location.SourceLocation]
    Start:    int
    Filename: str



    def __str__(self):
        if self.Start == -1:
            return ''
        s = self.Lexeme
        if isinstance(self.Lexeme, str):
            s = s.replace('\n','')
            s = s.replace('\t', '    ')
        t = f'{self.Type}, ' if self.Type is not None else ''
        l = f', {self.Location}' if self.Location is not None else ''
        a = f', {self.Start}' if self.Start >= 0 else ''
        return f"{t}'{s}'{l}{a}"



    def Clone(self):
        return copy.deepcopy(self)
    
