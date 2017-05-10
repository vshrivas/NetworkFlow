# Storage: 
# Bytes 1-4: Relationship ID
# Bytes 5-7: Node 1 ID
# Bytes 8-10: Node 2 ID 
# Bytes 11-14: Node 1 Next Rel ID
# Bytes 15-18: Node 1 Prev Rel ID
# Bytes 19-22: Node 2 Next Rel ID
# Bytes 23-26: Node 2 Prev Rel ID

# Uniqueness:
# If relationship with node 1 = A and node 2 = B exists, a relationship with 
# node 1 = B and node 2 = A should not exist
#from Node import Node 
import sys


class Relationship:
    RELATIONSHIP_ID_OFFSET = 0
    NODE1_ID_OFFSET = 4
    NODE2_ID_OFFSET = 7
    NODE1_NEXT_REL_ID_OFFSET = 10
    NODE1_PREV_REL_ID_OFFSET = 14
    NODE2_NEXT_REL_ID_OFFSET = 18
    NODE2_PREV_REL_ID_OFFSET = 22

    storageSize = 26
    numRelationships = 0

    relIDByteSize = 4

    def __init__(self, node1ID, node2ID, relationshipFile, relationshipID=None):
        if relationshipID is None:
            relationshipID = Relationship.numRelationships
        self.firstNodeID = node1ID
        self.secondNodeID = node2ID

        self.relationshipID = relationshipID

        if relationshipID != -1:
            Relationship.numRelationships += 1

        self.relationshipFile = relationshipFile

        self.startOffset = self.relationshipID * Relationship.storageSize

    def getID(self):
        return self.relationshipID 

    def getOtherNodeID(self, nodeID):
        if(nodeID == self.firstNodeID):
            return self.secondNodeID

        return self.firstNodeID

    def writeRelationship(self, node, prevRel, nextRel):
        # open relationship file
        print(self.relationshipFile)
        storeFileName = self.relationshipFile.getFileName()
        storeFile = open(storeFileName, 'r+b')

        # seek to location for relationship
        storeFile.seek(self.startOffset)

        # write relationship ID
        storeFile.write(self.relationshipID.to_bytes(Relationship.relIDByteSize, 
            byteorder = sys.byteorder, signed=True))
        print("wrote relationship id")

        # write node 1 id
        storeFile.seek(self.startOffset + Relationship.NODE1_ID_OFFSET)
        storeFile.write(self.firstNodeID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))
        print("wrote first node id")

        # write node 2 id
        storeFile.seek(self.startOffset + Relationship.NODE2_ID_OFFSET)
        storeFile.write(self.secondNodeID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))
        print("wrote second node id")

        # find which node relationship is being written for
        if node.getID() == self.firstNodeID:
            print("writing relationship for first node")

            storeFile.seek(self.startOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
            storeFile.write(nextRel.getID().to_bytes(Relationship.relIDByteSize, 
                byteorder = sys.byteorder, signed=True))

            storeFile.seek(self.startOffset + Relationship.NODE1_PREV_REL_ID_OFFSET)
            storeFile.write(prevRel.getID().to_bytes(Relationship.relIDByteSize, 
                byteorder = sys.byteorder, signed=True))

        else:
            print("writing relationship for second node")
            storeFile.seek(self.startOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
            storeFile.write(nextRel.getID().to_bytes(Relationship.relIDByteSize, 
                byteorder = sys.byteorder, signed = True))

            storeFile.seek(self.startOffset + Relationship.NODE2_PREV_REL_ID_OFFSET)
            storeFile.write(prevRel.getID().to_bytes(Relationship.relIDByteSize, 
                byteorder = sys.byteorder, signed = True))

    





