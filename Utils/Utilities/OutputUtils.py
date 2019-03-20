'''
Created on Aug 31, 2012
 
@author: Daniel J. Rivers
'''
from Utilities import TimeUtils

logLevel = 0

def exception( s, e ):
    if logLevel >= 0:
        p( s + ": " + str( e ), "EXCEPTION" )

def info( s ):
    if logLevel >= 2:
        p( s, "INFO" )

def warning( s ):
    if logLevel >= 1:
        p( s, "WARNING" )

def debug( s ):
    if logLevel >= 3:
        p( s, "DEBUG" )

def p( s, l ):
    print( nl( addTimestamp( addTags( s, l ) ) ) )

def nl( s ):
    return s + "\n"

def addTimestamp( s ):
    return "<" + TimeUtils.getCurrentTime() + ":>  " + s

def addTags( s, l ):
    return "[***" + l + "***]   " + s

def printHeaderLine():
    print( "----------------------------------------" )
