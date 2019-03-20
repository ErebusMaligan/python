'''
Created on Apr 21, 2013
 
@author: Daniel J. Rivers
'''
import sys
from cx_Freeze import setup, Executable

#no clue why this is needed but the exe crashes when run if it's not here
include = ["re"]

#additional non-py files that need to be included
includeFiles = [ "MKVCreator.properties", "MKV.ico" ]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict( compressed = True, includes = include, include_files = includeFiles, icon = "MKV.ico" )

setup( name = "MKVCreator",
        version = "0.0.9.9",
        description = "MKVDCreator",
        options = dict( build_exe = buildOptions ),
        executables = [Executable( "MKVCreator.py", base = base )] )
