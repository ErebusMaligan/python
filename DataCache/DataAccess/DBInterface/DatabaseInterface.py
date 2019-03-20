'''
Created on Sep 22, 2012
 
@author: Daniel J. Rivers
'''
from Utilities import OutputUtils
class DatabaseInterface:

    def __init__( self, dataConnection ):
        self.dc = dataConnection

#create
    def createTable( self, td ):
        s = "CREATE TABLE if not exists " + td.tableName + "(ID INTEGER PRIMARY KEY, "
        for i, v in enumerate( td.columnNames ):
            s += v[ 0 ] + " " + v[ 1 ]
            if i < len( td.columnNames ) - 1:
                s += ","
        s += ")"
        self.dc.cursor.execute( s )
        self.dc.connection.commit()

#metadata        
    def getColumnInfo( self, td ):
        self.dc.cursor.execute( "PRAGMA table_info(" + td.tableName + ")" )
        return self.dc.cursor.fetchall()

#read
    def getAll( self, tableName ):
        self.dc.cursor.execute( "SELECT * FROM " + tableName )
        return self.dc.cursor.fetchall()

#write
    def insert( self, td ):
        s = "INSERT INTO " + td.tableName + " ("
        s += self.listColumns( list( td.values.keys() ), False )
        s += ") VALUES ("
        l = list( td.values.values() )
        s += self.listValues( l )
        s += ")"
        self.dc.cursor.execute( s, l )
        self.dc.connection.commit()
        OutputUtils.debug( "INSERT Executed: " + s + "  PARAMS: " + str( l ) )

#update
    def update( self, td ):
        s = "UPDATE " + td.tableName + " SET "
        s += self.listColumns( list( td.values.keys() ), True )
        s += " WHERE "
        l = list( td.values.values() )
        pk = td.getPKSubset()
        s += self.listColumns( list( pk.keys() ), True )
        for i in pk.values():
            l.append( i )
        self.dc.cursor.execute( s, l )
        self.dc.connection.commit()
        OutputUtils.debug( "UPDATE Executed: " + s + "  PARAMS: " + str( l ) )

#utility methods
    def listColumns( self, l, addQ ):
        s = ""
        i = 0
        while i < len( l ):
            s += l[ i ]
            if addQ:
                s += "=?"
            s = self.addComma( i, s, l )
            i += 1
        return s

    def listValues( self, l ):
        s = ""
        i = 0
        while i < len( l ):
            s += "?"
            s = self.addComma( i, s, l )
            i += 1
        return s

    def addComma( self, i, s, l ):
        if i < len( l ) - 1:
            s += ", "
        return s

    def addAnd( self, i, s, w ):
        if i < len( w ) - 1:
            s += " AND "
        return s

    def getLastID( self ):
        return self.cur.lastrowid
