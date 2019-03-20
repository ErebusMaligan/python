'''
Handles basic file access tasks using a standard File object to facilitate differentiation of concepts like abstract path, vs strict file name

@author Daniel J. Rivers
2013

Created: Apr 24, 2013, 12:51:50 PM
'''
import os

def getSuffix( file ):
    '''Returns the file type suffix, for a given file object
    
    Parameters
    ----------
    file : File
        a File object to retrieve the suffix of
        
    Returns
    -------
    suffix : str
        a string containing the file type suffix
    
    '''
    return file.name[file.name.rfind( "." ) + 1:]


def getFiles( directory ):
    '''Returns file objects for every file in the given directory (only files, not subdirectories)
    
    Parameters
    ----------
    directory : File
        a File object with the path to the directory

    Returns
    -------
    files : File []
        list of Files in the given directory
        
    '''
    return [ File.pathParts( directory.absPath, f ) for f in os.listdir( directory.absPath ) if os.path.isfile( directory.absPath + "/" + f ) ]


def getFilesExcludeType( directory, suffix ):
    '''Returns file objects for every file in the given directory (only files, not subdirectories), excluding files of the given type
    
    Parameters
    ----------
    directory : File
        a File object with the path to the directory
    suffix : str
        a file type suffix to exclude
        
    Returns
    -------
    files : File []
        list of Files in the given directory that do not have the type suffix provided
    
    '''
    return [ f for f in getFiles( directory ) if not f.name.endswith( suffix ) ]

def getFilesOfType( directory, suffix ):
    '''Returns file objects for every file in the given directory (only files, not subdirectories), only including files of the given type
    
    Parameters
    ----------
    directory : File
        a File object with the path to the directory
    suffix : str
        a file type suffix to exclude
        
    Returns
    -------
    files : File []
        list of Files in the given directory that have the type suffix provided
    
    '''
    return [ f for f in getFiles( directory ) if f.name.endswith( suffix ) ]

def getSubDir( directory ):
    '''Returns file objects for every subdirectory in the given directory
    
    Parameters
    ----------
    directory : File
        a File object with the path to the directory
        
    Returns
    -------
    dirs : File []
        list of Subdirectories in the given directory
    
    '''
    return [ File.pathFull( directory.absPath + "/" + name ) for name in os.listdir( directory.absPath ) if os.path.isdir( directory.absPath + "/" + name ) ]

def moveFiles( destDir, files ):
    '''Moves the files provided to the destination directory
    
    Parameters
    ----------
    directory : File
        a File object with the path to the directory
    files : File[]
        a list of File objects to move
    
    '''
    if not os.path.exists( destDir.absPath ):
        os.makedirs( destDir.absPath )
    for f in files:
        n = File.pathParts( destDir.absPath, f.name )
        os.rename( f.absPath, n.absPath )


def deleteDirectory( directory ):
    '''Delete the provided directory
    
    Parameters
    ----------
    directory : File
        a File object with the path to the directory

    '''
    os.rmdir( directory.absPath )


class File():
    '''Encapsulates the various path string components of a file location into a standardized object
        
        Attributes
        ----------
        path : str
            the path location of the file, not including the final filename
        name : str
            the file name of the file
        absPath : str
            the full abstract path of the file - ( path / name )
    
    '''

    def __init__( self, path = None, name = None ):
        '''Constructor always requires both a path and a name, though either can be None. 
        
        THIS METHOD SHOULD NOT BE CALLED DIRECTLY
        
        Attributes
        ----------
        path : str
            the path location of the file
        name : str
            the file name of the file
        
        '''
        self.path = path
        self.name = name
        self.absPath = ( None if path == None else path + ( "" if name == None else "/" + name ) )

    @classmethod
    def pathFull( cls, path ):
        '''Create a file from a full abstract path
        
        Valid full path is expected, not putting full error check code for this because it's annoying
        
        Attributes
        ----------
        path : str
            the full abstract path location of the file
            
        Returns
        -------
        file : File
            Constructed File object based on the path provided
        
        '''
        return cls( None if path == None else path.rsplit( "/", 1 )[ 0 ], None if path == None else path.rsplit( "/", 1 )[ 1 ] )

    @classmethod
    def pathParts( cls, path, name ):
        '''Create a file from a path and file name
        
        Attributes
        ----------
        path : str
            the path location of the file
            
        name : str
            the name of the file
            
        Returns
        -------
        file : File
            Constructed File object based on the path and name provided
        
        '''
        return cls( path, name )

    def isDir( self ):
        '''Check if this File object only refers to a directory and not an actual file
        
        Returns
        -------
        isDir : bool
            True if this is only a directory, False if it's a file
        
        '''
        return self.name == None
