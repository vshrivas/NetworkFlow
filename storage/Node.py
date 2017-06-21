from .Relationship import Relationship
from .Property import Property
from .Label import Label
from .LabelIndex import LabelIndex
import sys

DEBUG = False

class Node:

    """Node class: representation of a Node, which has labels, properties 
    (key-value pairs), and relationships to other Nodes.
    
    The Node is the basic element for storing data in a graph database and 
    is somewhat similar to a row in a table in relational databases. Nodes 
    serve as the vertices of the graph representation of a graph database.
    Nodes have labels identifying their type, properties that specify info 
    about a node, and relationships to other nodes that indicate how various 
    nodes are related. 

    Storage: Nodes are stored as fixed size records which are 16 bytes in
    length. This fixed size storage format makes looking up specific nodes 
    in the database faster as to look up a node, only the node ID is needed. Also, 
    since every relationship, property, and label stores the ID of the next 
    relationship, property, or label for a given node (nodes in the case of a relationship), 
    the node only needs to store the IDs of the first relationship, property, and label.

    Bytes 1-3: Node ID
    Byte 4: In-use flag (1 for in-use, 0 for not)
    Bytes 5-8: ID of first relationship connected to node
    Bytes 9-12: ID of first property (key-value pair) for node
    Bytes 13-15: ID of first label for node
    Byte 16: Flags
    """

    # byte offsets from start of node
    NODE_ID_OFFSET = 0
    IN_USE_FLAG_OFFSET = 3
    REL_ID_OFFSET = 4
    PROPERTY_ID_OFFSET = 8
    LABEL_ID_OFFSET = 12
    FLAGS_OFFSET = 15

    nodeIDByteLen = 3

    storageSize = 16
    # number of nodes ever created (used for auto-incrementing the node ID)
    numNodes = 0

    def __init__(self, nodeFile, nodeID=None):
        """Constructor for Node, which sets the node ID and the file the node is stored in.

        Arguments:
        nodeFile: the NodeFile object that represents the file storing Nodes 
        nodeID: the ID of the Node to be initialized; default nodeID of None 
        means the Node will be assigned an auto-incrementing node ID
        """
        Node.numNodes = nodeFile.getNumNodes()
        if DEBUG:
            print("**** Num Nodes = {0} *****".format(Node.numNodes))

        # if nodeID is None, use auto-incrementing for nodeID
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

        # Assign nodeID
        self.nodeID = nodeID

        # if creating a new node
        if self.nodeID >= Node.numNodes:
            # increment number of nodes
            Node.numNodes += 1

        # set nodeFile for node
        self.nodeFile = nodeFile

        # open node file
        storeFileName = self.nodeFile.getFileName()
        storeFile = open(storeFileName, 'r+b')

        # write number of nodes to first 3 bytes of node file
        storeFile.write((self.numNodes).to_bytes(Node.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        # set starting offset of node in NodeFile
        self.startOffset = self.nodeID * Node.storageSize + Node.nodeIDByteLen

    
    def addRelationship(self, rel):
        """Adds a relationship to this node's relationship list."""
        self.relationships.append(rel)

    def addProperty(self, prop):
        """Add a property, which stores a key-value pair, to this node."""
        self.properties.append(prop)

    def addLabel(self, nodeLabel):
        """Add a label to this node and add node to appropriate labelIndex (index 
        that stores node IDs by label)."""
        # set nextLabelID of last label to current label's labelID.
        if len(self.labels) > 0:
            self.labels[len(self.labels) - 1].nextLabelID = nodeLabel.labelID
        # add label to labelID
        self.labels.append(nodeLabel)

        # if this is a new node
        # add nodeID to label index
        # open label index
        if self.nodeID == Node.numNodes - 1:
            labelIndex = LabelIndex(nodeLabel.getLabelStr())
            # add node to index
            labelIndex.addNode(self.nodeID)
        

    def removeRelationship(self, relID):
        """Remove a relationship from this node and write the node"""
        toRemove = 0
        # Find relationship with matching relID to remove
        for index in range(0, len(self.relationships)):
            rel = self.relationships[index]
            if rel.getID() == relID:
                toRemove = relID

        # Remove relationship from relationship list
        self.relationships.pop(toRemove)

        # Write node
        self.writeNode()

    def removeProperty(self, propID):
        """Remove a property from this node and write the node."""
        # Find property with matching propID to remove
        for index in range(0, len(self.properties)):
            prop = self.properties[index]
            # Remove property with matching propID
            if prop.getID() == propID:
                self.properties.pop(propID)

        # Write node
        self.writeNode()

    def removeLabel(self, labelID):
        """Remove a label from this node and write the node."""
        # Find label with matching labelID to remove
        for index in range(0, len(self.labels)):
            label = self.labels[index]
            # Remove label with matching labelID
            if label.getID() == labelID:
                self.labels.pop(index)

        # Write node
        self.writeNode()

    def getID(self):
        """Return nodeID of this node"""
        return self.nodeID

    def getRelationships(self):
        """Return relationships list of this node"""
        return self.relationships

    def getLabels(self):
        """Return labels list of this node"""
        return self.labels

    def getLabelStrs(self):
        """Return strings associated with labels for every label of this node"""
        labelStrs = []
        for label in self.labels:
            labelStrs.append(label.getLabelStr().strip())
        return labelStrs

    def getProperties(self):
        """Return properties list of this node"""
        return self.properties

    def writeNode(self):
        """Writes this node to the node's node file according to the storage 
        format given in the class description and writes this node's relationships, 
        properties, and labels to the node's relationship file, property file, and 
        label file, respectively.
        """
        if DEBUG:
            print("properties in node")
            for prop in self.properties:
                print(prop.getID())

            print("labels in node:")
            for label in self.labels:
                print(label.getLabelID())

            print("writing node...")

        # open node file
        storeFileName = self.nodeFile.getFileName()
        storeFile = open(storeFileName, 'r+b')

        if DEBUG:
            print("opened store file: {0}". format(storeFileName))

        # write node id
        storeFile.seek(self.startOffset + Node.NODE_ID_OFFSET)
        storeFile.write((self.nodeID).to_bytes(Node.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        if DEBUG:
            print("wrote node ID: {0}". format(self.nodeID))

        # write in-use flag
        storeFile.seek(self.startOffset + Node.IN_USE_FLAG_OFFSET)
        storeFile.write((1).to_bytes(1, byteorder = sys.byteorder, signed=True))

        if DEBUG:
            print("wrote in-use flag: {0}". format(1))

        # write first relationship ID
        storeFile.seek(self.startOffset + Node.REL_ID_OFFSET)
        # if there are no relationships, write -1 as first relationship ID
        if len(self.relationships) == 0:
            firstRel = -1
            storeFile.write((-1).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first rel ID: -1")
        # otherwise, write first relationship ID
        else:
            firstRel = self.relationships[0]
            storeFile.write(firstRel.getID().to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first rel ID: {0}". format(firstRel.getID()))

        # write first property ID
        storeFile.seek(self.startOffset + Node.PROPERTY_ID_OFFSET)
        # if there are no properties, write -1 as first property ID
        if len(self.properties) == 0:
            firstProp = -1
            storeFile.write((-1).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first property ID: -1")
        # otherwise, write first property ID
        else:
            firstProp = self.properties[0]
            storeFile.write(firstProp.getID().to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first property ID: {0}". format(firstProp.getID()))

        # write first label ID
        storeFile.seek(self.startOffset + Node.LABEL_ID_OFFSET)
        # if there are no labels, write -1 as first label ID
        if len(self.labels) == 0:
            storeFile.write((-1).to_bytes(Label.LABEL_OFFSET,
                byteorder = sys.byteorder, signed=True))
        # otherwise, write first label ID
        else:
            firstLabel = self.labels[0]
            storeFile.write(firstLabel.getLabelID().to_bytes(Label.LABEL_OFFSET,
                byteorder = sys.byteorder, signed=True))

        if DEBUG:
            print("writing relationships to relationship file ...")

        # write relationships to relationship file
        for relIndex in range(0, len(self.relationships)):
            if DEBUG:
                print("writing {0} relationship ".format(relIndex))
            rel = self.relationships[relIndex]

            # write first relationship
            if relIndex == 0:
                # A placeholder relationship in case there is no previous or next relationship
                nullRelationship = Relationship(-1, -1, "", "",-1)
                # no next relationship
                if relIndex == len(self.relationships) - 1:
                    if DEBUG:
                        print("only one relationship")
                    rel.writeRelationship(self, nullRelationship, nullRelationship)
                # there is a next relationship
                else:
                    nullRelationship = Relationship(-1, -1, "", "", -1)
                    rel.writeRelationship(self, nullRelationship, self.relationships[relIndex + 1])
            # write last relationship
            elif relIndex == len(self.relationships) - 1:
                # A placeholder relationship in case there is no previous or next relationship
                nullRelationship = Relationship(-1, -1, "", "", -1)
                rel.writeRelationship(self, self.relationships[relIndex - 1], nullRelationship)
            # write relationship that's not first or last relationship
            else:
                rel.writeRelationship(self, self.relationships[relIndex - 1],
                    self.relationships[relIndex + 1])
        if DEBUG:
            print("writing properties to property file ...")

        # write properties to property file
        for propIndex in range(0, len(self.properties)):
            prop = self.properties[propIndex]
            if DEBUG:
                print("writing {0} property ".format(prop.getID()))

            # write last property
            if propIndex == len(self.properties) - 1:
                if DEBUG:
                    print("no next property")
                # A placeholder property since there is no next property
                nullProperty = Property("", "", "", -1)
                prop.writeProperty(nullProperty)
            # write property that's not last property
            else:
                prop.writeProperty(self.properties[propIndex + 1])

        # write labels to label file
        for labelIndex in range(0, len(self.labels)):
            label = self.labels[labelIndex]
            if DEBUG:
                print("writing {0} label ".format(label.getLabelID()))

            # case of last label
            if labelIndex == len(self.labels) - 1:
                if DEBUG:
                    print("no next label")
                # set next label's id to -1
                nextLabelID = -1
            # case of any other label
            else:
                nextLabelID = (self.labels[labelIndex + 1]).getLabelID()
            # write label
            label.writeLabel(nextLabelID)


















