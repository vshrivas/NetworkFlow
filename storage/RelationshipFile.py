from .Relationship import Relationship
import sys

class RelationshipFile:
    numFiles = 0

    def __init__(self, createFile=True):
        RelationshipFile.numFiles += 1
        self.fileID = RelationshipFile.numFiles

        # create relationship file if it doesn't already exist
        self.fileName = "RelationshipFile{0}.store".format(self.fileID)
        try:
            relFile = open(self.fileName, 'r+b')
        except FileNotFoundError:
            relFile = open(self.fileName, 'wb')
            # write number of relationships to first 4 bytes of relationship file
            relFile.write((0).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))
        relFile.close()

    def getFileName(self):
        return self.fileName

    def getNumRelationships(self):
        relFile = open(self.fileName, 'r+b')
        numRelationships = int.from_bytes(relFile.read(Relationship.relIDByteLen), byteorder=sys.byteorder, signed=True)
        return numRelationships
