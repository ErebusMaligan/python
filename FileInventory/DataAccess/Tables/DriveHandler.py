'''
Created on Sep 3, 2012
 
@author: Daniel J. Rivers
'''
from DataAccess.DBInt import DBInt
from DataAccess.TableData import TableData
from DataAccess.TableHandler import TableHandler
from Utilities import OutputUtils

class DriveHandler( TableHandler ):

    @staticmethod
    def getDriveVolumes():
        return [ row[ 1 ] for row in DBInt().getAll( Drive() ) ]

    @staticmethod
    def getDriveIDByLetter( l ):
        try:
            return DBInt().get( ( ( "LETTER", l ), ), Drive() )[ 0 ][ 0 ]
        except Exception as e:
            OutputUtils.exception( "No row found", e )

    @staticmethod
    def getDriveVolumeByID( v ):
        try:
            return DBInt().get( ( ( "VOLUME", v ), ), Drive() )[ 0 ][ 1 ]
        except Exception as e:
            OutputUtils.exception( "No row found", e )


    @staticmethod
    def getDriveIDByVolume( v ):
        try:
            return DBInt().get( ( ( "VOLUME", v ), ), Drive() )[ 0 ][ 0 ]
        except Exception as e:
            OutputUtils.exception( "No row found", e )

    @staticmethod
    def getVolumeFromRecord( l ):
        return l[ 1 ]

class Drive( TableData ):

    def __init__( self ):
        self.columnNames = [ ( "VOLUME", "TEXT" ), ( "URI", "TEXT" ), ( "LETTER", "TEXT" ), ( "TOTAL_SPACE", "TEXT" ), ( "FREE_SPACE", "TEXT" ), ( "USAGE", "TEXT" ), ( "TOD", "TEXT" ) ]
        self.tableName = "DRIVE"
        self.where = 0
        self.idealColumnWidths = [100, 120, 45, 85, 75, 75]
