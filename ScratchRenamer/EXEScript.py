'''
Created on Apr 21, 2013
 
@author: Daniel J. Rivers
'''
import sys
from cx_Freeze import setup, Executable

#no clue why this is needed but the exe crashes when run if it's not here
include = ["re"]

#additional non-py files that need to be included
includeFiles = [ "rename.ico" ]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict( compressed = True, includes = include, include_files = includeFiles, icon = "rename.ico" )

setup( name = "Scratch Renamer",
        version = "0.0.9.9",
        description = "Scratch Renamer",
        options = dict( build_exe = buildOptions ),
        executables = [Executable( "RenameUtilities.py", base = base )] )
