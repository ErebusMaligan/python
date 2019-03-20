'''
@author Daniel J. Rivers
2013

Created: Apr 8, 2013, 9:50:14 AM 
'''
if __name__ == "__main__":
    from MKVCreator import PrimaryFrame
    PrimaryFrame()


from tkinter import Tk, ttk
from Processor import Processor
from Processor.Processor import Props
from Utils.LogUtils import Log
from Utils import UIUtils as UI

class PrimaryFrame:

    def __init__ ( self ):
        self.root = Tk()
        self.props = Props()
        self.root.iconbitmap( "MKV.ico" )
        self.root.title( "Automated MKV Creator" )
        self.root.geometry( "380x180" )
        self.buildPrimaryUI()
        self.root.columnconfigure( 0, weight = 1 )
        self.root.rowconfigure( 0, weight = 1 )
        self.root.mainloop()

    def buildPrimaryUI( self ):
        self.tab = ttk.Notebook( self.root )
        self.tab.grid( row = 0, column = 0, sticky = "NSEW" )
        for pair in [ ( "Run Info", self.buildRunInfo ), ( "Partial Season", self.buildPartialSeason ), ( "File Paths", self.buildFilePaths ), ( "Program Paths", self.buildProgramPaths )]:
            self.tab.add( pair[1]( self.tab ), text = pair[ 0 ] )
        ttk.Button( self.root, text = "Run", command = self.runProcess ).grid( row = 1, column = 0, sticky = "EW" )

    def buildRunInfo( self, tab ):
        f = ttk.Frame( tab )
        for i in range( 5 ):
            f.columnconfigure( i, weight = 0 if i == 2 else 1 )
        #row 0
        UI.gridIt( ttk.Label( f, text = "File Prefix:" ), 0, 1, 1, "E" )
        UI.gridIt( ttk.Entry( f, textvariable = self.props.FILE_PREFIX, width = 20 ), 0, 2, 2, "W" )
        #row 1
        UI.buildEntryPair( f, "Starting Season:", self.props.STARTING_SEASON, 1, 0, 0, 5 )
        UI.buildEntryPair( f, "Ending Season:", self.props.ENDING_SEASON, 1, 3, 0, 5 )
        #row2
        UI.buildEntryPair( f, "Min Time:", self.props.MIN_TIME, 2, 0, 0, 5 )
        UI.buildEntryPair( f, "Max Time:", self.props.MAX_TIME, 2, 3, 0, 5 )
        #row3
        UI.gridIt( ttk.Checkbutton( f, text = "Use File Prefix", variable = self.props.USE_FILE ), 3, 1 )
        UI.gridIt( ttk.Checkbutton( f, text = "Single Season", variable = self.props.SINGLE_SEASON ), 3, 3 )
        return f

    def buildPartialSeason( self, tab ):
        f = UI.buildFrame( tab, 3 )
        UI.buildEntryPair( f, "Starting File:", self.props.PARTIAL_FILE, 0, 0, 1 )
        UI.buildEntryPair( f, "Starting Ep #:", self.props.PARTIAL_EPISODE, 1, 0, 1 )
        UI.gridIt( ttk.Checkbutton( f, text = "Single File Only", variable = self.props.PARTIAL_SINGLEFILE ), 2, 1 )
        return f

    def buildFilePaths( self, tab ):
        f = UI.buildFrame( tab, 2 )
        UI.buildEntryPair( f, "Input Directory:", self.props.INPUT_PATH , 0, 0 )
        UI.buildEntryPair( f, "Output Directory:", self.props.OUTPUT_PATH , 1, 0 )
        return f

    def buildProgramPaths( self, tab ):
        return self.makeEntryFrame( tab, 2, [( "MakeMKV:", self.props.MAKEMKV_PATH, 0 ), ( "MKVMerge:", self.props.MKVMERGE_PATH, 0 ), ( "DVDFab8QT:", self.props.DVDFAB_PATH, 0 )] )

    def makeEntryFrame( self, tab, columns, pairs ):
        f = UI.buildFrame( tab, columns )
        for i, pair in enumerate( pairs ):
            if len( pair ) == 3:
                UI.buildEntryPair( f, pair[ 0 ], pair[ 1 ], i, pair[ 2 ] )
            else:
                UI.buildEntryPair( f, pair[ 0 ], pair[ 1 ], i, pair[ 2 ], pair[ 3 ] )
        return f

    def runProcess( self ):
        Log( self.props.OUTPUT_PATH.get(), self.props.FILE_PREFIX.get() )
        Processor.simpleProcess( self.props )
