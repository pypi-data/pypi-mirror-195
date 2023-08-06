#
# Product:   Macal
# Author:    Marco Caspers
# Date:      09-09-2022
#

import typing
from . import __about__
from . import token
from . import ast
from . import ast_expr
from . import ast_function_definition
from . import ast_function_call
from . import ast_block
from . import ast_assignment
from . import ast_if
from . import ast_foreach
from . import ast_break
from . import ast_continue
from . import ast_halt
from . import ast_while
from . import ast_return
from . import ast_include
from . import ast_select_field
from . import ast_select
from . import value_item
from . import types
from . import exceptions


class Parser:
    def __init__(self) -> None:
        self.version: str = __about__.__version__
        self.source: typing.List[token.LexToken]
        self.filename: str
        self.length = 0



    def Current(self, index: int) -> typing.Optional[token.LexToken]:
        if index < self.length:
            return self.source[index]
        return None



    def Next(self, index: int) -> typing.Tuple[int, typing.Optional[token.LexToken]]:
        index += 1
        if index >= 0 and index < self.length:
            return (index, self.source[index])
        return (index, None)



    def Peek(self, index: int, offset: int) -> typing.Optional[token.LexToken]:
        if index + offset < self.length and index+offset >= 0:
            return self.source[index+offset]
        return None



    def Previous(self, index: int) -> token.LexToken:
        peek = self.Peek(index, -1)
        if peek is None:
            raise exceptions.ParserError(f"Peek, Index ({index}) out of bounds.", None, self.filename)
        return peek



    def Match(self, index: int, type: types.LexTokenType, lex: typing.Union[typing.Optional[str], list]) -> typing.Tuple[int, bool, typing.Optional[token.LexToken]]:
        current = self.Current(index)
        if current is None:
            return (index, False, current)
        if current.Type == type:
            if lex is None:
                (index, _) = self.Next(index)
                return (index, True, current)
            if isinstance(lex, str):
                if current.Lexeme == lex:
                    (index, _) = self.Next(index)
                    return (index, True, current)
                return (index, False, current)
            if current.Lexeme in lex:
                (index, _) = self.Next(index)
                return (index, True, current)
        return (index, False, current)



    def Consume(self, index: int, message: str, type: types.LexTokenType, lex: typing.Optional[str] = None) -> int:
        (index, match, current) = self.Match(index, type, lex)
        if not match:
            if current is None:
                raise exceptions.ParserError(message = f'{message} ({type}, {lex})', loc = None ,filename = self.filename)
            else:
                raise exceptions.ParserError(message = f'{message} ({type}, {current.Type}, {lex}, {current.Lexeme})', loc = current.Location ,filename = self.filename)
        return index



    def Reset(self) -> None:
        self.source = []
        self.length = 0



    def Parse(self, source: typing.List[token.LexToken], filename: str) -> typing.List[ast.AST]:
        if source is None or (isinstance(source, list) and len(source) == 0):
            raise exceptions.ParserError(message = "No source to parse.", loc = None, filename = filename)
        # we remove whitespace and comments because they have no syntactic meaning.
        # This means that we can end up with an empty list in case there was only whitespace and/or comments, but that is not a problem.
        self.source = [token for token in source if token.Type is not types.LexTokenType.Whitespace and token.Type is not types.LexTokenType.Comment]
        self.filename = filename
        self.length = len(self.source)
        index = 0
        instructions = []
        while index < self.length:
            (index, instruction) = self.ParseInstruction(index)
            if instruction is not None:
                instructions.append(instruction)
        return instructions



    def Expression(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, expr) = self.Boolean(index, inFnDef)
        return (index, expr)



    def Boolean(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, expr) = self.Equality(index, inFnDef)
        (index, match, operator) = self.Match(index, types.LexTokenType.Identifier, ['and', 'or'])
        while match and operator is not None:
            (index, right) = self.Equality(index, inFnDef)
            expr = ast_expr.Expr(self.Previous(index)).Binary(expr, operator, right)
            (index, match, operator) = self.Match(index, types.LexTokenType.Identifier, ['and', 'or'])
        return (index, expr)



    def Equality(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, expr) = self.Comparison(index, inFnDef)
        (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['!=', '=='])
        while match and operator is not None:
            (index, right) = self.Comparison(index, inFnDef)
            expr = ast_expr.Expr(self.Previous(index)).Binary(expr, operator, right)
            (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['!=', '=='])
        return (index, expr)


    
    def Comparison(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, expr) = self.Term(index, inFnDef)
        (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['<=', '<', '>', '>='])
        while match and operator is not None:
            (index, right) = self.Term(index, inFnDef)
            expr = ast_expr.Expr(self.Previous(index)).Binary(expr, operator, right)
            (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['<=', '<', '>', '>='])
        return (index, expr)



    def Term(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, expr) = self.Factor(index, inFnDef)
        (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['+', '-'])
        while match and operator is not None:
            (index, right) = self.Factor(index, inFnDef)
            expr = ast_expr.Expr(self.Previous(index)).Binary(expr, operator, right)
            (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['+', '-'])
        return (index, expr)



    def Factor(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, expr) = self.PowerOrModulo(index, inFnDef)
        (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['/', '*'])
        while match and operator is not None:
            (index, right) = self.PowerOrModulo(index, inFnDef)
            expr = ast_expr.Expr(self.Previous(index)).Binary(expr, operator, right)
            (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['/', '*'])
        return (index, expr)



    def PowerOrModulo(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, expr) = self.Interpolate(index, inFnDef)
        (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['^', '%'])
        while match and operator is not None:
            (index, right) = self.Interpolate(index, inFnDef)
            expr = ast_expr.Expr(self.Previous(index)).Binary(expr, operator, right)
            (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['^', '%'])
        return (index, expr)



    def Interpolate(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, match, left) = self.Match(index, types.LexTokenType.InterpolationStart, '$')
        if match and left is not None:
            operator = token.LexToken('$+', types.LexTokenType.InterpolationOp, left.Location, index, self.filename)
            (index, expr) = self.Unary(index, inFnDef) # we may need to revert back to skipping unary and going straight to primary, 
                                                       # but i think we need to preserve the structure of the algorithm.
            (index, match, _) = self.Match(index, types.LexTokenType.InterpolationEnd, '$')
            while not match:
                (index, right) = self.Expression(index, inFnDef) # This is very tricky, going all the way back up to expression.
                expr = ast_expr.Expr(right.Token).Binary(expr, operator, right)
                (index, match, _) = self.Match(index, types.LexTokenType.InterpolationEnd, '$')
            result = ast_expr.Expr(left).InterpolationPart(expr)
            if result.Right.ExprType != types.ExprType.Binary:
                raise exceptions.ParserError("Interpolation string doesn't contain interpolation.", expr.Token.Location, self.filename)
            return (index, result)
        (index, expr) = self.Unary(index, inFnDef)
        return (index, expr)

    

    def Unary(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, match, operator) = self.Match(index, types.LexTokenType.Operator, ['!', '+', '-'])
        if not match:
            (index, match, operator) = self.Match(index, types.LexTokenType.Identifier, ['not'])
        if match and operator is not None:
            (index, right) = self.Primary(index, inFnDef)
            expr = ast_expr.Expr(self.Previous(index)).Unary(operator, right)
            return (index, expr)
        (index, expr) = self.Primary(index, inFnDef)
        return (index, expr)



    def Grouping(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, expr) = self.Expression(index, inFnDef)
        index = self.Consume(index, 'Unbalanced grouping, ")" expected.', types.LexTokenType.Punctuation, ')')
        expr = ast_expr.Expr(self.Previous(index)).Grouping(expr)
        return (index, expr)



    def Primary(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, match, tok) = self.Match(index, types.LexTokenType.Identifier, ['true', 'false'])
        if match and tok is not None:
            expr = ast_expr.Expr(tok).Literal(value_item.ValueItem(tok, types.VariableType.Bool, tok.Lexeme == 'true'))
            return (index, expr)
        (index, match, tok) = self.Match(index, types.LexTokenType.String, None)
        if match and tok is not None:
            expr = ast_expr.Expr(tok).Literal(value_item.ValueItem(tok, types.VariableType.String, tok.Lexeme))
            return (index, expr)
        (index, match, literal) = self.Match(index, types.LexTokenType.Number, None)
        if match and literal is not None:
            valType = types.VariableType.Int
            if '.' in literal.Lexeme:
                valType = types.VariableType.Float
                val = float(literal.Lexeme)
            else:
                val = int(literal.Lexeme)
            expr = ast_expr.Expr(literal).Literal(value_item.ValueItem(literal, valType, val))
            return (index, expr)
        (index, match, tok) = self.Match(index, types.LexTokenType.Identifier, 'nil')
        if match and tok is not None:
            expr = ast_expr.Expr(self.Previous(index)).Literal(value_item.ValueItem(tok, types.VariableType.Nil, types.VariableType.Nil.name.lower()))
            return (index, expr)
        (index, match, tok) = self.Match(index, 
                types.LexTokenType.Identifier, 
                [
                    'params',
                    'variable',
                    'any',
                    'string',
                    'int',
                    'float',
                    'bool',
                    'record',
                    'array',
                    'function'
                ])
        if inFnDef is True and match:
            (index, expr) = self.Argument(index)
            return (index, expr)
        elif match and tok is not None:
            if tok.Lexeme == 'array':
                expr = ast_expr.Expr(tok).Literal(value_item.ValueItem(tok, types.VariableType.Array, []))
                return (index, expr)
            elif tok.Lexeme == 'record':
                expr = ast_expr.Expr(tok).Literal(value_item.ValueItem(tok, types.VariableType.Record, {}))
                return (index, expr)
            else:
                raise exceptions.ParserError(message = f'Invalid use of reserved word. ({tok.Lexeme})', loc=tok.Location, filename=self.filename)       
        (index, match, _) = self.Match(index, types.LexTokenType.Identifier, None)
        if match:
            (index, expr) = self.FunctionCallOrVariable(index)
            return (index, expr)
        # grouping needs to be the last match, because technically a function call is also a grouping..
        (index, match, current) = self.Match(index, types.LexTokenType.Punctuation, '(')
        if match:
            (index, expr) = self.Grouping(index)
            return (index, expr)        
        if current is None:
            raise exceptions.ParserError(f'Unexpected nil in expression.', None, self.filename)            
        raise exceptions.ParserError(message = f'Unexpected token ("{current.Lexeme}") in expression.', loc = current.Location, filename = self.filename)



    def ValidateReservedWords(self, tok: token.LexToken) -> None:
        if tok.Lexeme in ['params', 'variable', 'int', 'bool', 'float', 'function', 'array', 'record', 'nil', 'any', 'string']:
            raise exceptions.ParserError(message = f'Invalid use of reserved word. ({tok.Lexeme})', loc=tok.Location, filename=self.filename)



    def Argument(self, index: int) -> typing.Tuple[int, ast_expr.Expr]:
        tok = self.Previous(index)
        (index, match, arg) = self.Match(index, types.LexTokenType.Identifier, None)
        if match and arg is not None:
            expr = ast_expr.Expr(tok).Argument(arg)
            return (index, expr)
        self.ValidateReservedWords(tok)
        raise exceptions.ParserError(message = f'Function argument definition requires an identifier. ({self.Current(index).Type})', loc=tok.Location, filename=self.filename) # type: ignore



    def GetVariableIndexer(self, index: int) -> typing.Tuple[int, ast_expr.Expr]:
        (index, match, open) = self.Match(index, types.LexTokenType.Punctuation, '[')
        if not match or open is None:
            raise exceptions.ParserError('Invalid call to GetVariableIndexer, no open bracket found.', None, filename=self.filename)
        expr = ast_expr.Expr(open).VariableIndex()
        expr.Left = []
        (index, match, close) = self.Match(index, types.LexTokenType.Punctuation, ']')
        if match and close is not None:
            expr.Left.append(ast_expr.Expr(close).NewArrayIndex())
            return (index, expr)
        match = True
        while match:
            (index, match, close) = self.Match(index, types.LexTokenType.Punctuation, ']')
            if match and close is not None:
                expr.Left.append(ast_expr.Expr(close).NewArrayIndex())
                return (index, expr)
            (index, left) = self.Expression(index)
            expr.Left.append(left)
            (index, match, close) = self.Match(index, types.LexTokenType.Punctuation, ']')
            if not match:
                raise exceptions.ParserError(message = 'Unbalanced brackets, expected "]".', loc=self.Previous(index).Location, filename=self.filename)
            (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '[')
        return (index, expr)



    def FunctionCallArgumentList(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        (index, match, open) = self.Match(index, types.LexTokenType.Punctuation, '(')
        if not match or open is None:
            raise exceptions.ParserError(message='Missing parenthesis, expected "(".', loc=self.Previous(index).Location,filename = self.filename)
        expr = ast_expr.Expr(open).ArgumentList()
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, ')')
        while not match and index < self.length:
            (index, left) = self.Expression(index, inFnDef)
            expr.Left.append(left)
            (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, ',')
            if match:
                (index, match, close) = self.Match(index, types.LexTokenType.Punctuation, ')')
                if match and close is not None:
                    raise exceptions.ParserError(message='Unexpected ")", expected expression after comma (",").', loc=close.Location,filename = self.filename)
            else:
                (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, ')')
        if not match:
            raise exceptions.ParserError(message='Unbalanced parenthesis, expected ")".', loc=expr.Token.Location, filename = self.filename)
        return (index, expr)



    def FunctionCallOrVariable(self, index: int, inFnDef: bool = False) -> typing.Tuple[int, ast_expr.Expr]:
        expr = ast_expr.Expr(self.Previous(index)) # the identifier.
        current = self.Current(index)
        if current is not None and current.Lexeme == '[':
            (index, varIndex) = self.GetVariableIndexer(index)
            expr.Indexed = True
            expr.Left = varIndex
        current = self.Current(index)
        if current is not None and current.Lexeme == '(':
            expr.ExprType = types.ExprType.FunctionCall
            (index, expr.Right) = self.FunctionCallArgumentList(index, inFnDef)
        else:
            expr.ExprType = types.ExprType.Variable
        return (index, expr)



    def ParseFunctionDefinition(self, index, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        instruction = ast_function_definition.FunctionDefinition(identifier)
        (index, instruction.Arguments) = self.FunctionCallArgumentList(index=index, inFnDef = True)
        (index, match, _) = self.Match(index, types.LexTokenType.Identifier, 'external')
        if match:
            instruction.IsExternal = True
            index = self.Consume(index=index, message = "Expected module name in external.", type = types.LexTokenType.String)
            instruction.ExternalModule = self.Previous(index)
            index = self.Consume(index, 'Expected ","', types.LexTokenType.Punctuation, ',')
            index = self.Consume(index=index, message = "Expected function name in external.", type = types.LexTokenType.String)
            instruction.ExternalFunction = self.Previous(index)
            index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
            return(index, instruction)
        (index, instruction.Block) = self.ParseBlock(index)
        return (index, instruction)



    def ParseFunctionCall(self, index, identifier: token.LexToken, varIndex: typing.Optional[ast_expr.Expr]) -> typing.Tuple[int, ast.AST]:
        instruction = ast_function_call.FunctionCall(identifier, varIndex)
        (index, expr) = self.FunctionCallArgumentList(index-1) # -1 because parse instruction consumed the opening bracket.
        if expr is None or expr.Left is None:
            raise exceptions.ParserError(message = 'Expected a function argument.', loc=self.Previous(index).Location, filename=self.filename)
        instruction.Args = expr.Left
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        return (index, instruction)

    

    def ParseInstruction(self, index: int) -> typing.Tuple[int, ast.AST]:
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '{')
        if match:
            return self.ParseBlock(index)
        index = self.Consume(index = index, message ='Expected instruction identifier.',  type = types.LexTokenType.Identifier)
        identifier = self.Previous(index)
        (index, keyword) = self.ParseKeyword(index, identifier)
        if keyword is not None:
            return (index, keyword)
        varIndex = None       
        current = self.Current(index)
        if current is not None and current.Lexeme == '[':
            (index, varIndex) = self.GetVariableIndexer(index)      
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '(')
        if match:
            return self.ParseFunctionCall(index, identifier, varIndex)
        (index, match, _) = self.Match(index, types.LexTokenType.Operator, ['=', '+=', '-=', '/=', '*='])
        if match:
            return self.ParseAssign(index, identifier, varIndex)
        (index, match, _) = self.Match(index, types.LexTokenType.Operator, '=>')
        if match:
            return self.ParseFunctionDefinition(index, identifier)
        if varIndex is not None:
            raise exceptions.ParserError(message = 'Invalid variable reference in instruction.', loc=identifier.Location, filename=self.filename)
        raise exceptions.ParserError(message = f'Unknown instruction or keyword ({identifier.Lexeme}).', loc=identifier.Location, filename=self.filename)



    def ParseKeyword(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, typing.Optional[ast.AST]]:
        if identifier.Lexeme == 'if': return self.ParseIf(index, identifier)
        if identifier.Lexeme == 'foreach': return self.ParseForeach(index, identifier)
        if identifier.Lexeme == 'while': return self.ParseWhile(index, identifier)
        if identifier.Lexeme == 'halt': return self.ParseHalt(index, identifier)
        if identifier.Lexeme == 'break': return self.ParseBreak(index, identifier)
        if identifier.Lexeme == 'continue': return self.ParseContinue(index, identifier)
        if identifier.Lexeme == 'return': return self.ParseReturn(index, identifier)
        if identifier.Lexeme == 'include': return self.ParseInclude(index, identifier)
        if identifier.Lexeme == 'select': return self.ParseSelect(index, identifier)
        if identifier.Lexeme == 'const': return self.ParseConst(index, identifier)
        return (index, None)



    def ParseBlock(self, index: int) -> typing.Tuple[int, ast_block.Block]:
        index = self.Consume(index=index, message='Expected block bracket "{".', type=types.LexTokenType.Punctuation, lex='{')
        block = ast_block.Block(self.Previous(index))
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '}')
        while not match and index < self.length:
            (index, instruction) = self.ParseInstruction(index)
            block.Add(instruction)
            (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '}')
        if not match:
            raise exceptions.ParserError(message = 'Unbalanced block bracket, expected "}".', loc=self.Previous(index).Location, filename=self.filename)
        return (index, block)



    def ParseAssign(self, index: int, identifier: token.LexToken, varIndex: typing.Optional[ast_expr.Expr]) -> typing.Tuple[int, ast.AST]:
        operator = self.Previous(index)
        if operator.Lexeme not in ['=', '+=', '-=','/=', '*=']:
            raise exceptions.ParserError(message = f'Invalid assignment operator: {operator}.', loc=self.Previous(index).Location, filename=self.filename)
        assgn = ast_assignment.Assignment(identifier, varIndex, operator)
        (index, assgn.Value) = self.Expression(index)
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        return (index, assgn)



    def ParseConst(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        (index, match, tok) = self.Match(index, types.LexTokenType.Identifier, None)
        if tok is None or match is False:
            current = self.Current(index)
            if current is None:
                raise exceptions.ParserError(message = f'Constant identifier required, got {identifier.Type}.', loc=identifier.Location, filename=self.filename) # type: ignore
            raise exceptions.ParserError(message = f'Constant identifier required, got {self.Current(index).Type}.', loc=self.Current(index).Location, filename=self.filename) # type: ignore
        index = self.Consume(index, 'Expected "="', types.LexTokenType.Operator, '=')
        assgn = ast_assignment.Assignment(tok, None, self.Previous(index))
        assgn.isConst = True
        (index, assgn.Value) = self.Expression(index)
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        return (index, assgn)



    def ParseIf(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        instruction = ast_if.If(identifier)        
        (index, instruction.Condition) = self.Expression(index)
        if instruction.Condition is None:
            raise exceptions.ParserError(message = 'Expected a condition expression.', loc=self.Previous(index).Location, filename=self.filename)
        (index, instruction.Block) = self.ParseBlock(index)
        if instruction.Block is None:
            raise exceptions.ParserError(message = 'Expected a block ({}).', loc=self.Previous(index).Location, filename=self.filename)
        (index, match, tok) = self.Match(index, types.LexTokenType.Identifier, 'elif')
        while match and index < self.length and tok is not None:
            elfi = ast_if.Elif(tok)
            (index, elfi.Condition) = self.Expression(index)
            if elfi.Condition is None:
                raise exceptions.ParserError(message = 'Expected a condition expression.', loc=self.Previous(index).Location, filename=self.filename)
            (index, elfi.Block) = self.ParseBlock(index)
            if elfi.Block is None:
                raise exceptions.ParserError(message = 'Expected a block ({}).', loc=self.Previous(index).Location, filename=self.filename)
            instruction.Add(elfi)
            (index, match, tok) = self.Match(index, types.LexTokenType.Identifier, 'elif')
        (index, match, _) = self.Match(index, types.LexTokenType.Identifier, 'else')
        if match:
            (index, instruction.Else) = self.ParseBlock(index)
            if instruction.Else is None:
                raise exceptions.ParserError(message = 'Expected a block ({}).', loc=self.Previous(index).Location, filename=self.filename)
        return (index, instruction)

    

    def ParseForeach(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '(')
        if match:
            raise exceptions.ParserError(message = 'Foreach is not a function, expected a variable.', loc=self.Previous(index).Location, filename=self.filename)
        (index, var) = self.Expression(index)
        if var is None:
            raise exceptions.ParserError(message = 'Expected a variable.', loc=self.Previous(index).Location, filename=self.filename)
        (index, blk) = self.ParseBlock(index)
        if blk is None:
            raise exceptions.ParserError(message = 'Expected a block ({}).', loc=self.Previous(index).Location, filename=self.filename)
        return (index, ast_foreach.Foreach(identifier, var, blk))



    def ParseBreak(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        brk = ast_break.Break(identifier)
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        return (index, brk)



    def ParseContinue(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        brk = ast_continue.Continue(identifier)
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        return (index, brk)



    def ParseHalt(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '(')
        if match:
            raise exceptions.ParserError(message = 'Halt is not a function, expected a variable or a literal value.', loc=self.Previous(index).Location, filename=self.filename)
        (index, exitcode) = self.Expression(index)
        if exitcode is None:
            raise exceptions.ParserError(message = 'Expected a variable or a literal value.', loc=self.Previous(index).Location, filename=self.filename)
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        return (index, ast_halt.Halt(identifier, exitcode))



    def ParseWhile(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '(')
        if match:
            raise exceptions.ParserError(message = 'While is not a function, expected a condition.', loc=self.Previous(index).Location, filename=self.filename)
        (index, condition) = self.Expression(index)
        if condition is None:
            raise exceptions.ParserError(message = 'Expected a condition.', loc=self.Previous(index).Location, filename=self.filename)
        (index, blk) = self.ParseBlock(index)
        if blk is None:
            raise exceptions.ParserError(message = 'Expected a block ({}).', loc=self.Previous(index).Location, filename=self.filename)
        return (index, ast_while.While(identifier, condition, blk))
    


    def ParseReturn(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        (index, value) = self.Expression(index)
        if value is None:
            raise exceptions.ParserError(message = 'Expected a variable or a literal value.', loc=self.Previous(index).Location, filename=self.filename)
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        return (index, ast_return.Return(identifier, value))



    def ParseInclude(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        incl = ast_include.Include(identifier)
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, '(')
        if match:
            raise exceptions.ParserError(message = 'Include is not a function, expected a module name.', loc=self.Previous(index).Location, filename=self.filename)
        (index, match, include) = self.Match(index, types.LexTokenType.Identifier, None)
        if not match:
            raise exceptions.ParserError(message = 'Expected a module name.', loc=self.Previous(index).Location, filename=self.filename)
        while match and include is not None:
            incl.Add(include)
            (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, ',')
            if match:
                (index, match, include) = self.Match(index, types.LexTokenType.Identifier, None)
                if not match:
                    raise exceptions.ParserError(message = 'Expected a module name.', loc=self.Previous(index).Location, filename=self.filename)
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        return (index, incl)



    def GetSelectField(self, index: int) -> typing.Tuple[int, ast_select_field.SelectField]:
        all = False
        (index, match, field) = self.Match(index, types.LexTokenType.Identifier, None)
        if not match:
            (index, match, field) = self.Match(index, types.LexTokenType.Operator, '*')
            if match:
                all = True
        if field is None or not match:
            raise exceptions.ParserError(message = 'Select requires a field name or *.', loc=self.Previous(index).Location, filename=self.filename)
        fld = ast_select_field.SelectField(field)
        if all:
            return (index, fld)
        (index, match, _) = self.Match(index, types.LexTokenType.Identifier, 'as')
        if not match:
            fld.As = fld.Token
            return (index, fld)
        (index, match, _) = self.Match(index, types.LexTokenType.Identifier, None)
        if not match:
            (index, match, _) = self.Match(index, types.LexTokenType.String, None)
        if not match:
            raise exceptions.ParserError(message = 'Select field as requires a field name or *.', loc=self.Previous(index).Location, filename=self.filename)
        fld.As = self.Previous(index)
        return (index, fld)



    def ParseSelect(self, index: int, identifier: token.LexToken) -> typing.Tuple[int, ast.AST]:
        (index, distinct, _) = self.Match(index, types.LexTokenType.Identifier, 'distinct')
        fields: typing.List[ast_select_field.SelectField] = []
        (index, field) = self.GetSelectField(index)
        fields.append(field)
        (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, ',')
        while match and index < self.length:
            (index, field) = self.GetSelectField(index)
            fields.append(field)
            (index, match, _) = self.Match(index, types.LexTokenType.Punctuation, ',')
        index = self.Consume(index=index, message = 'Select requires "from" after field names.', type=types.LexTokenType.Identifier, lex='from')
        (index, frm) = self.Expression(index)
        (index, match, _) = self.Match(index=index, type=types.LexTokenType.Identifier, lex='where')
        where = None
        if match:
            (index, where) = self.Expression(index)       
        (index, merge, _) = self.Match(index=index, type=types.LexTokenType.Identifier, lex='merge')
        index = self.Consume(index=index, message = 'Select requires requires "into" <variable>.', type=types.LexTokenType.Identifier, lex='into')
        (index, into) = self.Expression(index)
        index = self.Consume(index, 'Expected ";"', types.LexTokenType.Punctuation, ';')
        sel = ast_select.Select(identifier, frm, into)
        sel.Fields = fields
        if where is not None:
            sel.Where = where
        sel.Distinct = distinct
        sel.Merge = merge
        return (index, sel)
