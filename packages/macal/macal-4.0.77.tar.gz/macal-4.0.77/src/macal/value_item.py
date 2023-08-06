#
# Product:   Macal
# Author:    Marco Caspers
#
# Description:
#

from __future__ import annotations
from dataclasses import dataclass
import typing
import copy
from . import token
from . import types
from . import exceptions
from . import ast_function_definition
from . import variable

@dataclass
class ValueItem:
    Token: token.LexToken
    Type: types.VariableType = types.VariableType.Nil
    Value: typing.Any = None
    

    def ConvertFromPython(self, tok: typing.Optional[token.LexToken], value: typing.Any) -> ValueItem:
        if tok is None:
            tok = self.Token
        self.Token = tok
        self.Type = self.GetTypeFromPythonValue(value)
        self.Value = self.GetValueFromPythonValue(value).Value
        return self
   

    def GetTypeFromPythonValue(self, value: typing.Any) -> types.VariableType:
        if value is None:
            return types.VariableType.Nil
        elif type(value) is str:
            return types.VariableType.String
        elif type(value) is int:
            return types.VariableType.Int
        elif type(value) is float:
            return types.VariableType.Float
        elif type(value) is bool:
            return types.VariableType.Bool
        elif type(value) is list:
            return types.VariableType.Array
        elif type(value) is dict:
            return types.VariableType.Record
        # this one is here for set return value from an external library.
        elif isinstance(value, variable.Variable):
            return types.VariableType.Variable
        # this one is here for set return value from an external library.
        elif isinstance(value, ast_function_definition.FunctionDefinition):
            return types.VariableType.Function
        elif isinstance(value, types.VariableType):
            return types.VariableType.Type
        else:
            raise exceptions.RuntimeError(f"getTypeFromPythonValue() for type {type(value)} Not implemented.", self.Token.Location, self.Token.Filename)



    def GetValueFromPythonValue(self, val: typing.Any) -> ValueItem:
        if val is None:
            return ValueItem(self.Token, types.VariableType.Nil, types.VariableType.Nil.name.lower())
        elif type(val) is str:
            return ValueItem(self.Token, types.VariableType.String, val)
        elif type(val) is int:
            return ValueItem(self.Token, types.VariableType.Int, val)
        elif type(val) is float:
            return ValueItem(self.Token, types.VariableType.Float, val)
        elif type(val) is bool:
            return ValueItem(self.Token, types.VariableType.Bool, val)
        elif type(val) is dict:
            return self.FromPythonDict(val)
        elif type(val) is list:
            return self.FromPythonList(val)
        # this one is here for set return value from an external library.
        elif isinstance(val, variable.Variable):
            return ValueItem(self.Token, types.VariableType.Variable, val)
        # this one is here for set return value from an external library.
        elif isinstance(val, ast_function_definition.FunctionDefinition):
            return ValueItem(self.Token, types.VariableType.Function, val)
        elif isinstance(val, types.VariableType):
            self.Token.Lexeme = val.name
            self.Token.Type = types.LexTokenType.Identifier
            return ValueItem(self.Token, types.VariableType.Function, val)
        elif isinstance(val, ValueItem):
            raise exceptions.RuntimeError("Invalid ValueItem value. Value is ValueItem, this is a bug that should be fixed.", self.Token.Location, self.Token.Filename)           
        else:
            raise exceptions.RuntimeError(f"GetValueFromPythonValue() for type {type(val)} Not implemented.", self.Token.Location, self.Token.Filename)



    def FromPythonList(self, val: list) -> ValueItem:
        res = []
        for v in val:
            res.append(self.GetValueFromPythonValue(v))
        return ValueItem(self.Token, types.VariableType.Array, res)



    def FromPythonDict(self, val: dict) -> ValueItem:
        res = {}
        for (k, v) in val.items():
            res[k] = self.GetValueFromPythonValue(v)
        return ValueItem(self.Token, types.VariableType.Record, res)



    def SetValue(self, tok: token.LexToken, type: types.VariableType) -> None:
        self.Token = tok
        self.Type = type
        if self.Type == types.VariableType.Int:
            self.Value = int(tok.Lexeme)
        elif self.Type == types.VariableType.Float:
            self.Value = float(tok.Lexeme)
        elif self.Type == types.VariableType.Bool:
            self.Value = tok.Lexeme == 'true'
        elif self.Type == types.VariableType.String:
            self.Value = tok.Lexeme
        elif self.Type == types.VariableType.Array:
            self.Value = tok.Lexeme
        elif self.Type == types.VariableType.Record:
            self.Value = tok.Lexeme
        elif self.Type == types.VariableType.Nil:
            self.Value = types.VariableType.Nil.name.lower()
        else:
            raise exceptions.RuntimeError(f"Invalid value type ({self.Type}).", tok.Location, tok.Filename)



    def __eq__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'EQ: Other is not a ValueItem ({type(other)}).', self.Token.Location , self.Token.Filename)
        if self.Type == types.VariableType.Nil and self.Value != types.VariableType.Nil.name.lower():
            raise exceptions.RuntimeError(f'EQ: Self is nil type but not nil value.', self.Token.Location, self.Token.Filename)
        if other.Type == types.VariableType.Nil and other.Value != types.VariableType.Nil.name.lower():
            raise exceptions.RuntimeError(f'EQ: Other is nil type but not nil value.', other.Token.Location, other.Token.Filename)
        tok = self.Token.Clone()
        val = self.Value == other.Value
        tok.Lexeme = 'true' if val else 'false'
        tok.Type = types.LexTokenType.Identifier
        return ValueItem(tok, types.VariableType.Bool, val)


    
    def __add__(self, other) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'ADD: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), 
            types.VariableType.Float if self.Type == types.VariableType.Int and other.Type == types.VariableType.Float else self.Type,
            self.Value + other.Value)
        res.Token.Lexeme = f'{res.Value}'
        return res



    def __sub__(self, other: ValueItem):
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'SUB: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), 
            types.VariableType.Float if self.Type == types.VariableType.Int and other.Type == types.VariableType.Float else self.Type,
            self.Value - other.Value)
        res.Token.Lexeme = f'{res.Value}'
        return res



    def __mul__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'MUL: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), 
            types.VariableType.Float if self.Type == types.VariableType.Int and other.Type == types.VariableType.Float else self.Type,
            self.Value * other.Value)
        res.Token.Lexeme = f'{res.Value}'
        return res



    def __pow__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'POW: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), 
            types.VariableType.Float if self.Type == types.VariableType.Int and other.Type == types.VariableType.Float else self.Type,
            self.Value ** other.Value)
        res.Token.Lexeme = f'{res.Value}'
        return res



    def __mod__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'MOD: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        if other.Value == 0 or other.Value == 0.0:
            raise exceptions.RuntimeError(f"Division by zero.", other.Token.Location, other.Token.Filename)
        res = ValueItem(self.Token.Clone(), 
            types.VariableType.Int,
            self.Value % other.Value)
        res.Token.Lexeme = f'{res.Value}'
        return res



    def __truediv__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'DIV: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        if other.Value == 0 or other.Value == 0.0:
            raise exceptions.RuntimeError(f"Division by zero.", other.Token.Location, other.Token.Filename)
        res = ValueItem(self.Token.Clone(), types.VariableType.Float, self.Value / other.Value)
        res.Token.Lexeme = f'{res.Value}'
        return res



    def __gt__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'GT: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), types.VariableType.Bool, self.Value > other.Value)
        res.Token.Lexeme = 'true' if res.Value else 'false'
        res.Token.Type = types.LexTokenType.Identifier
        return res
    


    def __lt__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'LT: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), types.VariableType.Bool, self.Value < other.Value)
        res.Token.Lexeme = 'true' if res.Value else 'false'
        res.Token.Type = types.LexTokenType.Identifier
        return res


    
    def __ge__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'GTE: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), types.VariableType.Bool, self.Value >= other.Value)
        res.Token.Lexeme = 'true' if res.Value else 'false'
        res.Token.Type = types.LexTokenType.Identifier
        return res



    def __le__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'LTE: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), types.VariableType.Bool, self.Value <= other.Value)
        res.Token.Lexeme = 'true' if res.Value else 'false'
        res.Token.Type = types.LexTokenType.Identifier
        return res



    def __ne__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'NE: Other is not a ValueItem ({type(other)}) self: {self} other: {other}', self.Token.Location, self.Token.Filename)
        if self.Type == types.VariableType.Nil and self.Value != types.VariableType.Nil.name.lower():
            raise exceptions.RuntimeError(f'NE: Self is nil type but not nil value. self:', self.Token.Location, self.Token.Filename)
        if other.Type == types.VariableType.Nil and other.Value != types.VariableType.Nil.name.lower():
            raise exceptions.RuntimeError(f'NE: Other is nil type but not nil value.', other.Token.Location, other.Token.Filename)
        res = ValueItem(self.Token.Clone(), types.VariableType.Bool, self.Value != other.Value)
        res.Token.Lexeme = 'true' if res.Value else 'false'
        res.Token.Type = types.LexTokenType.Identifier
        return res



    def __and__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'AND: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), types.VariableType.Bool, self.Value and other.Value)
        res.Token.Lexeme = 'true' if res.Value else 'false'
        res.Token.Type = types.LexTokenType.Identifier
        return res



    def __or__(self, other: ValueItem) -> ValueItem:
        if not isinstance(other, ValueItem):
            raise exceptions.RuntimeError(f'OR: Other is not a ValueItem ({type(other)}).', self.Token.Location, self.Token.Filename)
        res = ValueItem(self.Token.Clone(), types.VariableType.Bool, self.Value or other.Value)
        res.Token.Lexeme = 'true' if res.Value else 'false'
        res.Token.Type = types.LexTokenType.Identifier
        return res


    
    def Clone(self) -> ValueItem:
        return copy.deepcopy(self)



    def __str__(self) -> str:
        res = f'ValueItem(token={self.Token}, type={self.Type}, value='
        if self.Type == types.VariableType.Array:
            if not isinstance(self.Value, list):
                 raise exceptions.RuntimeError(f'self.Type is Array, but self.Value is not. ({type(self.Value)}).', self.Token.Location, self.Token.Filename)
            res = f'{res}[\n'
            for v in self.Value:
                res = f'{res}    {v}\n'
            res = f'{res}]);'
        elif self.Type == types.VariableType.Record:
            if not isinstance(self.Value, dict):
                 raise exceptions.RuntimeError(f'self.Type is Record, but self.Value is not. ({type(self.Value)} (self.Value: {self.Value}))', self.Token.Location, self.Token.Filename)
            res = f'{res}{{\n'
            for (k,v) in self.Value.items():
                res = f'{res}    "{k}":{v}\n'
            res = f'{res}}});'
        else:
            res = f'{res}{self.Value});'
        return res
