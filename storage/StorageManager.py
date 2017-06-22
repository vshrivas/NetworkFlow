from .Label import Label
from .LabelFile import LabelFile
from .Node import Node
from .NodeFile import NodeFile
from .Property import Property
from .PropertyFile import PropertyFile
from .Relationship import Relationship
from .RelationshipFile import RelationshipFile

import pickle, os

# Storage manager that manages where nodes, relationships, properties, and labels
# are allocated in their respective files.
class StorageManager:

    #folder_prefix = "datastore/"
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
        self.dir = "datafiles"

        self.nodeFreeSpaceFileName = "NodeFreeSpaceFile.store"
        self.nodeFilePath = os.path.join(self.dir, self.nodeFreeSpaceFileName)

        if os.path.exists(self.nodeFilePath):
            nodeSpaceFile = open(self.nodeFilePath, 'rb')
            self.node_free_space = pickle.load(nodeSpaceFile)
        else:
            nodeSpaceFile = open(self.nodeFilePath, 'wb')
            self.node_free_space = [0]
            pickle.dump(self.node_free_space, nodeSpaceFile)
            

        self.relFreeSpaceFileName = "RelationshipFreeSpaceFile.store"
        self.relFilePath = os.path.join(self.dir, self.relFreeSpaceFileName)

        if os.path.exists(self.relFilePath):
            relSpaceFile = open(self.relFilePath, 'rb')
            self.rel_free_space = pickle.load(relSpaceFile)

        else:
            relSpaceFile = open(self.relFilePath, 'wb')
            self.rel_free_space = [0]
            pickle.dump(self.rel_free_space, relSpaceFile)


        self.propFreeSpaceFileName = "PropFreeSpaceFile.store"
        self.propFilePath = os.path.join(self.dir, self.propFreeSpaceFileName)

        if os.path.exists(self.propFilePath):
            propSpaceFile = open(self.propFilePath, 'rb')
            self.prop_free_space = pickle.load(propSpaceFile)

        else:
            propSpaceFile = open(self.propFilePath, 'wb')
            self.prop_free_space = [0]
            pickle.dump(self.prop_free_space, propSpaceFile)


        self.labelFreeSpaceFileName = "LabelFreeSpaceFile.store"
        self.labelFilePath = os.path.join(self.dir, self.labelFreeSpaceFileName)

        if os.path.exists(self.labelFilePath):
            labelSpaceFile = open(self.labelFilePath, 'rb')
            self.label_free_space = pickle.load(labelSpaceFile)

        else:
            labelSpaceFile = open(self.labelFilePath, 'wb')
            self.label_free_space = [0]
            pickle.dump(self.label_free_space, labelSpaceFile)


    # Finds free space for node (potentially location to the right of all nodes if
    # there is no free space), creates a node, and writes the node to the node file.
    # It returns the created node.
    def createNode(self):
        # there is free space
        if len(self.node_free_space) > 0:
            freeNodeID = self.node_free_space[len(self.node_free_space) - 1]
            node = Node(self.nodeFile, freeNodeID)
            node.writeNode()

            # remove block from list of node free space
            self.node_free_space.pop()

            # write changes to list
            nodeSpaceFile = open(self.nodeFilePath, 'wb')

            pickle.dump(self.node_free_space, nodeSpaceFile)
            nodeSpaceFile.close()

            return node

        # no free space, write node to right of all current nodes
        node = Node(self.nodeFile)
        node.writeNode()
        return node

    # Finds free space for relationship (potentially location to the right of all relationships if
    # there is no free space), creates a relationship, and writes the relationship to the relationship file.
    # It returns the created relationship.
    def createRelationship(self, node1, node2, relType):
        # there is free space
        if len(self.rel_free_space) > 0:
            freeRelID = self.rel_free_space[len(self.rel_free_space) - 1]
            relationship = Relationship(node1.getID(), node2.getID(), relType, self.relationshipFile, freeRelID)

            # remove block from list of relationship free space
            self.rel_free_space.pop()

            # write changes to list
            relSpaceFile = open(self.relFilePath, 'wb')
            pickle.dump(self.rel_free_space, relSpaceFile)
            relSpaceFile.close()

            return relationship

        relationship = Relationship(node1.getID(), node2.getID(), relType, self.relationshipFile)
        return relationship

    # Finds free space for property (potentially location to the right of all properties if
    # there is no free space), creates a property, and writes the property to the property file.
    # It returns the created property.
    def createProperty(self, key, value):
        # there is free space
        if len(self.prop_free_space) > 0:
            freePropID = self.prop_free_space[len(self.prop_free_space) - 1]
            prop = Property(key, value, self.propertyFile, freePropID)

            # remove block from list of property free space
            self.prop_free_space.pop()

            # write changes to list
            propSpaceFile = open(self.propFilePath, 'wb')
            pickle.dump(self.prop_free_space, propSpaceFile)
            propSpaceFile.close()

            return prop

        prop = Property(key, value, self.propertyFile)
        return prop

    # Finds free space for label (potentially location to the right of all label if
    # there is no free space), creates a label, and writes the label to the label file.
    # It returns the created label.
    def createLabel(self, labelStr):
        # there is free space
        if len(self.label_free_space) > 0:
            freeLabelID = self.label_free_space[len(self.label_free_space) - 1]
            label = Label(labelStr, self.labelFile, freeLabelID)

            # remove block from list of property free space
            self.label_free_space.pop()

            # write changes to list
            labelSpaceFile = open(self.labelFilePath, 'wb')
            pickle.dump(self.label_free_space, labelSpaceFile)
            labelSpaceFile.close()

            return label

        label = Label(labelStr, self.labelFile)
        return label

    # delete node by recording its ID in list of free space
    # also delete all corresponding relationships, properties, and labels
    def deleteNode(self, nodeID):
        node = self.nodeFile.readNode(nodeID, self.relationshipFile, self.propertyFile, self.labelFile)
        print("***properties in node 0***")
        for prop in node.properties:
            print(prop.getID())

        # delete associated relationships, properties, and labels

        # remove relationships from sibling node
        for rel in node.relationships:
            otherNodeID = rel.getOtherNodeID(nodeID)
            otherNode = self.nodeFile.readNode(otherNodeID, self.relationshipFile, self.propertyFile, self.labelFile)
            print("***properties in node 1***")
            for prop in otherNode.properties:
                print(prop.getID())
            otherNode.removeRelationship(rel.getID())

            self.rel_free_space.append(rel.getID())

        # write changes to list
        relSpaceFile = open(self.relFilePath, 'wb')
        pickle.dump(self.rel_free_space, relSpaceFile)
        relSpaceFile.close()

        for prop in node.properties:
            self.prop_free_space.append(prop.getID())

        # write changes to list
        propSpaceFile = open(self.propFilePath, 'wb')
        pickle.dump(self.prop_free_space, propSpaceFile)
        propSpaceFile.close()

        for label in node.labels:
            self.label_free_space.append(label.getLabelID())

        # write changes to list
        labelSpaceFile = open(self.labelFilePath, 'wb')
        pickle.dump(self.label_free_space, labelSpaceFile)
        labelSpaceFile.close()

        # add node id to node free space list
        self.node_free_space.append(nodeID)

    '''# opening files in write mode so that previous lists are cleared before new ones are written
    def openNodeSpaceFile(self):
        nodeSpaceFile = open(self.nodeFreeSpaceFileName, 'wb')
        return nodeSpaceFile

    def openRelSpaceFile(self):
        relSpaceFile = open(self.relFreeSpaceFileName, 'wb')
        return relSpaceFile

    def openPropSpaceFile(self):
        propSpaceFile = open(self.propFreeSpaceFileName, 'wb')
        return propSpaceFile

    def openLabelSpaceFile(self):
        labelSpaceFile = open(self.labelFreeSpaceFileName, 'wb')
        return labelSpaceFile'''










