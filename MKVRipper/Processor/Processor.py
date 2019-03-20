'''
@author Daniel J. Rivers
2013

Created: Apr 12, 2013, 1:06:17 PM 
'''
import os
from Utils import FileUtils
from Utils.FileUtils import File
from Utils.LogUtils import Log
from Utils import LogUtils
from tkinter import BooleanVar, StringVar, IntVar

import subprocess
import time

def simpleProcess( props ):
    props.FINAL_INPUT = props.INPUT_PATH.get() + ( "/" + props.FILE_PREFIX.get() if props.USE_FILE.get() else "" )
    props.FINAL_OUTPUT = props.OUTPUT_PATH.get() + ( "/" + props.FILE_PREFIX.get() if props.USE_FILE.get() else "" )
    props.EPISODE_COUNTER = 0
    startFile = None if props.PARTIAL_FILE.get() == "\"\"" or props.PARTIAL_FILE.get() == "" else props.PARTIAL_FILE.get()
    singleDone = False
    directory = File.pathFull( props.FINAL_INPUT )
    Log.info( "Converting show directory: " + directory.absPath + "\n" )
    sub = FileUtils.getSubDir( directory )
    seasonNumber = props.STARTING_SEASON.get() - 1

    #For all subdirectories (non recursive) in the given main directory...
    while ( seasonNumber < len( sub ) or props.SINGLE_SEASON.get() ) and seasonNumber < props.ENDING_SEASON.get():
        seasonDirectory = sub[ 0 ] if props.SINGLE_SEASON.get() else sub[ seasonNumber ]
        Log.info( "Searching in Sub-Directory: " + seasonDirectory.name )
        destDir = File.pathParts( props.FINAL_OUTPUT, seasonDirectory.name )
        props.EPISODE_COUNTER = props.PARTIAL_EPISODE.get()
        for isoFile in FileUtils.getFilesOfType( seasonDirectory, ".iso" ):
            Log.info( "Analyzing File: " + isoFile.name + "\n" )
            if startFile == None or isoFile.name == startFile:
                startFile = None
                if ( not props.PARTIAL_SINGLEFILE.get() ) or ( props.PARTIAL_SINGLEFILE.get() and not singleDone ):

                    #Info Process
                    proc = subprocess.Popen( props.MAKEMKV_PATH.get() + " info iso:\"" + isoFile.absPath + "\"", stdout = subprocess.PIPE, shell = False )
                    lines = []
                    while True:
                        line = proc.stdout.readline().decode( 'utf-8' )
                        if not line:
                            Log.info( "\n\n" )
                            break
                        else:
                            #If it's a title line...
                            if ( "Title #" in line ) and not "skipped" in line:
                                line = line.strip()
                                Log.info( line.strip() )
                                lines.append( line )

                    for line in lines:
                        trackNumber = int( line[ line.rfind( "#" ) + 1:line.rfind( "w" ) - 1 ] ) + 1
                        t = line[ line.rfind( ", " ) + 1:line.rfind( ":" ) ]
                        hours = int( t[ 1:t.find( ":" ) ] )
                        minutes = int( t[ t.find( ":" ) + 1: ] )

                        #If it's longer than the minimum t allowed go ahead and process it
                        if ( minutes >= props.MIN_TIME.get() or hours > 0 ) and minutes < props.MAX_TIME.get():

                            Log.info( "++++++++++ Processing Episode File " + str( trackNumber ) + " ++++++++++" )

                            #Make Season directory if needed
                            if not os.path.exists( destDir.absPath ):
                                os.makedirs( destDir.absPath )

                            Log.info( "VOB EXTRACTING:" )

                            #DVDFab8 Extraction process
                            Log.info( "Extracting: " + str( trackNumber ) + " from " + isoFile.absPath + " to " + destDir.absPath + "\n\n" )
                            LogUtils.logProcessOutput( subprocess.Popen( props.DVDFAB_PATH.get() + "/MODE \"DVDVOB\" /SRC \"" + isoFile.absPath + "\"" + " " + "/DEST \"" + destDir.absPath + "\\" + "\"" + " " + "/PROFILE \"vob.passthrough\"" + " " + "/TITLE " + "\"" + str( trackNumber ) + "\"" + " " + "/CLOSE", stdout = subprocess.PIPE, shell = True ), None )

                            #Sleep for 3 sec to allow file locks to release... was a problem at one point
                            time.sleep( 3 )

                            #File Renaming based on season/episode
                            Log.info( "RENAMING:" )
                            files = renameFiles( props, hours, isoFile, destDir, seasonNumber, trackNumber )

                            #MKVMerge repackage to MKV process
                            Log.info( "MKV MERGING:" )
                            vobPath = files[ 0 ].absPath
                            Log.info( "VOB PATH: " + vobPath )
                            proc = subprocess.Popen( props.MKVMERGE_PATH.get() + " -o \"" + vobPath[ 0 : len( vobPath ) - 4 ] + ".mkv\" \"" + vobPath + "\"", stdout = subprocess.PIPE, shell = True )
                            LogUtils.logProcessOutput( proc, lambda x: ( not "Progress" in x and not "mkvmerge" in x ) )

                            Log.info( "\n\n" )

                            #Move source files to subdirectory
                            Log.info( "MOVING SOURCE FILES:" )
                            FileUtils.moveFiles( File.pathParts( destDir.absPath, "SourceFiles" ), files );
                            Log.info( "---------- Processing Episode File " + str( trackNumber ) + " ----------\n\n" )
                    Log.info( "DISC FINISHED" )
                    singleDone = True
        seasonNumber += 1

def renameFiles( props, hours, isoFile, destDir, seasonNumber, trackNumber ):
    ret = []
    extra = ""
    if hours > 0:
        extra = "e" + addZeroes( str( props.EPISODE_COUNTER + 1 ) )
    ext = [ "vob", "idx", "sub" ]
    for i in range( 0, len( ext ) ):
        e = ext[ i ]
        z = File.pathParts( destDir.absPath, "Title" + str( trackNumber ) + "." + e )
        if os.path.exists( z.absPath ):
            newFileName = props.FILE_PREFIX.get() + "_s" + addZeroes( str( seasonNumber + 1 ) ) + "e" + addZeroes( str( props.EPISODE_COUNTER ) ) + extra + "." + e
            Log.info( "Renaming: " + z.name + " to: " + newFileName + "\n\n" )
            n = File.pathParts( destDir.absPath, newFileName )
            os.rename( z.absPath, n.absPath )
            ret.append( n )
    props.EPISODE_COUNTER += 2 if hours > 0 else 1
    return ret

def addZeroes( s ):
    return "0" + s if len( s ) < 2 else s

class Props:

    def __init__ ( self ):
        #Program Paths
        self.MAKEMKV_PATH = StringVar()
        self.MKVMERGE_PATH = StringVar()
        self.DVDFAB_PATH = StringVar()

        #Processing Paths
        self.INPUT_PATH = StringVar()
        self.OUTPUT_PATH = StringVar()

        #Process Run Settings
        self.FILE_PREFIX = StringVar()
        self.STARTING_SEASON = IntVar()
        self.ENDING_SEASON = IntVar()
        self.MIN_TIME = IntVar()
        self.MAX_TIME = IntVar()
        self.USE_FILE = BooleanVar()
        self.SINGLE_SEASON = BooleanVar()

        #Partial Season
        self.PARTIAL_FILE = StringVar()
        self.PARTIAL_EPISODE = IntVar()
        self.PARTIAL_SINGLEFILE = BooleanVar()

        self.FINAL_INPUT = ""
        self.FINAL_OUTPUT = ""

        self.EPISODE_COUNTER = 0

        self.loadProps()


    def loadProps( self ):
        p = dict()
        #Read properties into a map
        for line in open( "MKVCreator.properties" ):
            if ( not line.startswith( "#" ) and not line.strip() == "" ):
                l = line.strip().split( "=" )
                p[ l[ 0 ] ] = l[ 1 ]
        self.MAKEMKV_PATH.set( p[ "MAKEMKV.PATH" ] )
        self.MKVMERGE_PATH.set( p[ "MKVMERGE.PATH" ] )
        self.DVDFAB_PATH.set( p[ "DVDFAB.PATH" ] )
        self.INPUT_PATH.set( p[ "INPUT.PATH" ] )
        self.OUTPUT_PATH.set( p[ "OUTPUT.PATH" ] )

#        self.FILE_PREFIX.set( p[ "FILE.PREFIX" ] )

        self.STARTING_SEASON.set( int( p["STARTING.SEASON"] ) )
        self.ENDING_SEASON.set( int( p["ENDING.SEASON"] ) )

        self.MIN_TIME.set( int( p[ "MIN.TIME" ] ) )
        self.MAX_TIME.set( int( p[ "MAX.TIME" ] ) )
        self.USE_FILE.set( p[ "USE.FILE" ] == "true" )
        self.SINGLE_SEASON.set( p[ "SINGLE.SEASON" ] == "true" )

#        self.PARTIAL_FILE.set( p[ "PARTIAL.FILE" ] )
        self.PARTIAL_EPISODE.set( int( p[ "PARTIAL.EPISODE" ] ) )
        self.PARTIAL_SINGLEFILE.set( p[ "PARTIAL.SINGLEFILE" ] == "true" )

