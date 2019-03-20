'''
Created on Sep 1, 2012
 
@author: Daniel J. Rivers
'''
from tkinter.constants import VERTICAL
from tkinter.ttk import Labelframe, Treeview, Scrollbar

class SimpleTable:

    def __init__( self, parent, c, s, label ):
        self.columns = c[ 0 ]
        self.values = c[ 1 ]
        self.sizes = s
        self.frame = Labelframe( parent, text = label )
        self.createTree()
        self.setHeadings()
        self.setValues()
        self.setSizes()
        self.addScrollBars()
        self.pack()

    def pack( self ):
        self.vertical.grid( column = 1, sticky = "ns" )
        self.tree.grid( column = 0, row = 0, sticky = "nsew" )
        self.frame.grid( column = 0, row = 0, sticky = "nsew" )
        self.frame.columnconfigure( 0, weight = 1 )
        self.frame.rowconfigure( 0, weight = 1 )

    def createTree( self ):
        self.tree = Treeview( self.frame, selectmode = "browse" )
        self.tree[ "show" ] = "headings"
        self.tree[ "columns" ] = self.columns

    def setHeadings( self ):
        for i in self.columns:
            self.tree.heading( i, text = i )

    def setValues( self ):
        for i in sorted( self.values ):
            self.tree.insert( "", "end", text = i[ 0 ], values = i )

    def setSizes( self ):
        if self.sizes != None:
            for i, v in enumerate( self.sizes ):
                self.tree.column( self.columns[ i ], width = v, anchor = "center" )

    def addScrollBars( self ):
        self.vertical = Scrollbar( self.frame, command = self.tree.yview, orient = VERTICAL )
        self.tree.configure( yscrollcommand = self.vertical.set )

    def reload( self ):
        for item in self.tree.get_children():
            self.tree.delete( item )
        self.setValues()
