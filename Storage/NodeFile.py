from Node import Node
from Property import Property
from Relationship import Relationship
import sys

class NodeFile(object):
    numFiles = 0

    def __init__(self):
        NodeFile.numFiles += 1
        self.fileID = NodeFile.numFiles
        
        # create node file
        self.fileName = "NodeFile{0}".format(self.fileID)
        nodeFile = open(self.fileName, 'wb')
        nodeFile.close()

    def getFileName(self):
        return self.fileName

    # This method reads a given node based on nodeID and returns a node object for it
    def readNode(self, nodeID, relationshipFile, propertyFile, labelFile):
        node = Node(self)

        nodeStore = open(self.fileName, 'rb')
        nodeStartOffset = nodeID * Node.storageSize

        # TODO: refactor some of reading relationships and properties into those classes

        # find all relationships
        # read first rel ID
        nodeStore.seek(nodeStartOffset + Node.REL_ID_OFFSET)
        firstRelID = int.from_bytes(nodeStore.read(4), byteorder=sys.byteorder, signed=True)

        relationshipStore = open(relationshipFile.getFileName(), 'rb')
        nextRelID = firstRelID

        # while there is a next relationship
        while nextRelID != -1:
            relationshipStartOffset = nextRelID * Relationship.storageSize

            # find ID of first node in relationship
            relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_ID_OFFSET)
            node1ID = int.from_bytes(relationshipStore.read(3), sys.byteorder, signed=True)

            # find ID of second node in relationship
            relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_ID_OFFSET)
            node2ID = int.from_bytes(relationshipStore.read(3), sys.byteorder, signed=True)

            # create relationship and add to node
            rel = Relationship(node1ID, node2ID, relationshipFile)
            node.addRelationship(rel)

            # find next rel ID
            if nodeID == node1ID:
                relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
                nextRelID = int.from_bytes(relationshipStore.read(4), sys.byteorder, signed=True)
            else:
                relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
                nextRelID = int.from_bytes(relationshipStore.read(4), sys.byteorder, signed=True)


        # read first property ID
        nodeStore.seek(nodeStartOffset + Node.PROPERTY_ID_OFFSET)
        firstPropID = int.from_bytes(nodeStore.read(4), sys.byteorder, signed=True)

        propertyStore = open(propertyFile.getFileName(), 'rb')
        nextPropID = firstPropID

        while nextPropID != -1:
            propertyStartOffset = nextPropID * Property.storageSize

            # find key
            propertyStore.seek(propertyStartOffset + Property.KEY_OFFSET)
            key = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)

            # find value
            propertyStore.seek(propertyStartOffset + Property.VALUE_OFFSET)
            value = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)

            # create property and add to node
            prop = Property(key, value, propertyFile)
            node.addProperty(prop)

            # find next property id
            propertyStore.seek(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET)
            nextPropID = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)

        # read first label id
        nodeStore.seek(nodeStartOffset + Node.LABEL_STORE_PTR_OFFSET)
        firstLabelID = int.from_bytes(nodeFile.read(3), sys.byteorder, signed=True)
        nextLabelID = firstLabelID

        while nextLabelID != -1:
            # read label and add it to node
            labelStartOffset = nextLabelID * Label.storageSize
            labelFile.seek(labelStartOffset)
            label = labelFile.readLabel(nextLabelID)
            node.addLabel(label)

            # find next label id
            labelFile.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
            nextLabelID = int.from_bytes(labelFile.read(3), sys.byteorder, signed=True)

        return node











        
