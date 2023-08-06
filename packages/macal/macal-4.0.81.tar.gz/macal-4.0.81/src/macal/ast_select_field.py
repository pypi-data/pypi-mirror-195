#
# Product:   Macal
# Author:    Marco Caspers
# Date:      13-09-2022
#

from . import ast
from . import token
from . import types
import typing

class SelectField(ast.AST):
    '''Contains the location in the source code.'''
    def __init__(self, tok: token.LexToken) -> None:
        super().__init__(tok, types.AstType.SelectField)
        self.As: typing.Optional[token.LexToken] = None



    def __repr__(self):
        return f'SelectField(tok={self.Token})'



    def __str__(self):
        sa = f' as {self.As.Lexeme}' if self.As is not None else ''
        return f'{self.Token.Lexeme}{sa}'



    @property
    def AsName(self) -> str:
        if self.As is None:
            return self.Token.Lexeme
        return self.As.Lexeme



    @property
    def Name(self) -> str:
        return self.Token.Lexeme
