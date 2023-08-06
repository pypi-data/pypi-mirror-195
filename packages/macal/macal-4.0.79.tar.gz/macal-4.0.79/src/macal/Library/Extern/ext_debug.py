import macal

def DebugPrintScope(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    if scope.Parent is not None:
        for var in scope.Parent.Variables:
            print(f"Variable {var} ", scope.Parent.Variables[var])
    else:
        print("Parent is None, cant print variables.")


def DebugPrintVariable(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    name = scope.GetVariable("varname").GetValue()
    if scope.Parent is not None:
        var = scope.Parent.FindVariable(name)
        print(var)
    else:
        print("Parent is None, cant print variable.")