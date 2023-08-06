#
# Product:   Macal
# Author:    Marco Caspers
# Date:      07-09-2022
#

from enum import Enum

class LexTokenType(Enum):
    """Enum for lexer token types"""
    Operator = 0
    Identifier = 1
    Punctuation = 2
    Comment = 3
    String = 4
    Number = 5
    Whitespace = 6
    InterpolationStart = 7
    InterpolationEnd = 8
    InterpolationOp = 9
    Nil = 255




class AstType(Enum):
    """Enum for parser AST types"""
    AST = 0
    Expr = 1
    FunctionDefinition = 2
    FunctionCall = 3
    Block = 4
    Assignment = 5
    If = 6
    Elif = 7
    Else = 8
    Break = 9
    Continue = 10
    Halt = 11
    Select = 12
    SelectField = 13
    Foreach = 14
    While = 15
    Return = 16
    Include = 17




class ExprType(Enum):
    """Enum for Expression types"""
    Binary = 0
    Unary = 1
    Literal = 2
    Grouping = 3
    Variable = 4
    FunctionCall = 5
    FunctionArgument = 6
    VariableIndexStart = 7
    VariableIndex = 8
    NewArrayIndex = 9
    ArgumentList = 10
    InterpolationPart = 11
    Nil=255




class VariableType(Enum):
    """Enum for Variable value types"""
    Array = 0
    Bool = 1
    Int = 2
    Float = 3
    Function = 4
    Params = 5
    Record = 6
    String = 7
    Type = 8
    Variable = 9
    NewArrayIndex = 10
    FunctionDefinition = 11
    Nil = 255



