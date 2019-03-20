'''
@author Daniel J. Rivers
2013

Created: Apr 23, 2013, 12:00:02 PM 
'''
from tkinter import Tk, ttk, StringVar, filedialog
from Utils.FileUtils import File
from Utils import EpisodeUtils
from Utils import FileUtils
from Utils.LogUtils import Log
from Utils import UIUtils as UI

import os

if __name__ == "__main__":
    from RenameUtilities import PrimaryFrame
    PrimaryFrame()


class PrimaryFrame:

    def __init__ ( self ):
        self.root = Tk()
        self.root.iconbitmap( "rename.ico" )
        self.root.title( "File Renamer" )
        self.root.geometry( "380x180" )
        self.buildPrimaryUI()
        self.root.columnconfigure( 0, weight = 1 )
        self.root.rowconfigure( 0, weight = 1 )
        self.root.mainloop()

    def buildPrimaryUI( self ):
        self.tab = ttk.Notebook( self.root )
        self.tab.grid( row = 0, column = 0, sticky = "NSEW" )
        for pair in [ ( "Scratch Rename", self.buildFilePaths ) ]:
            self.tab.add( pair[1]( self.tab ), text = pair[ 0 ] )

    def buildFilePaths( self, tab ):
        path = StringVar()
        series = StringVar()
        season = StringVar()
        episode = StringVar()
        episode.set( 1 )
        path.set( "Browse..." )
        f = UI.buildFrame( tab, 2 )
        UI.buildDirEntry( f, "Input Directory:", path, 0, 0 )
        UI.buildEntryPair( f, "Series:", series, 1, 0 )
        UI.buildEntryPair( f, "Season:", season, 2, 0 )
        UI.buildEntryPair( f, "Starting Number:", episode, 3, 0 )
        UI.gridIt( ttk.Button( f, text = "Run Rename", command = lambda: self.scratchRename( File( path.get() ), series.get(), season.get(), episode.get() ) ), 4, 0, 3, "EW" )
        return f

    def scratchRename( self, directory, name, season, episode ):
        '''Rename a set of files that otherwise has no season/episode naming convention
    
        Parameters
        ----------
        directory : File
            Path that contains episode files to rename.
        name : str
            Show name, will preceed e/s numbers.
        season : str
            Should be the season being renumbered/created (should be a str containing an int).
            
        '''
        Log( directory.absPath, name )
        for idx, file in enumerate( FileUtils.getFilesExcludeType( directory, ".log" ) ):
            newName = name + "_s" + EpisodeUtils.addZeroes( season ) + "e" + EpisodeUtils.addZeroes( str( idx + int( episode ) ) ) + "." + FileUtils.getSuffix( file )
            Log.info( "Renaming: " + file.name + " to: " + newName + "\n" )
            os.rename( file.absPath, File.pathParts( directory.absPath, newName ).absPath )
        Log.closeCurrentLog()

