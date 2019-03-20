'''
Created on Sep 22, 2012
 
@author: Daniel J. Rivers
'''


from Cache.PollingCache import PollingCache
from Connection.DataConnection import DataConnection
from DBInterface.DatabaseInterface import DatabaseInterface
from Update.UpdateThread import UpdateThread

class BasicCacheProxy:

    def __init__( self, dbName, tableNames ):
        self.cache = PollingCache( DatabaseInterface( DataConnection( dbName ) ), tableNames )
        self.cache.writeInfo()
        self.cache.writeCache()
        self.updateThread = UpdateThread( 5, self.cache )
        self.updateThread.start()

    def getHandler( self, tableName ):
        return self.cache.handlers.get( tableName )
