'''
Created on Aug 28, 2012
 
@author: Daniel J. Rivers
'''
from DataAccess import DataFacade
from Utilities import OutputUtils
import os
import win32api
import win32wnet

def processAll( path ):
    letters = [line.strip() for line in open( path )]
    DataFacade.writeDriveRecords( processDrives( letters ) )
    series = processSeries( letters )
    seriesID = DataFacade.writeSeriesRecords( series )
    seasons = processSeasons( series, seriesID )
    seasonID = DataFacade.writeSeasonRecords( seasons )

def processDrives( letters ):
    ret = []
    for i in letters:
        try :
            space = win32api.GetDiskFreeSpace( i )
            #not a clue how this number works... something like bytes in sector * sector * clusters * bytes to terrabytes conversion - or... magic
            magic = ( space[ 0 ] * space[ 1 ] / ( 1024 ** 4 ) )
            total = space[ 3 ] * magic
            free = space[ 2 ] * magic
            ratio = str( ( ( total - free ) / total ) * 100 )[:5] + "%"
            free = str( free * 1024 )[:3] + " GB" if free < 1 else str( free )[:4] + " TB"
            total = str( total * 1024 )[:3] + " GB" if total < 1 else str( total )[:4] + " TB"
            ret.insert( 0, ( win32api.GetVolumeInformation( i )[ 0 ], win32wnet.WNetGetConnection( i ), i, total, free, ratio ) )
        except:
            OutputUtils.warning( i + os.sep + "  not found or inaccessible" )
    return ret

def processSeasons( series, seriesID ):
    ret = []
    for i, v in enumerate( series ):
        path = DataFacade.getDriveIDByVolumeID( v[ 1 ] )[ 3 ] + os.sep + v[ 0 ] + os.sep
        for x in os.listdir( path ):
            if os.path.isdir( path + x + os.sep ):
                ret.append( ( x, seriesID[ i ], 0 ) )
    return ret

def processSeries( letters ):
    ret = []
    for i in listDirectories( letters ):
        for j in i[ 1 ]:
            ret.append( [j[3:], DataFacade.getDriveIDByLetter( i[ 0 ] ), 0] )
    return ret

def listDirectories( letters ):
    ret = []
    for i in letters:
        try :
            ret.append( [ i, listDirectoriesForDrive( i + os.sep ) ] )
        except:
            OutputUtils.warning( i + os.sep + "  not found or inaccessible" )
    return ret

def listDirectoriesForDrive( letter ):
    dirs = os.listdir( letter )
    dirs = [ e.upper() for e in dirs ]
    ret = []
    for i in dirs:
        subPath = letter + i
        if ( ( not "$" in subPath ) and ( not "SYSTEM VOLUME INFORMATION" in subPath ) ) and ( os.path.isdir( subPath ) ):
            ret.insert( 0, subPath )
    ret.reverse()
    return ret
