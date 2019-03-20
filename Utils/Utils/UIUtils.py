'''
@author Daniel J. Rivers
2013

Created: May 1, 2013, 4:13:57 PM 
'''
from tkinter import ttk
from tkinter import filedialog

def buildEntryPair( frame, text, textvariable, row, column, cOffset = 0, width = None ):
    gridIt( ttk.Label( frame, text = text ), row, column, 1, "E" )
    gridIt( ttk.Entry( frame, textvariable = textvariable, width = width ), row, column + cOffset + 1, 1, "W" )

def buildFrame( parent, columns ):
    f = ttk.Frame( parent )
    for i in range( columns ):
        f.columnconfigure( i, weight = 1 )
    return f

def setVerticalExpand( container, rows ):
    for i in range( rows ):
        container.rowconfigure( i, weight = 1 )

def gridIt( item, row, column, width = 1, sticky = None ):
    item.grid( row = row, column = column, columnspan = width, padx = 2, pady = 5, sticky = sticky )
    
def buildDirButtonOnly( frame, lblText, var, row, column, width = 1, cOffset = 0 ):
    gridIt( ttk.Label( frame, text = lblText ), row, column, width, "E" )
    gridIt( ttk.Button( frame, textvariable = var, command = lambda: var.set( filedialog.askdirectory( initialdir = var.get() ) ) ), row, column + cOffset + 1, width, "W" )
    
def buildDirEntry( frame, lblText, var, row, column, cOffset = 0 ):
    gridIt( ttk.Label( frame, text = lblText ), row, column, 1, "E" )
    gridIt( ttk.Entry( frame, textvariable = var, width = 20 ), row, column + cOffset + 1, 1, "EW" )
    gridIt( ttk.Button( frame, text = "Browse...", width = 7, command = lambda: var.set( filedialog.askdirectory( initialdir = var.get() ) ) ), row, column + cOffset + 2, 1, "EW" )