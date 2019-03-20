'''
Created on Sep 2, 2012
 
@author: Daniel J. Rivers
'''
from tkinter import Toplevel, Listbox
from tkinter.constants import VERTICAL, END
from tkinter.ttk import Frame, Button, LabelFrame, Scrollbar

class FilterDialog:

    def __init__( self, primaryFrame, s, l ):
        self.primaryFrame = primaryFrame
        self.top = Toplevel( primaryFrame.getPrimaryFrame() )
        self.top.title( s )
        self.top.rowconfigure( 0, weight = 1 )
        self.top.columnconfigure( 0, weight = 1 )
        self.frame = Frame( self.top )
        self.frame.grid( sticky = "nsew" )
        self.frame.rowconfigure( 0, weight = 1 )
        self.frame.columnconfigure( 0, weight = 1 )
        self.frame.columnconfigure( 4, weight = 1 )
        self.exclude = l

    def build( self ):
        self.buildCenter()
        self.buildRight()
        self.buildLeft()
        self.reload()

    def buildLeft( self ):
        self.left = [ x for x in self.left if x not in self.right ]
        l = LabelFrame( self.frame, text = "Visible" )
        self.leftList = Listbox( l )
        self.leftList.grid( sticky = "nsew" )
        l.grid( column = 0, row = 0, rowspan = 5, columnspan = 3, padx = 10, sticky = "nsew" )
        l.columnconfigure( 0, weight = 1 )
        l.rowconfigure( 0, weight = 1 )
        v = Scrollbar( l, command = self.leftList.yview, orient = VERTICAL )
        v.grid( row = 0, column = 1, sticky = "ns" )
        self.leftList.configure( yscrollcommand = v.set )


    def buildCenter( self ):
        self.bFrame = Frame( self.frame )
        self.bFrame.grid( column = 3, row = 0, rowspan = 5, sticky = "nsew" )
        toRight = Button( self.bFrame, text = "->", command = self.moveRight )
        allRight = Button( self.bFrame, text = "all->", command = self.moveAllRight )
        allLeft = Button( self.bFrame, text = "<-all", command = self.moveAllLeft )
        toLeft = Button( self.bFrame, text = "<-", command = self.moveLeft )
        ok = Button( self.bFrame, text = "OK", command = self.ok )
        toRight.grid( column = 0, row = 0 )
        allRight.grid( column = 0, row = 1 )
        allLeft.grid( column = 0, row = 2 )
        toLeft.grid( column = 0, row = 3 )
        ok.grid( column = 0, row = 4 )
        self.bFrame.rowconfigure( 0, weight = 1 )
        self.bFrame.rowconfigure( 1, weight = 1 )
        self.bFrame.rowconfigure( 2, weight = 1 )
        self.bFrame.rowconfigure( 3, weight = 1 )
        self.bFrame.rowconfigure( 4, weight = 1 )


    def buildRight( self ):
        self.right = self.exclude
        r = LabelFrame( self.frame, text = "Removed" )
        self.rightList = Listbox( r )
        self.rightList.grid( sticky = "nsew" )
        r.grid( column = 4, row = 0, rowspan = 5, columnspan = 3, padx = 10, sticky = "nsew" )
        r.columnconfigure( 0, weight = 1 )
        r.rowconfigure( 0, weight = 1 )
        v = Scrollbar( r, command = self.rightList.yview, orient = VERTICAL )
        v.grid( row = 0, column = 1, sticky = "ns" )
        self.rightList.configure( yscrollcommand = v.set )

    def moveAllRight( self ):
        for i in self.left:
            self.right.append( i )
        self.left = []
        self.reload()

    def moveAllLeft( self ):
        for i in self.right:
            self.left.append( i )
        self.right = []
        self.reload()

    def moveRight( self ):
        if self.leftList.curselection():
            lsel = int( self.leftList.curselection()[ 0 ] )
            self.right.append( self.left[ lsel ] )
            del self.left[ lsel ]
            self.reload()

    def moveLeft( self ):
        if self.rightList.curselection():
            rsel = int( self.rightList.curselection()[ 0 ] )
            self.left.append( self.right[ rsel ] )
            del self.right[ rsel ]
            self.reload()

    def reload( self ):
        self.leftList.delete( 0, END )
        self.rightList.delete( 0, END )
        for i in sorted( self.left ):
            self.leftList.insert( END, i )
        for i in sorted( self.right ):
            self.rightList.insert( END, i )

    def ok( self ):
        self.callback( self.right )
        self.primaryFrame.reload()
        self.top.destroy()
