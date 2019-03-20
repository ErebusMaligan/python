'''
Created on Aug 31, 2012
 
@author: Daniel J. Rivers
'''
import time

def getCurrentTime():
    return time.asctime( time.localtime( time.time() ) )
