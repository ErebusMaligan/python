'''
Created on Sep 3, 2012
 
@author: Daniel J. Rivers
'''
from DataAccess.DBInt import DBInt
from Utilities import OutputUtils

class TableHandler:

    sep = "~"

    @staticmethod
    def writeRecord( l, td ):
        values = []
        where = []
        for i, v in enumerate( l ):
            values.append( ( td.columnNames[ i ][ 0 ], v ) )
            if i <= td.where:
                where.append( ( td.columnNames[ i ][ 0 ], v ) )
        ret = DBInt().merge( tuple( values ), tuple( where ), td )
        OutputUtils.debug( "Merged Record: " + str( values ) )
        return ret

    @staticmethod
    def getRecordByID( i, td ):
        try:
            return DBInt().get( ( ( "ID", i ), ), td )[ 0 ]
        except Exception as e:
            OutputUtils.exception( "No row found", e )

    @staticmethod
    def getAllRecords( td ):
        return DBInt().getAll( td )

    @staticmethod
    def getColumnHeaders( td ):
        ret = []
        for i in td.columnNames [:len( td.columnNames ) - 1]:
            ret.append( i[ 0 ] )
        return ret

    @classmethod
    def getTableSetup( cls, td, l ):
        return [ cls.getColumnHeaders( td ), cls.getValuesForTable( td, l )]

    @staticmethod
    def getValuesForTable( td, l ):
        records = TableHandler.getAllRecords( td )
        ret = []
        for i in records:
            record = i[1:len( td.columnNames )]
            if not l:
                ret.append( record )
            else:
                add = True
                for j in l:
                    if j in record:
                        add = False
                if add:
                    ret.append( record )
        return ret

    @staticmethod
    def getData():
        return None
