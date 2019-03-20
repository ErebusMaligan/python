'''
@author Daniel J. Rivers
2013

Created: Jul 30, 2013, 05:00:02 PM 
'''
from tkinter import Tk, ttk, StringVar
from Utils.FileUtils import File
from Utils import FileUtils
from Utils import UIUtils as UI

if __name__ == "__main__":
    from FlatDirectory import PrimaryFrame
    PrimaryFrame()

class PrimaryFrame:

    def __init__ ( self ):
        self.root = Tk()
        self.root.iconbitmap( "rename.ico" )
        self.root.title( "Flatten Directory" )
        self.root.geometry( "280x70" )
        self.buildFilePaths()
        self.root.columnconfigure( 0, weight = 1 )
        self.root.rowconfigure( 0, weight = 1 )
        self.root.mainloop()

    def buildFilePaths( self ):
        path = StringVar()
        path.set( "Browse..." )
        f = UI.buildFrame( self.root, 5 )
        UI.buildDirEntry( f, "Input Directory:", path, 0, 0 )
        UI.gridIt( ttk.Button( f, text = "Run Flatten", command = lambda: self.flattenDirectory( File.pathFull( path.get() ) ) ), 4, 0, 3, "EW" )
        f.grid( row = 0, column = 0, sticky = "NSEW" )

    def flattenDirectory( self, directory ):
        '''Flatten a set of 1 tier subdirectories by moving their files to the root directory and deleting the subdirectories
    
        Parameters
        ----------
        directory : File
            Path that contains episode files to rename.
            
        '''
        for d in FileUtils.getSubDir( directory ):
            FileUtils.moveFiles( directory, FileUtils.getFiles( d ) )
            FileUtils.deleteDirectory( d )
