# Node class: stores data

# Storage: Nodes will be stored as fixed size records which are 9 bytes in
# length.
# Bytes 1-3: Node ID
# Byte 4: In-use flag (1 for in-use, 0 for not)
# Bytes 5-8: ID of first relationship connected to node
# Bytes 9-12: ID of first property (key-value pair) for node
# Bytes 13-15: ID of first label for node
# Byte 16: flags

from .Relationship import Relationship
from .Property import Property
from .Label import Label
import sys

class Node:
    # offsets from start of node
    NODE_ID_OFFSET = 0
    IN_USE_FLAG_OFFSET = 3
    REL_ID_OFFSET = 4
    PROPERTY_ID_OFFSET = 8
    LABEL_ID_OFFSET = 12
    FLAGS_OFFSET = 15

    nodeIDByteLen = 3

    storageSize = 16
    numNodes = 0

    def __init__(self, nodeFile, nodeID=None):
        Node.numNodes = nodeFile.getNumNodes()
        print("**** Num Nodes = {0} *****".format(Node.numNodes))

        if nodeID is None:
            nodeID = Node.numNodes

		# relationships is the list of relationships this node is in
        self.relationships = []
        # key-value pairs or properties stored within node
        # e.g. name: Jane
        self.properties = []
        # labels indicate the type of a node, a node can have multiple labels
        # e.g. person, bank account, id
        self.labels = []

        self.nodeID = nodeID

        # if creating a new node
        if self.nodeID >= Node.numNodes:
        # increment number of nodes
            Node.numNodes += 1

        self.nodeFile = nodeFile

        # open node file
        storeFileName = self.nodeFile.getFileName()
        storeFile = open(storeFileName, 'r+b')

        # write number of nodes to first 3 bytes of node file
        storeFile.write((self.numNodes).to_bytes(Node.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        self.startOffset = self.nodeID * Node.storageSize + Node.nodeIDByteLen

    # This method adds a node with a relationship to this node's adj list
    def addRelationship(self, rel):
        self.relationships.append(rel)

    # This method adds data to a node
    def addProperty(self, prop):
        self.properties.append(prop)

    # This method adds labels to a node
    def addLabel(self, nodeLabel):
        if len(self.labels) > 0:
            self.labels[len(self.labels) - 1].nextLabelID = nodeLabel.labelID
        self.labels.append(nodeLabel)

    # This method removes a relationship from a node and writes the node
    def removeRelationship(self, relID):
        toRemove = 0
        for index in range(0, len(self.relationships)):
            rel = self.relationships[index]
            if rel.getID() == relID:
                toRemove = relID

        self.relationships.pop(toRemove)

        self.writeNode()

    # This method removes a property from a node and writes the node
    def removeProperty(self, propID):
        for index in range(0, len(self.properties)):
            prop = self.properties[index]
            if prop.getID() == propID:
                self.properties.pop(propID)

        self.writeNode()

    # This method removes a label from a node and writes the node
    def removeLabel(self, labelID):
        for index in range(0, len(self.labels)):
            label = self.labels[index]
            if label.getID() == labelID:
                self.labels.pop(index)

        self.writeNode()

    def getID(self):
        return self.nodeID

    def getRelationships(self):
        return self.relationships

    def getData(self):
        return self.data

    def getLabels(self):
        return self.labels

    def getProperties(self):
        return self.properties

    # This method writes this node to the given node file
    def writeNode(self):
        print("properties in node")
        for prop in self.properties:
            print(prop.getID())

        print("writing node...")

        # open node file
        storeFileName = self.nodeFile.getFileName()
        storeFile = open(storeFileName, 'r+b')

        print("opened store file: {0}". format(storeFileName))

        # write node id
        storeFile.seek(self.startOffset + Node.NODE_ID_OFFSET)
        storeFile.write((self.nodeID).to_bytes(Node.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        print("wrote node ID: {0}". format(self.nodeID))

        # write in-use flag
        storeFile.seek(self.startOffset + Node.IN_USE_FLAG_OFFSET)
        storeFile.write((1).to_bytes(1, byteorder = sys.byteorder, signed=True))

        print("wrote in-use flag: {0}". format(1))

        # write first relationship ID
        storeFile.seek(self.startOffset + Node.REL_ID_OFFSET)
        if len(self.relationships) == 0:
            firstRel = -1
            storeFile.write((-1).to_bytes(Relationship.relIDByteSize,
                byteorder = sys.byteorder, signed=True))
            print("wrote first rel ID: -1")
        else:
            firstRel = self.relationships[0]
            storeFile.write(firstRel.getID().to_bytes(Relationship.relIDByteSize,
                byteorder = sys.byteorder, signed=True))

            print("wrote first rel ID: {0}". format(firstRel.getID()))

        # write first property ID
        storeFile.seek(self.startOffset + Node.PROPERTY_ID_OFFSET)
        if len(self.properties) == 0:
            firstProp = -1
            storeFile.write((-1).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            print("wrote first property ID: -1")

        else:
            firstProp = self.properties[0]
            storeFile.write(firstProp.getID().to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))

            print("wrote first property ID: {0}". format(firstProp.getID()))

        # write first label ID
        storeFile.seek(self.startOffset + Node.LABEL_ID_OFFSET)
        if len(self.labels) == 0:
            storeFile.write((-1).to_bytes(Label.LABEL_OFFSET,
                byteorder = sys.byteorder, signed=True))
        else:
            firstLabel = self.labels[0]
            storeFile.write(firstLabel.getLabelID().to_bytes(Label.LABEL_OFFSET,
                byteorder = sys.byteorder, signed=True))

        print("writing relationships to relationship file ...")

        # write relationships to relationship file
        for relIndex in range(0, len(self.relationships)):
            print("writing {0} relationship ".format(relIndex))
            rel = self.relationships[relIndex]

            # first relationship
            if relIndex == 0:
                nullRelationship = Relationship(-1, -1, "", "",-1)
                # no next relationship
                if relIndex == len(self.relationships) - 1:
                    print("only one relationship")
                    rel.writeRelationship(self, nullRelationship, nullRelationship)
                else:
                    nullRelationship = Relationship(-1, -1, "", "", -1)
                    rel.writeRelationship(self, nullRelationship, self.relationships[relIndex + 1])
            elif relIndex == len(self.relationships) - 1:
                nullRelationship = Relationship(-1, -1, "", "", -1)
                rel.writeRelationship(self, self.relationships[relIndex - 1], nullRelationship)
            else:
                rel.writeRelationship(self, self.relationships[relIndex - 1],
                    self.relationships[relIndex + 1])

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


        # write labels
        for labelIndex in range(0, len(self.labels)):
            label = self.labels[labelIndex]
            print("writing {0} label ".format(label.getLabelID()))

            # no next label
            if labelIndex == len(self.labels) - 1:
                print("no next label")
                nextLabelID = -1

            else:
                nextLabelID = (self.labels[labelIndex + 1]).getLabelID()

            label.writeLabel(nextLabelID)


















