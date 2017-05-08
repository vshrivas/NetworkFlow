from Label import Label
from LabelFile import LabelFile
from Node import Node
from NodeFile import NodeFile
from Property import Property
from PropertyFile import PropertyFile
from Relationship import Relationship
from RelationshipFile import RelationshipFile

# Storage manager that manages where nodes, relationships, properties, and labels
# are allocated in their respective files.
class StorageManager:

    def __init__(self, nodeFile, relationshipFile, propertyFile, labelFile):
        self.nodeFile = nodeFile
        self.relationshipFile = relationshipFile
        self.propertyFile = propertyFile
        self.labelFile = labelFile

        # all lists of free spaces start with space at ID 0 being free
        # list of locations in node file with free space for nodes (specified by nodeIDs)
        self.node_free_space = [0]

        # list of locations in relationship file with free space for relationships (specified by relationshipIDs)
        self.rel_free_space = [0]

        # list of locations in property file with free space for property (specified by propertyIDs)
        self.prop_free_space = [0]

        # list of locations in label file with free space for labels (specified by labelIDs)
        self.label_free_space = [0]
    
    # Finds free space for node (potentially location to the right of all nodes if 
    # there is no free space), creates a node, and writes the node to the node file.
    # It returns the created node.
    def createNode(self):
        # there is free space
        if len(self.node_free_space) > 0:
            freeNodeID = self.node_free_space[len(self.node_free_space) - 1]
            node = Node(nodeFile, freeNodeID)
            node.writeNode()
            # remove block from list of node free space
            self.node_free_space.pop()
            return node

        # no free space, write node to right of all current nodes
        node = Node(nodeFile)
        node.writeNode()
        return node

    # Finds free space for relationship (potentially location to the right of all relationships if 
    # there is no free space), creates a relationship, and writes the relationship to the relationship file.
    # It returns the created relationship.
    def createRelationship(self, node1, node2):
        # there is free space
        if len(self.relationship_free_space) > 0:
            freeRelID = self.rel_free_space[len(self.rel_free_space) - 1]
            relationship = Relationship(relationshipFile, node1.getID(), node2.getID(), freeRelID)

            # remove block from list of relationship free space
            self.rel_free_space.pop()
            return relationship

        relationship = Relationship(relationshipFile, node1.getID(), node2.getID())
        return relationship

    # Finds free space for property (potentially location to the right of all properties if 
    # there is no free space), creates a property, and writes the property to the property file.
    # It returns the created property.
    def createProperty(self, key, value):
        # there is free space
        if len(self.prop_free_space) > ):
            freePropID = self.prop_free_space[len(self.prop_free_space) - 1]
            prop = Property(key, value, propertyFile, freePropID)

            # remove block from list of property free space
            self.prop_free_space.pop()
            return prop

        prop = Property(key, value, propertyFile)
        return prop

    # Finds free space for label (potentially location to the right of all label if 
    # there is no free space), creates a label, and writes the label to the label file.
    # It returns the created label.
    def createLabel(self, labelStr):
        # there is free space
        if len(self.label_free_space) > ):
            freeLabelID = self.label_free_space[len(self.label_free_space) - 1]
            label = Label(labelStr, labelFile, freeLabelID)

            # remove block from list of property free space
            self.label_free_space.pop()
            return label

        label = Label(labelStr, labelFile)
        return label

    # delete node by recording its ID in list of free space
    # also delete all corresponding relationships, properties, and labels
    def deleteNode(self, nodeID):
        node = self.nodeFile.readNode(nodeID, self.relationshipFile, self.propertyFile, self.labelFile)

        # delete associated relationships, properties, and labels
        
        # remove relationships from sibling node
        for (rel in node.relationships):
            otherNodeID = rel.getOtherNodeID()
            otherNode = self.nodeFile.readNode(otherNodeID, self.relationshipFile, self.propertyFile, self.labelFile)
            otherNode.removeRelationship(rel.getID())

            self.rel_free_space.append(rel.getID())

        for (prop in node.properties):
            self.prop_free_space.append(prop.getID())

        for (label in node.labels):
            self.label_free_space.append(label.getID())

        # add node id to node free space list
        self.node_free_space.append(nodeID)







        
    
    
