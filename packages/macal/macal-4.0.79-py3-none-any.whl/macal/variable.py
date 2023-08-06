#
# Product:   Macal
# Author:    Marco Caspers
# Date:      15-09-2022
#

from __future__ import annotations
import copy
from dataclasses import dataclass
import typing
from . import types
from . import token
from . import value_item
from . import exceptions
from . import ast_function_definition


@dataclass
class Variable:
    Token: token.LexToken
    Name: str
    Value = None
    isConst: bool = False


    
    def GetValue(self) -> typing.Any:
        if self.Value is None:
            raise exceptions.RuntimeError(f"Debug: variable.getValue() self.Value is None.", self.Token.Location, self.Token.Filename)
        if self.Value.Type in [types.VariableType.String, types.VariableType.Int, types.VariableType.Float, types.VariableType.Bool, types.VariableType.Nil, types.VariableType.Variable, types.VariableType.Type]:
            return self.Value.Value
        if self.Value.Type == types.VariableType.Record:
            return self.MacalRecordToPythonValue(self.Value)
        if self.Value.Type == types.VariableType.Array:
            return self.MacalArrayToPythonValue(self.Value)
        if self.Value.Type == types.VariableType.Function:
            return self.MacalFunctionToPythonValue(self.Value)
        raise exceptions.RuntimeError(f"getValue() for type {self.Value.Type} Not implemented.", self.Token.Location, self.Token.Filename)



    def GetFunction(self) -> typing.Optional[ast_function_definition.FunctionDefinition]:
        if self.Value is None:
            raise exceptions.RuntimeError(f"Debug: variable.getFunction() self.Value is None.", self.Token.Location, self.Token.Filename)
        #print(self)
        if self.Value.Type == types.VariableType.Function:
            return self.Value.Value
        return None



    def MacalRecordToPythonValue(self, val: value_item.ValueItem) -> typing.Any:
        res = {}
        check = [types.VariableType.String, types.VariableType.Int, types.VariableType.Float, types.VariableType.Bool, types.VariableType.Nil, types.VariableType.Type]
        for (k, v) in val.Value.items():
            if v.Type in check:
                res[k] = v.Value
            elif v.Type == types.VariableType.Record:
                res[k] = self.MacalRecordToPythonValue(v)
            elif v.Type == types.VariableType.Array:
                res[k] = self.MacalArrayToPythonValue(v)
            elif v.Type == types.VariableType.Function:
                res[k] = self.MacalFunctionToPythonValue(v)
            else:
                raise exceptions.RuntimeError(f"getValue() for type {v.Type} Not implemented.", v.Token.Location, v.Token.Filename)
        return res



    def MacalFunctionToPythonValue(self, val: value_item.ValueItem) -> str:
        func = val.Value
        params = ', '.join([f'{arg.Token.Lexeme}' for arg in func.Arguments])
        return f'<Macal function: {func.Name}({params})>'



    def MacalArrayToPythonValue(self, val: value_item.ValueItem) -> typing.Any:
        res = []
        for v in val.Value:
            if v.Type in [types.VariableType.String, types.VariableType.Int, types.VariableType.Float, types.VariableType.Bool, types.VariableType.Nil, types.VariableType.Type]:
                res.append(v.Value)
            elif v.Type == types.VariableType.Record:
                res.append(self.MacalRecordToPythonValue(v))
            elif v.Type == types.VariableType.Array:
                res.append(self.MacalArrayToPythonValue(v))
            elif v.Type == types.VariableType.Function:
                res.append(self.MacalFunctionToPythonValue(v))
            else:
                raise exceptions.RuntimeError(f"getValue() for type {v.Type} Not implemented.", v.Token.Location, v.Token.Filename)
        return res



    def GetType(self) -> types.VariableType:
        if self.Value is None:
            raise exceptions.RuntimeError(f"Debug: variable.getType(): self.Value is None.", self.Token.Location, self.Token.Filename)
        return self.Value.Type



    def SetValue(self, value: typing.Any) -> None:
        if self.Value is None:
            #print("Debug: variable.setValue: self.Value is None.")
            return None
        self.Value = self.Value.ConvertFromPython(self.Token, value)        


    
    def __str__(self) -> str:
        return f'{self.Name} = {self.Value}'



    def Clone(self):
        return copy.deepcopy(self)

