from Node import Node
from Property import Property
from Relationship import Relationship
from Label import Label
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

        print("reading relationships")

        # while there is a next relationship
        while nextRelID != -1:
            print(nextRelID)
            relationshipStartOffset = nextRelID * Relationship.storageSize

            # find ID of first node in relationship
            relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_ID_OFFSET)
            node1ID = int.from_bytes(relationshipStore.read(3), sys.byteorder, signed=True)

            # find ID of second node in relationship
            relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_ID_OFFSET)
            node2ID = int.from_bytes(relationshipStore.read(3), sys.byteorder, signed=True)

            # create relationship and add to node
            rel = Relationship(node1ID, node2ID, relationshipFile)
            rel.relationshipID = nextRelID
            node.addRelationship(rel)

            # find next rel ID
            if nodeID == node1ID:
                relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
                nextRelID = int.from_bytes(relationshipStore.read(4), sys.byteorder, signed=True)
                
            else:
                relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
                nextRelID = int.from_bytes(relationshipStore.read(4), sys.byteorder, signed=True)
        
        print("reading properties")

        # read first property ID
        nodeStore.seek(nodeStartOffset + Node.PROPERTY_ID_OFFSET)
        firstPropID = int.from_bytes(nodeStore.read(4), sys.byteorder, signed=True)

        propertyStore = open(propertyFile.getFileName(), 'rb')
        nextPropID = firstPropID

        while nextPropID != -1:
            print()
            print('for node: {0}'.format(nodeID))
            print('first prop id: {0}'. format(firstPropID))
            print(nextPropID)
            propertyStartOffset = nextPropID * Property.storageSize

            # find ID
            propertyStore.seek(propertyStartOffset)
            print("seek to {0} for ID". format(propertyStartOffset))
            ID = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)
            #key = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)
            print('id: {0}'.format(ID))

            # find key
            propertyStore.seek(propertyStartOffset + Property.KEY_OFFSET)
            print("seek to {0} for key". format(propertyStartOffset + Property.KEY_OFFSET))
            key = propertyStore.read(4).decode("utf-8")
            #key = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)
            print('key: {0}'.format(key))

            # find value
            propertyStore.seek(propertyStartOffset + Property.VALUE_OFFSET)
            print("seek to {0} for value". format(propertyStartOffset + Property.VALUE_OFFSET))
            #value = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)
            value = propertyStore.read(4).decode("utf-8")
            print('value: {0}'.format(value))

            # create property and add to node
            prop = Property(key, value, propertyFile, nextPropID)
            node.addProperty(prop)

            # find next property id
            propertyStore.seek(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET)
            print("seek to {0} for next property id". format(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET))
            nextPropID = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)
            print("next prop id is {0}".format(nextPropID))

        # read first label id
        nodeStore.seek(nodeStartOffset + Node.LABEL_ID_OFFSET)
        firstLabelID = int.from_bytes(nodeStore.read(3), sys.byteorder, signed=True)
        nextLabelID = firstLabelID

        labelStore = open(labelFile.getFileName(), 'rb')

        print("reading labels")
         
        while nextLabelID != -1:
            print('for node: {0}'.format(nodeID))
            # read label and add it to node
            labelStartOffset = nextLabelID * Label.storageSize
            print('label start offset:{0}'.format(labelStartOffset))

            labelStore.seek(labelStartOffset)
            label = labelFile.readLabel(nextLabelID)
            node.addLabel(label)

            # find next label id
            labelStore.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
            nextLabelID = int.from_bytes(labelStore.read(3), sys.byteorder, signed=True)
            print (nextLabelID)

        return node











        
