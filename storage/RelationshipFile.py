from .Relationship import Relationship
import sys, os

class RelationshipFile:

    """RelationshipFile class: representation of relationship file, which stores info about all
    relationships.
    """

    numFiles = 0

    def __init__(self, createFile=True):
        """Constructor for RelationshipFile, which creates the backing file if necessary. """
        RelationshipFile.numFiles += 1
        self.fileID = RelationshipFile.numFiles

        # create relationship file if it doesn't already exist
        self.fileName = "RelationshipFile{0}.store".format(self.fileID)
        self.dir = "datafiles"
        self.filePath = os.path.join(self.dir, self.fileName)
        
        if os.path.exists(os.path.join(self.dir, self.fileName)):
            relFile = open(os.path.join(self.dir, self.fileName), 'r+b')
        else:
            relFile = open(os.path.join(self.dir, self.fileName), 'wb')
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
