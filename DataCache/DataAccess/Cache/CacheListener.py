'''
Created on Sep 24, 2012
 
@author: Daniel J. Rivers
'''
class CacheListener:

    def __init__( self ):
        if self.__class__ is CacheListener:
            raise NotImplementedError

    def added( self, td ):
        raise NotImplementedError

    def updated( self, td ):
        raise NotImplementedError

    def removed( self, td ):
        raise NotImplementedError
