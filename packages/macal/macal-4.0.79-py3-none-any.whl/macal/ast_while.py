#
# Product:   Macal
# Author:    Marco Caspers
# Date:      12-09-2022
#

from . import ast
from . import types
from . import ast_expr
from . import ast_block
from . import token


class While(ast.AST):
    def __init__(self, tok: token.LexToken, condition: ast_expr.Expr, blk: ast_block.Block) -> None:
        super().__init__(tok, types.AstType.While)
        self.Condition: ast_expr.Expr = condition
        self.Block: ast_block.Block = blk


    def __str__(self):
        return f'while {self.Condition} {self.__mask_linefeeds__(f"{self.Block}")}'