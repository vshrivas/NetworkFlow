from Relationship import Relationship
import sys, os

class RelationshipFile:

    """RelationshipFile class: representation of relationship file, which stores info about all
    relationships.
    """
    MAX_PAGES = 10
    NUMPAGES_OFFSET = 0
    PAGES_OFFSET = 100

    directory = "relstore"

    def __init__(self, fileID):
        """Constructor for RelationshipFile, which creates the backing file if necessary. """
        self.fileID = RelationshipFile.numFiles

        # create relationship file if it doesn't already exist
        self.fileName = "RelationshipFile{0}.store".format(self.fileID)
        self.filePath = os.path.join(self.directory, self.fileName)
        
        if os.path.exists(self.filePath):
            relFile = open(self.filePath, 'r+b')
        else:
            relFile = open(self.filePath, 'wb')
            # write number of relationships to first 4 bytes of relationship file
            relFile.write((0).to_bytes(Relationship.relIDByteLen,
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
