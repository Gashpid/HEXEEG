import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {'packages': [], 'excludes' : []}
base = 'Win32GUI'
exe = Executable(
    script = 'game.py',
    initScript = None,
    base = 'Win32GUI',
    targetName = 'game.exe',
    #compress = True,
    #appendScriptToExe = True,
    #appendScriptToLibrary = True,
    #icon = True
)

setup( name = 'Game_H3XEEG', 
        version = '0.85',
        description = 'Game_H3XEEG',
        options = {'build_exe': build_exe_options},
        executables = [Executable('game.py', base = base)])
