#
# Product:   Macal
# Author:    Marco Caspers
# Date:      12-09-2022
#

import typing
from . import ast
from . import types
from . import ast_expr
from . import token


class Assignment(ast.AST):
    def __init__(self, tok: token.LexToken, varIndex: typing.Optional[ast_expr.Expr], operator: token.LexToken) -> None:
        super().__init__(tok, types.AstType.Assignment)
        self.Variable: str = tok.Lexeme
        self.VarIndex: typing.Optional[ast_expr.Expr] = varIndex
        self.Operator: token.LexToken = operator
        self.Value: typing.Optional[ast_expr.Expr] = None
        self.isConst: bool = False

    
    def __str__(self):
        return f'{self.Variable} {self.Operator.Lexeme} {self.Value};'