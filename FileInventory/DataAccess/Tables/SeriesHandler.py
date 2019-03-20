'''
Created on Sep 3, 2012
 
@author: Daniel J. Rivers

test change
'''
from DataAccess.DBInt import DBInt
from DataAccess.TableData import TableData
from DataAccess.TableHandler import TableHandler
from DataAccess.Tables.DriveHandler import Drive, DriveHandler
from Utilities import OutputUtils

class SeriesHandler( TableHandler ):

    @staticmethod
    def getValuesForTable( td, l ):
        records = TableHandler.getAllRecords( td )
        ret = []
        for i in records:
            i = list( i )
            i[ 2 ] = DBInt().get( ( ( "ID", i[ 2 ] ), ), Drive() )[ 0 ][ 1 ]
            record = i[ 1:len( td.columnNames ) ]
            if not l:
                ret.append( record )
            else:
                add = True
                for j in l:
                    x = j.find( TableHandler.sep )
                    series = j[ :x]
                    volume = j[ x + 2: len( j ) - 1]
                    if series in record and volume in record:
                        add = False
                if add:
                    ret.append( record )
        return ret

    @staticmethod
    def getSeriesIDFromFilterName( name ):
        x = name.find( TableHandler.sep )
        series = name[ :x ]
        volume = name[ x + 2: len( name ) - 1 ]
        return DBInt().get( ( ( "VOLUME_ID", DriveHandler.getDriveIDByVolume( volume ) ), ( "SERIES", series ) ), Series() )[ 0 ][ 0 ]

    @staticmethod
    def getSeriesNameBySeriesID( i ):
        ret = []
        try:
            for i in DBInt().get( ( ( "ID", i ), ), Series() ):
                ret.append( i[ 1 ] )
            return ret
        except Exception as e:
            OutputUtils.exception( "No row found", e )

    @staticmethod
    def getSeriesNamesByVolumeID( l ):
        ret = []
        try:
            for i in DBInt().get( ( ( "VOLUME_ID", l ), ), Series() ):
                ret.append( i[ 1 ] )
            return ret
        except Exception as e:
            OutputUtils.exception( "No row found", e )

    @staticmethod
    def getColumnHeaders( td ):
        l = TableHandler.getColumnHeaders( td )
        l[ 1 ] = "VOLUME"
        return l

    @staticmethod
    def getSeriesIDs():
        ret = []
        for i in DBInt().getAll( Series() ):
            ret.append( i[0] )
        return ret

class Series( TableData ):

    def __init__( self ):
        self.columnNames = [ ( "SERIES", "TEXT" ), ( "VOLUME_ID", "INTEGER" ), ( "COMPLETED", "INTEGER" ), ( "TOD", "TEXT" ) ]
        self.tableName = "SERIES"
        self.where = 1
        self.idealColumnWidths = [ 125, 125, 125 ]

