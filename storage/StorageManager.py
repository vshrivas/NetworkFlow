from .Label import Label
from .LabelFile import LabelFile
from .Node import Node
from .NodeFile import NodeFile
from .Property import Property
from .PropertyFile import PropertyFile
from .Relationship import Relationship
from .RelationshipFile import RelationshipFile

import pickle, os

# Uses the file manager to find files 

# storage manager should have a file to store metadatalike number of files
# of each type
class StorageManager(object):

    '''def __init__():'''
    '''#folder_prefix = "datastore/"
    def __init__(self, nodeFile, relationshipFile, propertyFile, labelFile):
        self.nodeFile = nodeFile
        self.relationshipFile = relationshipFile
        self.propertyFile = propertyFile
        self.labelFile = labelFile

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
        storeFilePath = self.nodeFile.getFilePath()
        storeFile = open(storeFilePath, 'r+b')

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
            label.writeLabel(nextLabelID)'''



























