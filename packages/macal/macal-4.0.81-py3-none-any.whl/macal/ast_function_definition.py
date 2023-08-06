#
# Product:   Macal
# Author:    Marco Caspers
# Date:      12-09-2022
#

from __future__ import annotations
import typing
from . import ast
from . import types
from . import ast_expr
from . import ast_block
from . import token
from . import location


class FunctionDefinition(ast.AST):
    def __init__(self, tok: token.LexToken) -> None:
        super().__init__(tok, types.AstType.FunctionDefinition)
        self.Name: str = tok.Lexeme
        self.Arguments: typing.Optional[ast_expr.Expr] = None
        self.Block: typing.Optional[ast_block.Block] = None
        self.IsExternal: bool = False
        self.ExternalModule: typing.Optional[token.LexToken] = None
        self.ExternalFunction: typing.Optional[token.LexToken] = None



    def RegisterArgument(self, name: str) -> None:
        if self.Arguments is None:
            self.Arguments = ast_expr.Expr(
                token.LexToken('()', 
                    types.LexTokenType.Punctuation, 
                    self.Token.Location, -1, self.Token.Filename)).ArgumentList()
        if name == '': 
            return
        expr = ast_expr.Expr(
            token.LexToken(name, 
                types.LexTokenType.Identifier,
                None, -1, self.Token.Filename)).Variable(types.VariableType.Nil)
        self.Arguments.Left.append(expr)



    def __repr__(self):
        return f'FunctionDefinition(tok="{self.Token}")'



    def __str__(self):
        #a = ', '.join([f'{arg}' for arg in self.Arguments.Left])
        a = ', '.join([arg.Token.Lexeme for arg in self.Arguments.Left]) if self.Arguments is not None else ''
        s = f'{self.Name} => ({a})'
        if self.Block is not None:
            s = f'{s}{self.__mask_linefeeds__(f"{self.Block}")}'
        return s
