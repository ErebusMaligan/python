'''
Created on Sep 22, 2012
 
@author: Daniel J. Rivers
'''

from Cache.BasicHandler import BasicHandler
from TableData import TableData
from Utilities import OutputUtils

class Cache:

    def __init__( self, databaseInterface, tableNames ):
        self.cache = dict()
        self.keys = dict()
        self.columnInfo = dict()
        self.handlers = dict()
        self.databaseInterface = databaseInterface
        self.tableNames = tableNames

    def writeInfo( self ):
        for i in self.tableNames:
            td = TableData()
            td.tableName = i
            columnInfo = self.databaseInterface.getColumnInfo( td )
            for c in columnInfo:
                '''some unused variables named for future reference'''
#                index = c[ 0 ]
                name = c[ 1 ]
                dtype = c[ 2 ]
#                nullable = c[ 3 ]
#                default = c[ 4 ]
                primary = c[ 5 ]
                if primary == 1: #add name to primary keys list if it is one
                    l = []
                    if i in self.keys:
                        l = self.keys.get( i )
                    l.append( name )
                    self.keys[ i ] = l
                l = []
                if i in self.columnInfo:
                    l = self.columnInfo.get( i )
                l.append( ( name, dtype ) )
                self.columnInfo[ i ] = l

    def writeCache( self ):
        for i in self.tableNames:
            records = self.databaseInterface.getAll( i )
            l = []
            for r in records:
                td = TableData()
                td.tableName = i
                td.pks = self.keys.get( i )
                for index, x in enumerate( r ):
                    td.values[ list( self.columnInfo.get( i ) )[ index ][ 0 ] ] = x
                l.append( td )
                OutputUtils.debug( "INITIAL WRITE: Added record to " + i + " cache" )
            self.cache[ i ] = l
            self.handlers[ i ] = BasicHandler( i, self )

    def printColumnInfo( self ):
        for k, v in self.columnInfo.items():
            OutputUtils.printHeaderLine()
            print ( "Column Info for " + k + ":" )
            OutputUtils.printHeaderLine()
            for x in v:
                print( "\t" + x[ 0 ] + " = " + x[ 1 ] )
            print( "\n" )

    def printCache( self ):
        for k, v  in self.cache.items():
            OutputUtils.printHeaderLine()
            print( "All Records for Table: " + k )
            OutputUtils.printHeaderLine()
            for x in v:
                x.printData()

    def getDBInt( self ):
        return self.databaseInterface

    def getPKs( self, tableName ):
        return self.keys.get( tableName )

    def reloadConnection( self ):
        self.databaseInterface.dc.reload()

