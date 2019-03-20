'''
Created on Sep 3, 2012
 
@author: Daniel J. Rivers
'''

from DataAccess.DBInt import DBInt
from DataAccess.TableData import TableData
from DataAccess.TableHandler import TableHandler
from DataAccess.Tables.DriveHandler import Drive
from DataAccess.Tables.SeriesHandler import Series
from Utilities import OutputUtils

class SeasonHandler( TableHandler ):

    @staticmethod
    def getColumnHeaders( td ):
        l = TableHandler.getColumnHeaders( td )
        l[ 1 ] = "SERIES"
        return l

    @staticmethod
    def getValuesForTable( td, l ):
        records = TableHandler.getAllRecords( td )
        ret = []
        for i in records:
            i = list( i )
            seriesRec = DBInt().get( ( ( "ID", i[ 2 ] ), ), Series() )[ 0 ]
            seriesName = seriesRec[ 1 ]
            volumeName = TableHandler.getRecordByID( seriesRec[ 2 ], Drive() )[ 1 ]
            i[ 2 ] = seriesName + TableHandler.sep + "(" + volumeName + ")"
            record = i[ 1:len( td.columnNames ) ]
            if not l:
                ret.append( record )
            else:
                add = True
                for j in l:
                    x = j.find( TableHandler.sep )
                    season = j[ :x ]
                    p2 = j[ x + 2:]
                    x = p2.find( TableHandler.sep )
                    series = p2[ :x]
                    volume = p2[ x + 1: len( p2 ) - 1]
                    if season in record and series + TableHandler.sep + "(" + volume + ")" in record:
                        add = False
                if add:
                    ret.append( record )
        return ret

    @staticmethod
    def getFilterName( i ):
        seriesRec = DBInt().get( ( ( "ID", i ), ), Series() )[ 0 ]
        seriesName = seriesRec[ 1 ]
        volumeName = TableHandler.getRecordByID( seriesRec[ 2 ], Drive() )[ 1 ]
        return TableHandler.sep + "(" + seriesName + TableHandler.sep + volumeName + ")"

    @staticmethod
    def getSeasonNamesBySeriesID( l ):
        ret = []
        try:
            for i in DBInt().get( ( ( "SERIES_ID", l ), ), Season() ):
                ret.append( i[ 1 ] )
            return ret
        except Exception as e:
            OutputUtils.exception( "No row found", e )

class Season( TableData ):

    def __init__( self ):
        self.columnNames = [ ( "SEASON", "TEXT" ), ( "SERIES_ID", "INTEGER" ), ( "COMPLETED", "INTEGER" ), ( "TOD", "TEXT" ) ]
        self.tableName = "SEASON"
        self.where = 1
        self.idealColumnWidths = [75, 125, 50]
