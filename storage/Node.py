from Relationship import Relationship
from Property import Property
from Label import Label
from LabelIndex import LabelIndex
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

    # node ID is a list of 2 elements 
    # nodeID[0] = pageID
    # nodeID[1] = nodeIndex
    def __init__(self, nodeFile, nodePage, nodeID):
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
        #if nodeID is None:
            #nodeID = Node.numNodes

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

        # set nodeFile for node
        self.nodeFile = nodeFile

        self.firstRelID = [[1,0], -1]
        self.firstPropID = [[2,0], -1]
        self.firstLabelID = [[3,0], -1]

        # open node file
        storeFilePath = self.nodeFile.getFilePath()
        storeFile = open(storeFilePath, 'r+b')

        # write number of nodes to first 3 bytes of node file
        storeFile.write((self.numNodes).to_bytes(Node.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        # set starting offset of node in NodeFile
        nodeIndex = self.nodeID[1]
        #self.startOffset = nodeIndex * Node.storageSize + Node.nodeIDByteLen

    
    def addRelationship(self, rel):
        prevRel = None
        prevRelID = [[1, 0], -1]

        # node had relationships before
        if (len(self.relationships) > 0):
             # find last relationship
             prevRel = self.relationships[len(self.relationships) - 1]
             prevRelID = prevRel.getID()

             # set previous relationship's next relID 
             # the node is the first node in the relationship
             if node.getID()[1] == prevRel.firstNodeID[1]:
                prevRel.node1NextRelID = rel.getID()

             # node is the second node in the relationship
             else:
                prevRel.node2NextRelID = rel.getID()
        else:
            firstRelID = rel.getID()

        # set this relationship's prev relID
        if node.getID()[1] == rel.firstNodeID[1]:
            rel.node1PrevRelID = prevRelID

        else:
            rel.node2PrevRelID = prevRelID

        rel.node1NextRelID = prevRelID
        rel.node2NextRelID = prevRelID

        """Adds a relationship to this node's relationship list."""
        self.relationships.append(rel)


    def addRelationships(self, rels):
        for rel in rels:
            addRelationship(rel)

    def addProperty(self, prop):
        if len(self.properties) > 0:
            self.properties[len(self.properties) - 1].nextPropertyID = prop.getID()
        else:
            firstPropID = prop.getID()

        prop.nextPropertyID = [[2, 0], -1]
        """Add a property, which stores a key-value pair, to this node."""
        self.properties.append(prop)

    def addProperties(self, props):
        for props in props:
            addProperty(prop)

    def addLabel(self, nodeLabel):
        """Add a label to this node and add node to appropriate labelIndex (index 
        that stores node IDs by label)."""
        # set nextLabelID of last label to current label's labelID.
        if len(self.labels) > 0:
            self.labels[len(self.labels) - 1].nextLabelID = nodeLabel.labelID
        else:
            firstLabelID = nodeLabel.getID()

        nodeLabel.nextLabelID = [[3,0], -1]

        # add label to labelID
        self.labels.append(nodeLabel)

        # add nodeID to label index if node is not already in label index
        # open label index
        labelIndex = LabelIndex(nodeLabel.getLabelStr())
        # add node to index
        if self.nodeID not in labelIndex.getItems():
            labelIndex.addNode(self.nodeID)

    def addLabels(self, lbls):
        for lbl in lbls:
            addLabel(self, lbl)
        
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

