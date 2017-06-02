# Storage: 
# Bytes 1-4: Relationship ID
# Bytes 5-7: Node 1 ID
# Bytes 8-10: Node 2 ID 
# Bytes 11-14: Node 1 Next Rel ID
# Bytes 15-18: Node 1 Prev Rel ID
# Bytes 19-22: Node 2 Next Rel ID
# Bytes 23-26: Node 2 Prev Rel ID
# Bytes 27-126: Relationship Type
# Bytes 127-130: ID of first property for relationship

# Uniqueness:
# If relationship with node 1 = A and node 2 = B exists, a relationship with 
# node 1 = B and node 2 = A should not exist
#from Node import Node 
from .Property import Property
import sys


class Relationship:
    RELATIONSHIP_ID_OFFSET = 0
    NODE1_ID_OFFSET = 4
    NODE2_ID_OFFSET = 7
    NODE1_NEXT_REL_ID_OFFSET = 10
    NODE1_PREV_REL_ID_OFFSET = 14
    NODE2_NEXT_REL_ID_OFFSET = 18
    NODE2_PREV_REL_ID_OFFSET = 22
    RELATIONSHIP_TYPE_OFFSET = 26
    PROPERTY_ID_OFFSET = 126

    MAX_TYPE_SIZE = 100

    storageSize = 130
    numRelationships = 0

    relIDByteLen = 4

    def __init__(self, node1ID, node2ID, relType, relationshipFile, relationshipID=None):
        if relationshipFile != "":
            Relationship.numRelationships = relationshipFile.getNumRelationships()

        print("**** Num Relationships = {0} *****".format(Relationship.numRelationships))

        if relationshipID is None:
            relationshipID = Relationship.numRelationships

        self.firstNodeID = node1ID
        self.secondNodeID = node2ID

        self.type = relType 

        self.properties = []

        self.relationshipID = relationshipID

        if relationshipID != -1 and relationshipID >= Relationship.numRelationships:
            Relationship.numRelationships += 1

        self.relationshipFile = relationshipFile

        if relationshipFile != "":
            # open relationship file
            storeFileName = self.relationshipFile.getFileName()
            storeFile = open(storeFileName, 'r+b')

            # write number of relationships to first 4 bytes of relationship file
            storeFile.write((self.numRelationships).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))

        self.startOffset = self.relationshipID * Relationship.storageSize + Relationship.relIDByteLen

    def getID(self):
        return self.relationshipID 

    def getFirstNodeID(self):
        return self.firstNodeID

    def getSecondNodeID(self):
        return self.secondNodeID
        
    def getOtherNodeID(self, nodeID):
        if(nodeID == self.firstNodeID):
            return self.secondNodeID

        return self.firstNodeID

    def getRelType(self):
        return self.type

    # This method adds property data to a relationship
    def addProperty(self, prop):
        self.properties.append(prop)

    def writeRelationship(self, node, prevRel, nextRel):
        # open relationship file
        print(self.relationshipFile)
        storeFileName = self.relationshipFile.getFileName()
        storeFile = open(storeFileName, 'r+b')

        # seek to location for relationship
        storeFile.seek(self.startOffset)

        # write relationship ID
        storeFile.write(self.relationshipID.to_bytes(Relationship.relIDByteLen, 
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
            storeFile.write(nextRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed=True))

            storeFile.seek(self.startOffset + Relationship.NODE1_PREV_REL_ID_OFFSET)
            storeFile.write(prevRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed=True))

        else:
            print("writing relationship for second node")
            storeFile.seek(self.startOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
            storeFile.write(nextRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed = True))

            storeFile.seek(self.startOffset + Relationship.NODE2_PREV_REL_ID_OFFSET)
            storeFile.write(prevRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed = True))


        # write relationship type
        print("writing relationship type")
        storeFile.seek(self.startOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)

        # type is not of max size
        if(sys.getsizeof(self.type) != self.MAX_TYPE_SIZE):
            # pad value up to max size
            while len(self.type.encode('utf-8')) != self.MAX_TYPE_SIZE:
                self.type += ' '

        storeFile.write(bytearray(self.type, 'utf8'))
        self.type = self.type.rstrip(' ')

        # write first property ID
        storeFile.seek(self.startOffset + Relationship.PROPERTY_ID_OFFSET)

        # if no properties write -1 for first ID
        if len(self.properties) == 0:
            firstProp = -1
            storeFile.write((-1).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            print("wrote first property ID: -1")
        # otherwise write id of first property
        else:
            firstProp = self.properties[0]
            storeFile.write(firstProp.getID().to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))

            print("wrote first property ID: {0}". format(firstProp.getID()))


        # write properties to property file
        print("writing properties to property file ...")

        # write properties to property file
        for propIndex in range(0, len(self.properties)):
            prop = self.properties[propIndex]
            print("writing {0} property ".format(prop.getID()))

            # no next property
            if propIndex == len(self.properties) - 1:
                print("no next property")
                nullProperty = Property("", "", "", -1)
                prop.writeProperty(nullProperty)

            else:
                prop.writeProperty(self.properties[propIndex + 1])

    





