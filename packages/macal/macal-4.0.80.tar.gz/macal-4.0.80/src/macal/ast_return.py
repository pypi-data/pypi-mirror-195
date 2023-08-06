#
# Product:   Macal
# Author:    Marco Caspers
# Date:      12-09-2022
#

from . import ast
from . import types
from . import token
from . import ast_expr

class Return(ast.AST):
    def __init__(self, tok: token.LexToken, val: ast_expr.Expr) -> None:
        super().__init__(tok, types.AstType.Return)
        self.Value: ast_expr.Expr = val



    def __repr__(self):
        return f'Return(tok={self.Token})'



    def __str__(self):
        return f'return;'