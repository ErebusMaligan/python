'''
Created on Aug 28, 2012

@author: Daniel
'''
from DataAccess import DataFacade
from DataAnalysis import DataGrabber
from UI import UIManager

#table creation steps
DataFacade.createAllTables()

#data gathering

DataGrabber.processAll( "drives.txt" )

#create UI

ui = UIManager.PrimaryFrame()
