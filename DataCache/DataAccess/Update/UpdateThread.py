'''
Created on Sep 24, 2012
 
@author: Daniel J. Rivers
'''
from Connection.DataConnection import DataConnection
from DBInterface.DatabaseInterface import DatabaseInterface
from Utilities import OutputUtils
from threading import Thread
from time import sleep

class UpdateThread ( Thread ):

    def __init__( self, time, cache ):
        self.time = time
        self.cache = cache
        Thread.__init__( self ) #super class call

    def run( self ):
        self.DatabaseInterface = DatabaseInterface( DataConnection( self.cache.getDBInt().dc.dbInfo ) )
        while True:
            sleep( self.time )
            OutputUtils.debug( "*** Update Cycle Started ***" )
            self.cache.updateCache( self.DatabaseInterface )
            OutputUtils.debug( "*** Update Cycle Completed ***" )
