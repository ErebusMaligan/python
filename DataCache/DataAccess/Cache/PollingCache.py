'''
Created on Sep 25, 2012
 
@author: Daniel J. Rivers
'''
from Cache.Cache import Cache
from TableData import TableData

class PollingCache ( Cache ):

    def updateCache( self, updatedbInterface ): #needs a seperate db interface to use to avoid threading issues
        for i in self.tableNames:
            records = updatedbInterface.getAll( i )
            l = self.cache.get( i )
            for r in records:
                td = TableData()
                td.tableName = i
                td.pks = self.keys.get( i )
                for index, x in enumerate( r ):
                    td.values[ list( self.columnInfo.get( i ) )[ index ][ 0 ] ] = x
                if not self.alreadyExists( td ):
                    existingRecord = self.alreadyExistsPKS( td )
                    if existingRecord:
                        l.remove( existingRecord )
                    l.append( td )
                    if not existingRecord:
                        self.handlers.get( i ).added( td )
                    else:
                        self.handlers.get( i ).updated( td )

    def alreadyExists( self, td ):
        ret = False
        for r in self.cache.get( td.tableName ):
            if td.equals( r ):
                ret = True
                break
        return ret

    def alreadyExistsPKS( self, td ):
        ret = None
        for r in self.cache.get( td.tableName ):
            if td.pkEquals( r ):
                ret = r
                break
        return ret
