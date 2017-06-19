from .Node import Node
from .Property import Property
from .Relationship import Relationship
from .Label import Label
import sys

DEBUG = False

class NodeFile(object):

    """NodeFile class: representation of node file, which stores info about all
    nodes. A NodeFile object can read nodes from the backing node file and stores 
    the current number of nodes.
    """

    # number of node files
    numFiles = 0

    def __init__(self):
        """Constructor for NodeFile, which creates the backing file if necessary. """
        NodeFile.numFiles += 1
        self.fileID = NodeFile.numFiles

        # create node file if it doesn't already exist
        self.fileName = "NodeFile{0}.store".format(self.fileID)
        try:
            nodeFile = open(self.fileName, 'r+b')
        except FileNotFoundError:
            nodeFile = open(self.fileName, 'wb')
            # write number of nodes to first 3 bytes of node file
            nodeFile.write((0).to_bytes(Node.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))
        nodeFile.close()

    def getFileName(self):
        """Return file name of backing file."""
        return self.fileName

    def getNumNodes(self):
        """Return number of nodes."""
        nodeFile = open(self.fileName, 'r+b')
        numNodes = int.from_bytes(nodeFile.read(Node.nodeIDByteLen), byteorder=sys.byteorder, signed=True)
        return numNodes

    def readNode(self, nodeID, relationshipFile, propertyFile, labelFile):
        """Read the node corresponding to a given node ID and return a node object for it.

        Arguments:
        nodeID: node ID of node to be returned
        relationshipFile: RelationshipFile object to read relationships from
        propertyFile: PropertyFile object to read properties from
        labelFile: LabelFile object to read labels from
        """
        node = Node(self, nodeID)
        nodeStore = open(self.fileName, 'rb')
        propertyStore = open(propertyFile.getFileName(), 'rb')
        nodeStartOffset = nodeID * Node.storageSize + Node.nodeIDByteLen

        # find all relationships
        # read first rel ID
        nodeStore.seek(nodeStartOffset + Node.REL_ID_OFFSET)
        firstRelID = int.from_bytes(nodeStore.read(4), byteorder=sys.byteorder, signed=True)

        relationshipStore = open(relationshipFile.getFileName(), 'rb')
        nextRelID = firstRelID

        if DEBUG:
            print("reading relationships")

        # while there is a next relationship
        while nextRelID != -1:
            if DEBUG:
                print(nextRelID)
            # find starting offset of relationship in relationship file
            relationshipStartOffset = nextRelID * Relationship.storageSize + Relationship.relIDByteLen

            # find ID of first node in relationship
            relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_ID_OFFSET)
            node1ID = int.from_bytes(relationshipStore.read(3), sys.byteorder, signed=True)

            # find ID of second node in relationship
            relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_ID_OFFSET)
            node2ID = int.from_bytes(relationshipStore.read(3), sys.byteorder, signed=True)

            # read in type of relationship
            relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)
            relType = relationshipStore.read(Relationship.MAX_TYPE_SIZE).decode("utf-8")
            relType = relType.rstrip(' ')

            if DEBUG:
                print('Node 1 id: {0}'.format(node1ID))
                print('Node 2 id: {0}'.format(node2ID))
                print('Relationship type: {0}'.format(relType))

            # create relationship and add to node
            rel = Relationship(node1ID, node2ID, relType, relationshipFile, nextRelID)
            #rel.relationshipID = nextRelID
            node.addRelationship(rel)

            # read in relationship properties
            # read in first property ID
            relationshipStore.seek(relationshipStartOffset + Relationship.PROPERTY_ID_OFFSET)
            firstRelPropID = int.from_bytes(relationshipStore.read(Property.propIDByteLen), sys.byteorder, signed=True)

            nextRelPropID = firstRelPropID
            if DEBUG:
                print ('Reading in properties for rel {0}...'.format(nextRelID))
            # while there is a next property for the relationship
            while nextRelPropID != -1:
                if DEBUG:
                    print()
                    print('for rel: {0}'.format(nextRelID))
                    print('first prop id: {0}'. format(firstRelPropID))
                    print(nextRelPropID)
                # find starting offset of property
                propertyStartOffset = nextRelPropID * Property.storageSize + Property.propIDByteLen

                # find ID
                propertyStore.seek(propertyStartOffset)
                if DEBUG:
                    print("seek to {0} for ID". format(propertyStartOffset))
                ID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
                if DEBUG:
                    print('id: {0}'.format(ID))

                # find key
                propertyStore.seek(propertyStartOffset + Property.KEY_OFFSET)
                if DEBUG:
                    print("seek to {0} for key". format(propertyStartOffset + Property.KEY_OFFSET))
                key = propertyStore.read(Property.MAX_KEY_SIZE).decode("utf-8")
                # strip padding from key
                key = key.rstrip(' ')
                if DEBUG:
                    print('key: {0}'.format(key))

                # find value
                propertyStore.seek(propertyStartOffset + Property.VALUE_OFFSET)
                if DEBUG:
                    print("seek to {0} for value". format(propertyStartOffset + Property.VALUE_OFFSET))
                value = propertyStore.read(Property.MAX_VALUE_SIZE).decode("utf-8")
                # strip padding from value
                value = value.rstrip(' ')
                if DEBUG:
                    print('value: {0}'.format(value))

                # initialize property object with key and value and add to relationship
                prop = Property(key, value, propertyFile, nextRelPropID)
                rel.addProperty(prop)

                # find next property id
                propertyStore.seek(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET)
                if DEBUG:
                    print("seek to {0} for next property id". format(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET))
                nextRelPropID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
                if DEBUG:
                    print("next prop id is {0}".format(nextRelPropID))            

            # find next rel ID
            if nodeID == node1ID:
                relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
                nextRelID = int.from_bytes(relationshipStore.read(4), sys.byteorder, signed=True)

            else:
                relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
                nextRelID = int.from_bytes(relationshipStore.read(4), sys.byteorder, signed=True)

        if DEBUG:
            print("reading properties")

        # read first property ID
        nodeStore.seek(nodeStartOffset + Node.PROPERTY_ID_OFFSET)
        firstPropID = int.from_bytes(nodeStore.read(4), sys.byteorder, signed=True)

        nextPropID = firstPropID
        # while there is a next property
        while nextPropID != -1:
            if DEBUG:
                print()
                print('for node: {0}'.format(nodeID))
                print('first prop id: {0}'. format(firstPropID))
                print(nextPropID)
            # find starting offset of property in property file
            propertyStartOffset = nextPropID * Property.storageSize + Property.propIDByteLen

            # find ID
            propertyStore.seek(propertyStartOffset)
            if DEBUG:
                print("seek to {0} for ID". format(propertyStartOffset))
            ID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
            if DEBUG:
                print('id: {0}'.format(ID))

            # find key
            propertyStore.seek(propertyStartOffset + Property.KEY_OFFSET)
            if DEBUG:
                print("seek to {0} for key". format(propertyStartOffset + Property.KEY_OFFSET))
            key = propertyStore.read(Property.MAX_KEY_SIZE).decode("utf-8")
            key = key.rstrip(' ')
            if DEBUG:
                print('key: {0}'.format(key))

            # find value
            propertyStore.seek(propertyStartOffset + Property.VALUE_OFFSET)
            if DEBUG:
                print("seek to {0} for value". format(propertyStartOffset + Property.VALUE_OFFSET))
            value = propertyStore.read(Property.MAX_VALUE_SIZE).decode("utf-8")
            value = value.rstrip(' ')
            if DEBUG:
                print('value: {0}'.format(value))

            # create property and add to node
            prop = Property(key, value, propertyFile, nextPropID)
            node.addProperty(prop)

            # find next property id
            propertyStore.seek(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET)
            if DEBUG:
                print("seek to {0} for next property id". format(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET))
            nextPropID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
            if DEBUG:
                print("next prop id is {0}".format(nextPropID))

        # read first label id
        nodeStore.seek(nodeStartOffset + Node.LABEL_ID_OFFSET)
        firstLabelID = int.from_bytes(nodeStore.read(3), sys.byteorder, signed=True)
        nextLabelID = firstLabelID

        labelStore = open(labelFile.getFileName(), 'rb')

        if DEBUG:
            print("reading labels")

        # while there is a next label
        while nextLabelID != -1:
            if DEBUG:
                print('for node: {0}'.format(nodeID))
            # read label and add it to node
            labelStartOffset = nextLabelID * Label.storageSize + Label.labelIDByteLen
            if DEBUG:
                print('label start offset:{0}'.format(labelStartOffset))

            labelStore.seek(labelStartOffset)
            label = labelFile.readLabel(nextLabelID)
            node.addLabel(label)
            if DEBUG:
                print(label.label)

            # find next label id
            labelStore.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
            nextLabelID = int.from_bytes(labelStore.read(3), sys.byteorder, signed=True)
            if DEBUG:
                print (nextLabelID)

        return node












