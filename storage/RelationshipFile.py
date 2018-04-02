from .Relationship import Relationship
from .RelationshipPage import RelationshipPage
import sys, os

class RelationshipFile:

    """RelationshipFile class: representation of relationship file, which stores info about all
    relationships, including number of pages.
    """
    MAX_PAGES = 10
    NUMPAGES_OFFSET = 0
    PAGES_OFFSET = 100

    NUMPAGES_SIZE = 100

    directory = "relstore"

    def __init__(self, fileID):
        """Constructor for RelationshipFile, which creates the backing file if necessary. """
        self.fileID = fileID

        # create relationship file if it doesn't already exist
        self.fileName = "RelationshipFile{0}.store".format(self.fileID)
        self.filePath = os.path.join(self.directory, self.fileName)
        
        self.numPages = 0

        if os.path.exists(self.filePath):
            print('rel file exists')
            relFile = open(self.filePath, 'rb')
            self.numPages = int.from_bytes(relFile.read(self.NUMPAGES_SIZE), sys.byteorder, signed=True)
            print('has {0} pages'.format(self.numPages))
        else:
            print('creating new rel file')
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            relFile = open(self.filePath, 'wb')
            # write number of pages to first 3 bytes of relationship file
            relFile.write((0).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        relFile.close()

    # creates a rel page
    def createPage(self):
        RelationshipPage(self.numPages, self, True)
        self.numPages += 1
            
        relFile = open(self.filePath, 'r+b')
        relFile.write((self.numPages).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        relFile.close()

    def getFileName(self):
        """Return file name of backing file."""
        return self.fileName

    def getFilePath(self):
        return self.filePath

    def getNumRelationships(self):
        """Return number of relationships. """
        relFile = open(self.filePath, 'r+b')
        numRelationships = int.from_bytes(relFile.read(Relationship.relIDByteLen), byteorder=sys.byteorder, signed=True)
        return numRelationships
