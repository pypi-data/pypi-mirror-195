#
# Product:   Macal
# Author:    Marco Caspers
# Date:      09-09-2022
#

from __future__ import annotations
import typing
from . import ast
from . import types
from . import token
from . import ast_expr
from . import value_item



class Expr(ast.AST):
    def __init__(self, tok: token.LexToken) -> None:
        super().__init__(tok, types.AstType.Expr)
        self.Left: typing.Any = None
        self.Operator: typing.Optional[token.LexToken] = None
        self.Right: typing.Any = None
        self.ExprType: types.ExprType = types.ExprType.Nil
        self.LiteralValueType: types.VariableType = types.VariableType.Nil
        self.Indexed: bool = False



    def Binary(self, left: typing.Union[token.LexToken, ast_expr.Expr, list], operator: token.LexToken, right: typing.Union[token.LexToken, ast_expr.Expr]) -> Expr:
        self.Left = left
        self.Operator = operator
        self.Right = right
        self.ExprType = types.ExprType.Binary
        return self
    


    def Unary(self, operator: token.LexToken, right: typing.Any) -> Expr:
        self.Right = right
        self.Operator = operator
        self.ExprType = types.ExprType.Unary
        return self


    
    def Literal(self, val: value_item.ValueItem) -> Expr:
        self.LiteralValueType = val.Type
        self.ExprType = types.ExprType.Literal
        return self



    def Grouping(self, left: Expr) -> Expr:
        self.Left = left
        self.ExprType = types.ExprType.Grouping
        return self

    

    def Variable(self, valType: types.VariableType) -> Expr:
        self.LiteralValueType = valType
        self.ExprType = types.ExprType.Variable
        return self



    def VariableIndex(self) -> Expr:
        self.ExprType = types.ExprType.VariableIndex
        return self



    def NewArrayIndex(self) -> Expr:
        self.ExprType = types.ExprType.NewArrayIndex
        return self



    def InterpolationPart(self, right: typing.Any) -> Expr:
        self.Right = right
        self.ExprType = types.ExprType.InterpolationPart
        return self



    def ArgumentList(self) -> Expr:
        self.ExprType = types.ExprType.ArgumentList
        self.Left = []
        return self



    def Argument(self, left: token.LexToken) -> Expr:
        self.Left = left
        self.ExprType = types.ExprType.FunctionArgument
        return self



    def __str__(self):
        s = self
        if self.Operator is not None:
            if self.ExprType == types.ExprType.Binary:
                s= f'Expr.Binary: {self.Left} {self.Operator.Lexeme} {self.Right}'
            if self.ExprType == types.ExprType.Unary:
                s= f'Expr.Unary: {self.Operator.Lexeme}{self.Right}'
        if self.ExprType == types.ExprType.InterpolationPart:
            s= f'Expr.InterpolationPart: {self.Right}'
        if self.ExprType == types.ExprType.VariableIndex:
            s= f'Expr.VariableIndex: \n L: {self.Left} \n R: {self.Right}]'
        if self.ExprType == types.ExprType.Variable:
            s= f'Expr.Variable: {self.Token.Lexeme}'
        if self.ExprType == types.ExprType.Grouping:
            s= f'Expr.Grouping: ({self.Left})'
        if self.ExprType == types.ExprType.Literal:
            s= f'Expr.Literal: {self.Token.Lexeme} (Type: {self.Token.Type})'
        if self.ExprType == types.ExprType.FunctionCall:
            s= f'Expr.FunctionCall: {self.Token.Lexeme}{self.Right}'
        if self.ExprType == types.ExprType.ArgumentList:
            s= f"Expr.ArgumentList: ({', '.join(f'{item}' for item in self.Left)})" # type: ignore
        if self.ExprType == types.ExprType.FunctionArgument:
            s= f"Expr.FunctionArgument: ({self.Left})"
        if self.ExprType == types.ExprType.NewArrayIndex:
            s= 'Expr.NewArrayIndex: []'
        if self.ExprType == types.ExprType.VariableIndexStart:
            s = 'Expr.VariableIndexStart: ['
        return s