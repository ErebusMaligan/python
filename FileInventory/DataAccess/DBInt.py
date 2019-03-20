'''
Created on Aug 28, 2012
 
@author: Daniel J. Rivers
'''
from Utilities import TimeUtils, OutputUtils
import sqlite3

class DBInt:

    conn = sqlite3.connect( "TVInventory.sqlite" );

    c = conn.cursor()

#create
    @staticmethod
    def createTable( td ):
            s = "CREATE TABLE if not exists " + td.tableName + "(ID INTEGER PRIMARY KEY, "
            for i, v in enumerate( td.columnNames ):
                s += v[ 0 ] + " " + v[ 1 ]
                if i < len( td.columnNames ) - 1:
                    s += ","
            s += ")"
            DBInt.c.execute( s )

#reads
    @staticmethod
    def getAll( td ):
        DBInt.c.execute( "SELECT * FROM " + td.tableName )
        return DBInt.c.fetchall()

    @staticmethod
    def get( w, td ): #TODO: multiple key where clause
        s = "SELECT * FROM " + td.tableName + " WHERE "
        values = []
        i = 0
        while i < len( w ):
            s += w[ i ][ 0 ] + "=?"
            values.append( w[ i ][ 1 ] )
            s = DBInt.addAnd( i, s, w )
            s += " "
            i += 1
        DBInt.c.execute( s, tuple( values ) )
        ret = DBInt.c.fetchall()
        if ret is None:
            ret = DBInt.c.fetchone()
        return ret


#easier interface for insert/update
    @staticmethod
    def merge( l, w, td ):
        row = DBInt.get( w, td )
        if row:
            row = row[ 0 ]
            DBInt.updateAutoRecord( l, w, td )
            ret = row[ 0 ]
        else:
            simplerL = ()
            for i in l:
                simplerL += ( i[ 1 ], )
            DBInt.insertAutoRecord( simplerL, td )
            ret = DBInt.getLastID()
        return ret

#--------------Everything below this line shouldn't really be called externally without a good reason-------------------------------

#updates - should only be called by merge
    @staticmethod
    def updateAutoRecord( l, w, td ):
        ls = list( l )
        ls.append( ( "TOD", ( TimeUtils.getCurrentTime() ) ) )
        DBInt.updateRecord( tuple( ls ), w, td )

    @staticmethod
    def updateRecord( l, w, td ):
        s = "UPDATE " + td.tableName + " SET "
        values = []
        i = 0;
        while i < len( l ):
            s += l[ i ][ 0 ] + "=?"
            values.append( l[ i ][ 1 ] )
            s = DBInt.addComma( i, s, l )
            s += " "
            i += 1
        s += "WHERE "
        i = 0
        while i < len( w ):
            s += w[ i ][ 0 ] + "=?"
            values.append( w[ i ][ 1 ] )
            s = DBInt.addAnd( i, s, w )
            s += " "
            i += 1
        DBInt.c.execute( s, tuple( values ) )
        OutputUtils.debug( "UPDATE Executed: " + s + "  PARAMS: " + str( values ) )

#inserts - should only be called by merge
    @staticmethod
    def insertAutoRecord( l, td ):
        DBInt.insertRecord( ( None, ) + l + ( TimeUtils.getCurrentTime(), ), td )

    @staticmethod
    def insertRecord( l, td ):
        s = "INSERT INTO " + td.tableName + " VALUES ("
        i = 0;
        while i < len( l ):
            s += "?"
            s = DBInt.addComma( i, s, l )
            i += 1
        s += ")"
        DBInt.c.execute( s, l )
        OutputUtils.debug( "INSERT Executed: " + s + "  PARAMS: " + str( l ) )


#utility methods
    @staticmethod
    def addComma( i, s, l ):
        if i < len( l ) - 1:
            s += ","
        return s

    @staticmethod
    def addAnd( i, s, w ):
        if i < len( w ) - 1:
            s += " AND "
        return s

    @staticmethod
    def getLastID():
        return DBInt.c.lastrowid
