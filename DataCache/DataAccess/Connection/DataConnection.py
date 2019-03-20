'''
Created on Sep 22, 2012
 
@author: Daniel J. Rivers
'''
from Utilities import OutputUtils
import sqlite3

class DataConnection:

    def __init__( self, dbInfo ):
        self.dbInfo = dbInfo
        self.reload()

    def reload( self ):
        try:
            self.connection.close()
        except:
            OutputUtils.warning( "Tried to close connection that wasn't even open" )
        self.connection = sqlite3.connect( self.dbInfo )
        self.cursor = self.connection.cursor()
