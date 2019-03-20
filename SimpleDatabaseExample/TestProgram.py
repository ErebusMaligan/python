'''
Created on Sep 22, 2012
 
@author: Daniel J. Rivers
'''

from DataAccess.BasicCacheProxy import BasicCacheProxy
from TableData import TableData
from Utilities import OutputUtils
import copy

OutputUtils.logLevel = 3

cacheProxy = BasicCacheProxy( "TVInventory.sqlite", ["DRIVE"] )
handler = cacheProxy.getHandler( "DRIVE" )

for i in handler.getByCriteria( { "LETTER" : "ZZZ" } ):
    x = copy.deepcopy( i )
    x.values[ "URI" ] = "Y"
    handler.merge( x )

t = TableData.defaultTableData( "DRIVE", cacheProxy.cache )
t.values = { "VOLUME" : "TEST", "URI" : "TEST", "LETTER" : "TEST", "TOTAL_SPACE" : "TEST", "FREE_SPACE" : "TEST", "USAGE" : "TEST", "TOD" : "TEST" }
handler.merge( t )
