'''
Created on Sep 1, 2012
 
@author: Daniel J. Rivers
'''
from DataAccess import DataFacade
from UI.FilterDialog import FilterDialog
from tkinter import Menu

class PrimaryMenuBar:

    def __init__( self, primaryFrame ):
        self.primaryFrame = primaryFrame
        self.menu = Menu( primaryFrame.getPrimaryFrame(), tearoff = False )
        primaryFrame.getPrimaryFrame()[ "menu" ] = self.menu
        self.createFileMenu()
        self.createFilterMenu()
        self.createExportMenu()

    def createFileMenu( self ):
        fMenu = Menu( self.menu )
        self.menu.add_cascade( menu = fMenu, label = "File" )
        fMenu.add_command( label = "Exit", command = "exit" )

    def createFilterMenu( self ):
        fMenu = Menu( self.menu )
        self.menu.add_cascade( menu = fMenu, label = "Filter" )
        fMenu.add_command( label = "Filter Volumes...", command = lambda e = self.primaryFrame : VolumeFilterDialog( e ) )
        fMenu.add_command( label = "Filter Series...", command = lambda e = self.primaryFrame : SeriesFilterDialog( e ) )
        fMenu.add_command( label = "Filter Seasons...", command = lambda e = self.primaryFrame : SeasonFilterDialog( e ) )

    def createExportMenu( self ):
        fMenu = Menu( self.menu )
        self.menu.add_cascade( menu = fMenu, label = "Export" )
        fMenu.add_command( label = "Export", command = lambda e = self.primaryFrame : self.primaryFrame.exportTablesToFile( e ) )

class VolumeFilterDialog( FilterDialog ):

    def __init__( self, primaryFrame ):
        super( VolumeFilterDialog, self ).__init__( primaryFrame, "Filter Volumes...", primaryFrame.lists.volumes )
        self.left = sorted( DataFacade.getDriveVolumes() )
        self.callback = self.primaryFrame.lists.setVolumes
        self.build()

class SeriesFilterDialog( FilterDialog ):

    def __init__( self, primaryFrame ):
        super( SeriesFilterDialog, self ).__init__( primaryFrame, "Filter Series...", primaryFrame.lists.series )
        self.left = sorted( DataFacade.getSeriesNamesByVolumeIDs( DataFacade.getDriveVolumes() ) )
        self.callback = self.primaryFrame.lists.setSeries
        self.build()

class SeasonFilterDialog( FilterDialog ):

    def __init__( self, primaryFrame ):
        super( SeasonFilterDialog, self ).__init__( primaryFrame, "Filter Seasons...", primaryFrame.lists.seasons )
        self.left = sorted( DataFacade.getSeasonNamesBySeriesIDs( DataFacade.getSeriesIDs() ) )
        self.callback = self.primaryFrame.lists.setSeasons
        self.build()
