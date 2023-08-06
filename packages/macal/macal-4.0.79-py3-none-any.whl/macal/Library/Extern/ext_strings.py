# Product:   Macal
# Author:    Marco Caspers
# Date:      27-09-2022
#

from unidecode import unidecode
import macal



def StrLen(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of len function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    arg = scope.GetVariable("arg")
    at = arg.GetType()
    if at != macal.VariableType.String and at != macal.VariableType.Record and at != macal.VariableType.Array:
        raise macal.RuntimeError(f"StrLen: Invalid argument type ({at}).", arg.Token.Location, filename)
    result = len(arg.GetValue())
    scope.SetReturnValue(result)



def StrLeft(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of left function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    arg = scope.GetVariable("arg")
    argl = scope.GetVariable("length")  
    result = arg.GetValue()[0:argl.GetValue()]
    scope.SetReturnValue(result)



def StrMid(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of mid function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    arg = scope.GetVariable("arg")
    args = scope.GetVariable("start")
    argl = scope.GetVariable("length")
    value = arg.GetValue()
    start = args.GetValue()
    length = argl.GetValue()
    endpos = start+length
    result = value[start:endpos]
    scope.SetReturnValue(result)



def ToString(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of toString function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    argvalue = scope.GetVariable("arg")
    result = f"{argvalue.GetValue()}"
    scope.SetReturnValue(result)



def StrContains(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of strContains function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    needle = scope.GetVariable("needle").GetValue()
    haystack = scope.GetVariable("haystack").GetValue()
    result = needle in haystack
    scope.SetReturnValue(result)



def StrReplace(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of strReplace function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    var = scope.GetVariable("var").GetValue()
    frm = scope.GetVariable("frm")
    wth = scope.GetVariable("with")
    result = var.GetValue().replace(frm.GetValue(), wth.GetValue())
    scope.SetReturnValue(result)



def StartsWith(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of StartsWith function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    haystack = scope.GetVariable("haystack").GetValue()
    needle = scope.GetVariable("needle").GetValue()
    result = haystack.startswith(needle)
    scope.SetReturnValue(result)



def RemoveNonAscii(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of RemoveNonAscii function"""
    macal.ValidateFunctionArguments(func, scope, filename)   
    txt = scope.GetVariable("text")
    text = txt.GetValue()
    result = unidecode(text)
    scope.SetReturnValue(result)



def ReplaceEx(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of ReplaceEx function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    var  = scope.GetVariable("var")
    repl = scope.GetVariable("repl")
    by   = scope.GetVariable("by")
    result = var.GetValue().GetValue()
    r = repl.GetValue()    
    b = by.GetValue()
    for ch in r:
        result = result.replace(ch, b)
    scope.SetReturnValue(result)



def PadLeft(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of ReplaceEx function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    string = scope.GetVariable("strng")
    char   = scope.GetVariable("char")
    amount = scope.GetVariable("amount")
    # this is counter intuitive, but the *just functions in python pad the character on the other end as what their name would imply.
    result = string.GetValue().rjust(amount.GetValue(), char.GetValue())
    scope.SetReturnValue(result)



def PadRight(func:macal.FunctionDefinition, scope: macal.Scope, filename: str) -> None:
    """Implementation of ReplaceEx function"""
    macal.ValidateFunctionArguments(func, scope, filename)
    string = scope.GetVariable("strng")
    char   = scope.GetVariable("char")
    amount = scope.GetVariable("amount")
    # this is counter intuitive, but the *just functions in python pad the character on the other end as what their name would imply.
    result = string.GetValue().ljust(amount.GetValue(), char.GetValue()) 
    scope.SetReturnValue(result)
