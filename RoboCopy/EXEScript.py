'''
Created on Apr 21, 2013
 
@author: Daniel J. Rivers
'''
import sys
from cx_Freeze import setup, Executable

#no clue why this is needed but the exe crashes when run if it's not here
include = ["re"]

#additional non-py files that need to be included
includeFiles = [ "copy.ico" ]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict( compressed = True, includes = include, include_files = includeFiles, icon = "copy.ico" )

setup( name = "RoboCopy GUI",
        version = "0.0.9.9",
        description = "RoboCopy GUI",
        options = dict( build_exe = buildOptions ),
        executables = [Executable( "RoboCopy.py", base = base )] )
