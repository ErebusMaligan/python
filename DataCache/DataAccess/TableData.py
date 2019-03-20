'''
Created on Sep 22, 2012
 
@author: Daniel J. Rivers
'''
from Utilities import OutputUtils

class TableData:

    def __init__( self ):
        self.tableName = ""
        self.values = dict()
        self.pks = []

    @classmethod
    def defaultTableData( cls, tableName, cache ):
        d = TableData()
        d.tableName = tableName
        d.pks = cache.getPKs( tableName )
        return d

    def getPKSubset( self ):
        ret = dict()
        for pk in self.pks:
            ret[ pk ] = self.values.get( pk )
        return ret

    def pkEquals( self, td ):
        ret = True
        for k in self.pks:
            if str( self.values.get( k ) ) != str( td.values.get( k ) ):
                ret = False
                break
        return ret

    def equals( self, td ):
        ret = True
        for k in self.values.keys():
            if str( self.values.get( k ) ) != str( td.values.get( k ) ):
                ret = False
                break
        return ret

    def equalsWhere( self, criteria ):
        ret = True
        for k, v in criteria.items():
            if self.values.get( k ) != v:
                ret = False
                break
        return ret

    def printData( self ):
        OutputUtils.printHeaderLine()
        print( "Data Info: " )
        OutputUtils.printHeaderLine()
        for k, v in self.values.items():
            print( k + " = " + str( v ) )
        print( "\n" )
