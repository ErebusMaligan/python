'''
Created on Aug 29, 2012

@author: riversda
'''
from DataAccess import DataFacade
from DataAccess.TableHandler import TableHandler
from DataAccess.Tables.DriveHandler import Drive
from DataAccess.Tables.SeasonHandler import Season, SeasonHandler
from DataAccess.Tables.SeriesHandler import Series, SeriesHandler
from UI.PrimaryMenuBar import PrimaryMenuBar
from UI.SimpleTable import SimpleTable
from tkinter import Tk, ttk
from tkinter.constants import FALSE

class PrimaryFrame:

    def __init__( self ):
        self.root = Tk()
        self.root.option_add( "*tearOff", FALSE )
        self.root.title( "File Inventory System" )
        self.root.rowconfigure( 0, weight = 1 )
        self.root.columnconfigure( 0, weight = 1 )
        self.lists = ExclusionLists()
        self.buildPrimaryUI()
        self.root.mainloop()

    def getPrimaryFrame( self ):
        return self.root

    def buildPrimaryUI( self ):
        self.menubar = PrimaryMenuBar( self )
        self.tab = ttk.Notebook( self.root )
        self.tab.grid( sticky = "nsew" )
        self.dTable = SimpleTable( self.tab, TableHandler.getTableSetup( Drive(), self.lists.volumes ), Drive().idealColumnWidths, "Drives" )
        self.tab.add( self.dTable.frame, text = "Drives" )
        self.sTable = SimpleTable( self.tab, SeriesHandler.getTableSetup( Series(), self.lists.series ), Series().idealColumnWidths, "Series" )
        self.tab.add( self.sTable.frame, text = "Series" )
        self.seTable = SimpleTable( self.tab, SeasonHandler.getTableSetup( Season(), self.lists.seasons ), Season().idealColumnWidths, "Seasons" )
        self.tab.add( self.seTable.frame, text = "Season" )

    def reload( self ):
        self.dTable.values = TableHandler.getTableSetup( Drive(), self.lists.volumes )[ 1 ]
        self.dTable.reload()

        for v in self.lists.volumes:
            for i in DataFacade.getSeriesNamesByVolumeID( v ):
                if i not in self.lists.series:
                    self.lists.series.append( i )
        self.sTable.values = SeriesHandler.getTableSetup( Series(), self.lists.series )[ 1 ]
        self.sTable.reload()

        for i in DataFacade.getSeasonNamesBySeriesIDs( DataFacade.getSeriesIDsFromFilterNames( self.lists.series ) ):
            if i not in self.lists.seasons:
                self.lists.seasons.append( i )
        self.seTable.values = SeasonHandler.getTableSetup( Season(), self.lists.seasons )[ 1 ]
        self.seTable.reload()

    def exportTablesToFile( self, primaryFrame ):
        f = open( 'FileList.txt', 'w' )
        for i in self.dTable.values:
            prettyDrive = i[ 0 ] + " -- Free Space = " + i[ 4 ] + "/" + i[ 3 ] + "  Used: " + i[ 5 ]
            f.write( "%s\n" % prettyDrive )
            for s in self.sTable.values:
                if i[ 0 ] in s:
                    f.write( "\t|__ %s\n" % s[ 0 ] )
                    for se in self.seTable.values:
                        if s[ 0 ] + "~(" + i[ 0 ] + ")" in se:
                            f.write( "\t\t|__ %s\n" % str( se[ 0 ] ) )
            f.write( "\n" )


class ExclusionLists:

    def __init__( self ):
        self.volumes = []
        self.series = []
        self.seasons = []

    def setVolumes( self, v ):
        self.volumes = v

    def setSeries( self, s ):
        self.series = s

    def setSeasons( self, s ):
        self.seasons = s
