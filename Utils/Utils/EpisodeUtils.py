'''
Contains functions that are domain specific to TV Episode ripping

@author Daniel J. Rivers
2013

Created: Apr 23, 2013, 3:07:03 PM 
'''
def addZeroes( s ):
    '''Adds a 0 to any numeric string that is less than 10, otherwise returns the same input string.
    
    DOES NOT CHECK TO SEE IF A VALID NUMERIC STRING IS PASSED
    
    Parameters
    ----------
    s : str
        numeric string input
        
    Returns
    -------
    s+ : str
        string containing contents of s with a 0 prepended to it if it is a 1 digit number
        
    '''
    return "0" + s if len( s ) < 2 else s