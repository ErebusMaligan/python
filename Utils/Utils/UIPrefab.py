'''
@author Daniel J. Rivers
2013

Created: May 9, 2013, 3:56:49 PM 
'''
from tkinter import ttk

class ScrollingList(ttk.Frame):
    
    def __init__(self, parent, heading = None, l = [], width = 2, selectmode = "browse"):
        super().__init__( parent )
        self.heading = heading
        for i in range( width - 1 ):
            self.columnconfigure( i, weight = 1 )            
        self.tree = ttk.Treeview( self, height = 3, selectmode = selectmode )
        self.tree.grid( row = 0, column = 0, columnspan = width - 1, sticky = "NSEW" )
        
        if heading == None:
            self.tree.config( show = "tree" )
        else:
            self.tree.config( show = "headings" )
            self.tree[ "columns" ] = [heading]
            self.tree.heading( heading, text = heading )
                    
        s = ttk.Scrollbar( self, orient = "vertical", command = self.tree.yview )
        self.tree.config( yscrollcommand = s.set )
        s.grid( row = 0, column = width - 1, sticky = "NS" )
        self.l = l
        self.reload()
        
    def reload(self):
        self.__removeAllItems()
        self.__addAllItems()
        self.tree.update()
    
    def addItemToList(self, item):
        if not (item == None or item == ""):
            self.l.append( item )
            self.reload()
        
    def getAllItems(self):
        return self.l
        
    def removeSelectedItem(self):
        sel = self.tree.selection()
        for i in sel:
            print( self.tree.item( i ) )
            self.l = [ x for x in self.l if x != self.tree.item( i )[ "text" ] ]
            self.tree.delete( self.tree.selection() )
        
    def __removeAllItems(self):
        for item in self.tree.get_children():
            self.tree.delete( item )    
    
    def __addAllItems(self):
        for i in self.l:
            self.__addItemToTree( i )        
        
    def __addItemToTree(self, item, index = "end"):
        self.tree.insert( "", index, text = str( item ), values = str( item ) )