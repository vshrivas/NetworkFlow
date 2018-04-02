from .Node import Node
from .Property import Property
from .Relationship import Relationship
from .Label import Label
from .NodePage import NodePage
import sys, struct, os

class PropertyFile:

    """PropertyFile class: representation of property file, which stores info about all
    properties.
    """

    # number of property files
    MAX_PAGES = 10
    NUMPAGES_OFFSET = 0
    PAGES_OFFSET = 100

    NUMPAGES_SIZE = 100

    directory = "propertystore"

    def __init__(self, fileID):
        """Constructor for PropertyFile, which creates the backing file if necessary. """
        self.fileID = fileID

        # create property file if it doesn't already exist
        self.fileName = "PropertyFile{0}.store".format(self.fileID)
        self.filePath = os.path.join(self.directory, self.fileName)

        self.numPages = 0

        if os.path.exists(self.filePath):
            print('property file exists')
            propertyFile = open(self.filePath, 'rb')
            self.numPages = int.from_bytes(propertyFile.read(self.NUMPAGES_SIZE), sys.byteorder, signed=True)
            print('has {0} pages'.format(self.numPages))
        else:
            print('creating new property file')
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            propertyFile = open(self.filePath, 'wb')
            # write number of pages to first 3 bytes of node file
            propertyFile.write((0).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        propertyFile.close()

    def createPage(self):
        propertyPage = PropertyPage(self.numPages, self, True)
        self.numPages += 1
            
        propertyFile = open(self.filePath, 'r+b')
        propertyFile.write((self.numPages).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        propertyFile.close()

        return propertyPage

    def getFileName(self):
        """Return file name of backing file."""
        return self.fileName

    def getFilePath(self):
        return self.filePath

    def getNumProperties(self):
        """Return number of properties. """
        propertyFile = open(self.filePath, 'r+b')
        numProperties = int.from_bytes(propertyFile.read(Property.propIDByteLen), byteorder=sys.byteorder, signed=True)
        return numProperties
