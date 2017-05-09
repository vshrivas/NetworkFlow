from Label import Label
from LabelFile import LabelFile
from Node import Node
from NodeFile import NodeFile
from Property import Property
from PropertyFile import PropertyFile
from Relationship import Relationship
from RelationshipFile import RelationshipFile

import pickle

# Storage manager that manages where nodes, relationships, properties, and labels
# are allocated in their respective files.
class StorageManager:

    def __init__(self, nodeFile, relationshipFile, propertyFile, labelFile):
        self.nodeFile = nodeFile
        self.relationshipFile = relationshipFile
        self.propertyFile = propertyFile
        self.labelFile = labelFile

        # ?????????????????????????????????????????
        # StorageManager.numFiles += 1
        # self.fileID = StorageManager.numFiles
        # ?????????????????????????????????????????

        # create storage files to keep track of free space
        # all lists of free spaces start with space at ID 0 being free
        # list of locations in node file with free space for nodes (specified by nodeIDs)
        # try to load lists from disk, if no lists currently exist, create new ones
        self.nodeFreeSpaceFileName = "NodeFreeSpaceFile.store"
        try:
            nodeSpaceFile = open(self.nodeFreeSpaceFileName, 'rb')
            self.node_free_space = pickle.load(nodeSpaceFile)

        except FileNotFoundError:
            nodeSpaceFile = open(self.nodeFreeSpaceFileName, 'wb')
            self.node_free_space = [0]
            pickle.dump(self.node_free_space, nodeSpaceFile)
            

        self.relFreeSpaceFileName = "RelationshipFreeSpaceFile.store"
        try:
            relSpaceFile = open(self.relFreeSpaceFileName, 'rb')
            self.rel_free_space = pickle.load(relSpaceFile)

        except FileNotFoundError:
            relSpaceFile = open(self.relFreeSpaceFileName, 'wb')
            self.rel_free_space = [0]
            pickle.dump(self.rel_free_space, relSpaceFile)


        self.propFreeSpaceFileName = "PropFreeSpaceFile.store"
        try:
            propSpaceFile = open(self.propFreeSpaceFileName, 'rb')
            self.prop_free_space = pickle.load(propSpaceFile)

        except FileNotFoundError:
            propSpaceFile = open(self.propFreeSpaceFileName, 'wb')
            self.prop_free_space = [0]
            pickle.dump(self.prop_free_space, propSpaceFile)
            

        self.labelFreeSpaceFileName = "LabelFreeSpaceFile.store"
        try:
            labelSpaceFile = open(self.labelFreeSpaceFileName, 'rb')
            self.label_free_space = pickle.load(labelSpaceFile)

        except FileNotFoundError:
            labelSpaceFile = open(self.labelFreeSpaceFileName, 'wb')
            self.label_free_space = [0]
            pickle.dump(self.label_free_space, labelSpaceFile)

    # opening files in write mode so that previous lists are cleared before new ones are written
    def openNodeSpaceFile():
        nodeSpaceFile = open(self.nodeFreeSpaceFile, 'wb')
        return nodeSpaceFile

    def openRelSpaceFile():
        relSpaceFile = open(self.relFreeSpaceFile, 'wb')
        return relSpaceFile

    def openPropSpaceFile():
        propSpaceFile = open(self.propFreeSpaceFile, 'wb')
        return propSpaceFile

    def openLabelSpaceFile():
        labelSpaceFile = open(self.labelFreeSpaceFile, 'wb')
        return labelSpaceFile

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

            # write changes to list
            nodeSpaceFile = openNodeSpaceFile()
            pickle.dump(self.node_free_space, nodeSpaceFile)
            nodeSpaceFile.close()

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

            # write changes to list
            relSpaceFile = openRelSpaceFile()
            pickle.dump(self.rel_free_space, relSpaceFile)
            relSpaceFile.close()

            return relationship

        relationship = Relationship(relationshipFile, node1.getID(), node2.getID())
        return relationship

    # Finds free space for property (potentially location to the right of all properties if
    # there is no free space), creates a property, and writes the property to the property file.
    # It returns the created property.
    def createProperty(self, key, value):
        # there is free space
        if len(self.prop_free_space) > 0:
            freePropID = self.prop_free_space[len(self.prop_free_space) - 1]
            prop = Property(key, value, propertyFile, freePropID)

            # remove block from list of property free space
            self.prop_free_space.pop()

            # write changes to list
            propSpaceFile = openPropSpaceFile()
            pickle.dump(self.prop_free_space, propSpaceFile)
            propSpaceFile.close()

            return prop

        prop = Property(key, value, propertyFile)
        return prop

    # Finds free space for label (potentially location to the right of all label if
    # there is no free space), creates a label, and writes the label to the label file.
    # It returns the created label.
    def createLabel(self, labelStr):
        # there is free space
        if len(self.label_free_space) > 0:
            freeLabelID = self.label_free_space[len(self.label_free_space) - 1]
            label = Label(labelStr, labelFile, freeLabelID)

            # remove block from list of property free space
            self.label_free_space.pop()

            # write changes to list
            labelSpaceFile = openLabelSpaceFile()
            pickle.dump(self.label_free_space, labelSpaceFile)
            labelSpaceFile.close()

            return label

        label = Label(labelStr, labelFile)
        return label

    # delete node by recording its ID in list of free space
    # also delete all corresponding relationships, properties, and labels
    def deleteNode(self, nodeID):
        node = self.nodeFile.readNode(nodeID, self.relationshipFile, self.propertyFile, self.labelFile)

        # delete associated relationships, properties, and labels

        # remove relationships from sibling node
        for rel in node.relationships:
            otherNodeID = rel.getOtherNodeID()
            otherNode = self.nodeFile.readNode(otherNodeID, self.relationshipFile, self.propertyFile, self.labelFile)
            otherNode.removeRelationship(rel.getID())

            self.rel_free_space.append(rel.getID())

        # write changes to list
        relSpaceFile = openRelSpaceFile()
        pickle.dump(self.rel_free_space, relSpaceFile)
        relSpaceFile.close()

        for prop in node.properties:
            self.prop_free_space.append(prop.getID())

        # write changes to list
        propSpaceFile = openPropSpaceFile()
        pickle.dump(self.prop_free_space, propSpaceFile)
        propSpaceFile.close()

        for label in node.labels:
            self.label_free_space.append(label.getID())

        # write changes to list
        labelSpaceFile = openLabelSpaceFile()
        pickle.dump(self.label_free_space, labelSpaceFile)
        labelSpaceFile.close()

        # add node id to node free space list
        self.node_free_space.append(nodeID)










