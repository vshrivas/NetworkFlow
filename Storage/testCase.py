from Node import Node
from NodeFile import NodeFile

from Property import Property
from PropertyFile import PropertyFile

from Label import Label
from LabelFile import LabelFile

from Relationship import Relationship
from RelationshipFile import RelationshipFile


def testCase():
    nodeFile = NodeFile()
    relationshipFile = RelationshipFile()
    propertyFile = PropertyFile()
    labelFile = LabelFile()

    # create node, create property
    node1 = Node(nodeFile)
    property1 = Property('Name', 'John', propertyFile)

    node1.addProperty(property1)

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

    print(rels[0])


testCase()


