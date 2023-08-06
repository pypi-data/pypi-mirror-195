#
# Product:   Macal
# Author:    Marco Caspers
# Date:      13-09-2022
#

import typing
from . import ast
from . import token
from . import types
from . import ast_expr
from . import ast_select_field

class Select(ast.AST):
    '''select [distinct] <field-list | *> from <expr> [where <expr>] [merge] into <expr>.'''
    def __init__(self, tok: token.LexToken, frm: ast_expr.Expr, into: ast_expr.Expr) -> None:
        super().__init__(tok, types.AstType.Select)
        self.Fields: typing.List[ast_select_field.SelectField] = []
        self.From: ast_expr.Expr = frm
        self.Into: ast_expr.Expr = into
        self.Where: typing.Optional[ast_expr.Expr] = None
        self.Distinct: bool = False
        self.Merge: bool = False



    def __repr__(self):
        return f'Select(tok={self.Token})'



    def __str__(self):
        distinct = 'distinct ' if self.Distinct else ''
        fields = ', '.join([f'{field}' for field in self.Fields])
        where = f' {self.Where}' if self.Where is not None else ''
        merge = ' merge ' if self.Merge else ''
        return f'select {distinct}{fields} from {self.From}{where}{merge} into {self.Into}'
