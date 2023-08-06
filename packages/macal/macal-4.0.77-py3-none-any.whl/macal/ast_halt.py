#
# Product:   Macal
# Author:    Marco Caspers
# Date:      12-09-2022
#

from . import ast
from . import types
from . import token
from . import ast_expr

class Halt(ast.AST):
    def __init__(self, tok: token.LexToken, exitcode: ast_expr.Expr) -> None:
        super().__init__(tok, types.AstType.Halt)
        self.Exitcode: ast_expr.Expr = exitcode



    def __repr__(self):
        return f'Halt(tok={self.Token})'


    
    def __str__(self):
        return f'halt {self.Exitcode};'
