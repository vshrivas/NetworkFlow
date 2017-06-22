from storage.Node import Node
from storage.NodeFile import NodeFile

from storage.Property import Property
from storage.PropertyFile import PropertyFile

from storage.Label import Label
from storage.LabelFile import LabelFile

from storage.Relationship import Relationship
from storage.RelationshipFile import RelationshipFile


def testCase():
    nodeFile = NodeFile()
    relationshipFile = RelationshipFile()
    propertyFile = PropertyFile()
    labelFile = LabelFile()

    # create node, create property
    node1 = Node(nodeFile)
    property1 = Property('Name', 'John', propertyFile)

    node1.addProperty(property1)
    node1.addLabel(Label("blab", labelFile))

    node2 = Node(nodeFile)
    property2 = Property('Name', 'Pupp', propertyFile)

    node2.addProperty(property2)

    relationship1 = Relationship(node1.getID(), node2.getID(), relationshipFile)
    node1.addRelationship(relationship1)
    #node2.addRelationship(relationship1)

    node1.writeNode()
    #node2.writeNode()

    # node 3 should be the same as node 1
    node3 = nodeFile.readNode(0, relationshipFile, propertyFile, labelFile)

    rels = node3.getRelationships()
    labels = node3.getLabels()
    properties = node3.getProperties()

    print(rels[0].firstNodeID)
    print(rels[0].secondNodeID)
    print(rels[0].relationshipID)
    print(labels[0])
    print(labels[0].labelID)
    print(labels[0].labelFile)
    print(properties[0])
    print(properties[0].key)
    print(properties[0].value)


testCase()


