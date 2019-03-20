'''
Created on Sep 23, 2012
 
@author: Daniel J. Rivers
'''
from Cache.CacheListener import CacheListener
from Utilities import OutputUtils

class BasicHandler ( CacheListener ):

    def __init__( self, tableName, cache ):
        self.tableName = tableName
        self.cache = cache
        self.listeners = []

    def getAll( self ):
        return self.cache.cache.get( self.tableName )

    def getByCriteria( self, criteria ):
        ret = []
        for i in self.cache.cache.get( self.tableName ):
            if i.equalsWhere( criteria ):
                ret.append( i )
        return ret

    def merge( self, td ):
        criteria = dict()
        for i in td.pks:
            criteria[ i ] = td.values.get( i )
        records = self.getByCriteria( criteria )
        if not records:
            self.cache.databaseInterface.insert( td )
        else:
            self.cache.databaseInterface.update( td )

    def addListener( self, l ):
        self.listeners.append( l )

    def removeListener( self, l ):
        self.listeners.remove( l )

    def added( self, td ):
        OutputUtils.debug( self.tableName + " Handler: ADDED" )
        td.printData()
        for l in self.listeners:
            l.added( td )

    def updated( self, td ):
        OutputUtils.debug( self.tableName + " Handler: UPDATED" )
        td.printData()
        for l in self.listeners:
            l.updated( td )

    def removed( self, td ):
        OutputUtils.debug( self.tableName + " Handler: REMOVED" )
        for l in self.listeners:
            l.removed( td )
