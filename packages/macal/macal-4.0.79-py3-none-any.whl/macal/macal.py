#
# Product:   Macal
# Author:    Marco Caspers
# Date:      15-09-2022
#

from __future__ import annotations
import os
import pathlib
import typing
from . import mscope
from . import lexer
from . import parser
from . import interpreter
from . import exceptions
from . import types
from . import variable
from . import value_item
from . import ast_function_definition
from . import token


class Macal:
    def __init__(self) -> None:
        self.debug: bool = False
        self.scriptExtension: str = '.mcl'
        self.Root: mscope.Scope = mscope.Scope('root')
        self.Root.Root = self.Root
        self.exitcode: variable.Variable = self.RegisterVariable("exitcode", 0, 'root')
        self.filePath: str = ''
        fn = self.RegisterEmbeddedFunction('GetInfiniteLoopProtectionCount', self.Root, 'root')
        fn.RegisterArgument('')
        fn = self.RegisterEmbeddedFunction('SetInfiniteLoopProtectionCount', self.Root, 'root')
        fn.RegisterArgument('count')


       
    def RegisterVariable(self, name: str, value: typing.Any, filename: str) -> variable.Variable:
        tok = token.LexToken(name, types.LexTokenType.Identifier, None, -1, filename)
        var = variable.Variable(tok, name)
        tok = token.LexToken('?registered_var_value?', types.LexTokenType.Identifier, None, -1, filename)
        var.Value = value_item.ValueItem(tok, types.VariableType.Nil, types.VariableType.Nil.name.lower()).ConvertFromPython(tok, value)
        self.Root.AddVariable(var)
        return var



    def RegisterEmbeddedFunction(self, name: str, scope: mscope.Scope, filename: str) -> ast_function_definition.FunctionDefinition:
        func = ast_function_definition.FunctionDefinition(
            token.LexToken(name, types.LexTokenType.Identifier, None, -1, filename))
        func.IsExternal = True
        scope.Functions[func.Name] = func
        return func



    def LoadFile(self, filename: str) -> str:
        if os.path.exists(filename):
            with open (filename, mode = 'r', encoding = 'utf-8') as text_file:
                source = text_file.read()
            return source
        return ''



    def FindIncludeFileName(self, include: str, scope: mscope.Scope) -> str:
        filename = f'{include}{self.scriptExtension}'
        path = os.path.join(os.path.dirname(__file__), "Library", filename)
        if pathlib.Path(path).is_file(): return path
        path = os.path.join(scope.includeFolder, filename)
        if pathlib.Path(path).is_file(): return path
        path = os.path.join(pathlib.Path(self.filePath).parent, filename)
        if pathlib.Path(path).is_file(): return path
        return ''



    def RunInclude(self, filename: str, scope: mscope.Scope, iscope: mscope.Scope)-> typing.Tuple[bool, str]:
        incl = Macal()
        incl.Root = iscope
        (r, _) = incl.Run(filename)
        if r:
            scope.Includes.append(iscope)
        return (r, '')



    def Include(self, include: str, scope: mscope.Scope) -> typing.Tuple[bool, str]:
        iscope = scope.CreateTempScope(include)
        iscope.Root = iscope  # we are our own root
        iscope.Parent = None   # type: ignore
        iscope.Name = include # overwrite the name! We don't want it to be called as a regular child scope
        filename = self.FindIncludeFileName(include, scope)
        debug = True
        if filename == '':
            return (False, f'File not found ({include}).')
        if debug:
            return self.RunInclude(filename, scope, iscope)
        try:
            return self.RunInclude(filename, scope, iscope)
        except Exception as ex:
            return (False, f"{ex}")
        


    def Execute(self, source: str, filename: str, root: mscope.Scope, exitcode: variable.Variable) -> typing.Tuple[bool, mscope.Scope]:
        root.Source = source
        lex = lexer.Lexer()
        root.Tokens = lex.Lex(root.Source, filename)
        parse = parser.Parser()
        root.AST = parse.Parse(root.Tokens, filename)
        intrprt = interpreter.Interpreter(self.Include)
        exitcode.SetValue(0)
        return (True, intrprt.Interpret(root.AST, filename, root))



    def Run(self, filename: str)-> typing.Tuple[bool, mscope.Scope]:
        self.filePath = filename
        source = self.LoadFile(filename)
        if source == '':
            raise exceptions.RuntimeError(f"Failed to load file {filename}", None, filename)           
        if self.debug:
            return self.Execute(source, filename, self.Root, self.exitcode)
        try:
            return self.Execute(source, filename, self.Root, self.exitcode)
        except exceptions.LexError as ex:
            self.exitcode.SetValue(1)
            print(ex)
        except exceptions.ParserError as ex:
            self.exitcode.SetValue(2)
            print(ex)
        except exceptions.RuntimeError as ex:
            self.exitcode.SetValue(3)
            print(ex)
        except Exception as ex:
            self.exitcode.SetValue(4)
            print(f'Unhandled exception: {ex}')
        return (False, self.Root)
