#!/usr/bin/env python3
#
# Product:   Macal
# Author:    Marco Caspers
# Date:      15-09-2022
#

"""Macal Interpreter Application Runner"""

import os
import sys
import macal



def Run(lang: macal.Macal, filename: str, silent: bool) -> None:
    ext = os.path.splitext(filename)
    if len(ext) == 2 and ext[1] == '':
        filename = f'{filename}{lang.scriptExtension}'
    (result, _) = lang.Run(filename)
    print()
    exitCode = lang.exitcode.GetValue()
    if silent:
        return
    if exitCode != 0:
        print(f'Execution failed with errors, exit code: {exitCode}.')
    else:
        if result is True:
            print(f'Executed successfully, exit code: {exitCode}.')
        else:
            print(f'Execution failed, exit code: {exitCode}.')



def Main() -> None:
    args = sys.argv
    lang = macal.Macal()
    if len(args) > 1 and args[1] == '-v':
        args.pop(1)
        print(f'Macal version: {macal.__version__}')
    silent = False
    if len(args) > 1 and args[1] == '-s':
        args.pop(1)
        silent = True
    if len(args) > 1:
        lang.RegisterVariable('sysargv', args, 'root')
        Run(lang, args[1], silent)           
    else:
        print('Usage: mi [options] <filename> [options-for-app]')
        print()
        print('Options:')
        print()
        print('-v:  Show the version number of the language.')
        print("-s:  Don't show the exit code.")
        print()
        print('If you wish to use both -v and -s they must appear in this order.')
        print()
        print('Options for app:')
        print()
        print('These are specific for the application that you are running.')
        print('You need to set them after the filename.')



if __name__ == '__main__':
    Main()