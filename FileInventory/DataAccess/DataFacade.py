'''
Created on Sep 3, 2012
 
@author: Daniel J. Rivers
'''
from DataAccess.DBInt import DBInt
from DataAccess.TableHandler import TableHandler
from DataAccess.Tables.DriveHandler import Drive, DriveHandler
from DataAccess.Tables.EpisodeHandler import Episode
from DataAccess.Tables.SeasonHandler import Season, SeasonHandler
from DataAccess.Tables.SeriesHandler import Series, SeriesHandler

def createAllTables():
    DBInt().createTable( Drive() )
    DBInt().createTable( Series() )
    DBInt().createTable( Season() )
    DBInt().createTable( Episode() )
    DBInt().conn.commit()

def writeSeriesRecords( series ):
    ret = []
    for i in series:
        ret.append( TableHandler.writeRecord( i, Series() ) )
    DBInt().conn.commit()
    return ret

def writeDriveRecords( drives ):
    for i in drives:
        TableHandler.writeRecord( i, Drive() )
    DBInt().conn.commit()

def writeSeasonRecords( seasons ):
    ret = []
    for i in seasons:
        ret.append( TableHandler.writeRecord( i, Season() ) )
    DBInt().conn.commit()
    return ret

def getDriveIDByLetter( l ):
    return DriveHandler.getDriveIDByLetter( l )
    DBInt().conn.commit()

def getDriveVolumes():
    return DriveHandler.getDriveVolumes()

def getDriveIDByVolume( v ):
    return DriveHandler.getDriveIDByVolume( v )

def getDriveIDByVolumeID( vID ):
    return TableHandler.getRecordByID( vID, Drive() )

def getSeriesNamesByVolumeIDs( v ):
    ret = []
    for i in v:
        ret += getSeriesNamesByVolumeID( i )
    return ret

def getSeriesNamesByVolumeID( v ):
    s = TableHandler.sep + "(" + DriveHandler.getDriveVolumeByID( v ) + ")"
    return [ i + s for i in SeriesHandler.getSeriesNamesByVolumeID( getDriveIDByVolume( v ) )]

def getSeasonNamesBySeriesIDs( s ):
    ret = []
    for i in s:
        ret += getSeasonNamesBySeriesID( i )
    return ret

def getSeriesIDsFromFilterNames( l ):
    ret = []
    for i in l:
        ret.append( SeriesHandler.getSeriesIDFromFilterName( i ) )
    return ret

def getSeriesIDs():
    return SeriesHandler.getSeriesIDs()

def getSeasonNamesBySeriesID( se ):
    s = SeasonHandler.getFilterName( se )
    return [ i + s for i in SeasonHandler.getSeasonNamesBySeriesID( se ) ]
