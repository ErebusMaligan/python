'''
@author Daniel J. Rivers
2013

Created: Apr 23, 2013, 12:00:02 PM 
'''
if __name__ == "__main__":
    from RoboCopy import PrimaryFrame
    PrimaryFrame()

'''
Created on Apr 14, 2013
 
@author: Daniel J. Rivers
'''
from tkinter import Tk, ttk, StringVar, BooleanVar
from Utils import UIUtils as UI, UIPrefab
from Utils.LogUtils import Log, LogWindow
from Utils import LogUtils
import os
import subprocess

class PrimaryFrame:

    def __init__ ( self ):
        self.root = Tk()
        self.root.iconbitmap( "copy.ico" )
        self.root.title( "Advanced Robocopy" )
        self.root.geometry( "300x220" )
        self.buildPrimaryUI()
        self.root.columnconfigure( 0, weight = 1 )
        self.root.rowconfigure( 0, weight = 1 )
        self.root.mainloop()

    def buildPrimaryUI( self ):
        self.tab = ttk.Notebook( self.root )
        self.tab.grid( row = 0, column = 0, sticky = "NSEW" )
        self.tab.columnconfigure( 0, weight = 1 )
        self.tab.rowconfigure( 0, weight = 1 )
        for pair in [ ( "Directories", self.buildFilePaths ), ( "Exclude", self.buildXDOptions ), ( "Options", self.buildOtherOptions ) ]:
            self.tab.add( pair[1](), text = pair[ 0 ] )
        UI.gridIt( ttk.Button( self.root, text = "Run Copy", command = lambda: self.roboCopy( self.source.get(), self.dest.get(), self.out.get() ) ), 3, 0, 4, "NSEW" )

    def buildFilePaths( self ):
        self.source = StringVar( value = "C:/MKVTEST/" )
        self.dest = StringVar( value = "C:/cptest/" )
        self.out = StringVar( value = "test1" )
        f = UI.buildFrame( self.tab, 4 )
        UI.buildDirEntry( f, "Source Dir:", self.source, 0, 0, 1 )
        UI.buildDirEntry( f, "Dest Dir:", self.dest, 1, 0, 1 )
        UI.buildEntryPair( f, "Log Name:", self.out, 2, 0, 1 )
        f.grid( row = 0, column = 0, sticky = "NSEW" )
        return f

    def buildXDOptions( self ):
        self.xdVar = StringVar()
        f = UI.buildFrame( self.tab, 3 )
        self.excludePanel = UIPrefab.ScrollingList( f, "Excluded Dir", [ "System Volume Information", "$RECYCLE.BIN" ], 3 )
        UI.gridIt( self.excludePanel, 0, 0, 3, "NSEW" )
        self.xdE = ttk.Entry( f, textvariable = self.xdVar )
        UI.gridIt( self.xdE, 1, 0, 3 )
        UI.gridIt( ttk.Button( f, text = "Add", command = lambda: self.excludePanel.addItemToList( self.xdVar.get() ) ), 2, 0, 1, "E" )
        UI.gridIt( ttk.Button( f, text = "Remove", command = lambda: self.excludePanel.removeSelectedItem() ), 2, 2, 1, "W" )
        return f

    def buildOtherOptions( self ):
        f = UI.buildFrame( self.tab, 3 )
        self.subDir = BooleanVar( value = True )
        self.mirror = BooleanVar( value = True )
        self.wait = StringVar( value = "5" )
        self.retry = StringVar( value = "1000000" )
        UI.gridIt( ttk.Checkbutton( f, text = "Include Subdirectories", variable = self.subDir ), 0, 0, 1, "E" )
        UI.gridIt( ttk.Checkbutton( f, text = "Mirror", variable = self.mirror ), 0, 1, 1, "W" )
        UI.buildEntryPair( f, "Time Betweeen Retry (sec):", self.wait, 1, 0 )
        UI.buildEntryPair( f, "Number of Retries:", self.retry, 2, 0 )
        return f

    def roboCopy( self, source, dest, output ):
        LogWindow.getInstance()
        Log( os.getcwd(), output )
        xd = ""
        if self.excludePanel.getAllItems():
            xd += " /XD"
            for i in self.excludePanel.getAllItems():
                xd += " \"" + i + "\""
        sub = "/S " if self.subDir.get() else ""
        mir = " /MIR" if self.mirror.get() else ""
        composite = "robocopy \"" + source + "\" \"" + dest + "\" " + sub + "/W:" + self.wait.get() + " /R:" + self.retry.get() + mir + xd
        Log.info( composite )
        LogUtils.logProcessOutput( subprocess.Popen( composite, stdout = subprocess.PIPE, shell = True ), None )
        Log.closeCurrentLog()
