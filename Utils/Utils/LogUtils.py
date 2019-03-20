'''
Utilities for SIMPLE logging

@author Daniel J. Rivers
2013

Created: Mar 21, 2013, 1:25:43 PM 
'''
from datetime import datetime
from tkinter import *
import time
import logging
import os
from threading import Thread

class Log:
    '''Class for setting up and appending to a central log file'''
    
    formatter = logging.Formatter( "%(asctime)s  (%(levelname)s):\t%(message)s", "%Y-%m-%d %H:%M:%S" )
    
    def __init__( self, path, name ):
        '''Sets up all the logging filters and handlers'''
        logger = logging.getLogger()
        logger.addFilter( NoEmptyFilter() )
        handlers = [logging.FileHandler( path + os.sep + name + "-" + str( datetime.now() ).replace( " ", "_" ).replace( ":", "-" ) + ".log" ), logging.StreamHandler(), logging.StreamHandler( LogStream( LogWindow.getInstance() ) )]
        logger.setLevel( logging.INFO )
        for h in handlers:
            h.setFormatter( Log.formatter )
            logger.addHandler( h )
            
        
    @staticmethod
    def info( msg ):
        '''append the given message to the log as info category
        
        Parameters
        ----------
        msg : str
            Message to append to the log
        
        '''
        logging.getLogger().info( msg )
    
    @staticmethod    
    def closeCurrentLog():
        '''close the current file log being written to'''
        log = logging.getLogger()
        '''copy the list becuase removing while iterating messes it up'''
        for i in list( log.handlers ): 
            log.removeHandler(i)
            i.flush()
            i.close()

class NoEmptyFilter( logging.Filter ):
    '''Filter class that excludes messages that are empty'''
    
    def filter( self, record ):
        '''Method that executes the filtering of a message
        
        Parameters
        ----------
        record : LogRecord
            Incoming log record object
        
        '''
        return not record.getMessage() == ""


def logProcessOutput( proc, conditional ):
    '''Reads from an externally launched OS process and prints any output from said process to standard info of the log
    
    Parameters
    ----------
    proc : Process
        Process that is being run by the native OS
    conditional : Function
        Boolean evaluation function that checks the input variable for some string matching condition.
    
    
    '''
    while True:
        line = proc.stdout.readline().decode( 'utf-8' )
        if not line:
            break
        if ( conditional == None ) or conditional( line ):
            Log.info( line.strip() )
            if LogWindow.instance != None:
                LogWindow.getInstance().update()

            
class LogWindow():
    
    instance = None
    
    def __init__(self):
        self.lw = Tk()
        self.lw.protocol( "WM_DELETE_WINDOW", lambda: self.destroyed() )
        self.lw.title( "Console Log" )
        self.lw.geometry( "900x400" )
        self.s = ttk.Scrollbar( self.lw )
        self.t = Text( self.lw, wrap = None, width = 800 )
        self.t.focus_set()
        self.s.pack( side = RIGHT, fill = Y )
        self.t.pack( side = LEFT, fill = Y )
        self.s.config( command = self.t.yview )
        self.t.config( yscrollcommand = self.s.set )
    
    def write(self, msg):
        self.t.insert( END, msg )
        self.t.see( END )
    
    @classmethod
    def getInstance( cls ):
        if cls.instance is None:
            cls.instance = LogWindow()
        return cls.instance
    
    def update(self):
        self.lw.update()
        
    def destroyed(self):
        self.lw.destroy()
        self.lw = None
        LogWindow.instance = None

    
    
class LogStream():
    
    def __init__(self, lw):
        self.lw = lw
    
    def write(self, msg):
        self.lw.write( msg )