from Node import Node
from NodeFile import NodeFile
from NodePage import NodePage
from Property import Property
from PropertyFile import PropertyFile
from Relationship import Relationship
from RelationshipFile import RelationshipFile
from Label import Label
from LabelFile import LabelFile

nodeFile = NodeFile()
node1 = Node(nodeFile)
node2 = Node(nodeFile)
# node3 = Node(nodeFile)

relationshipFile = RelationshipFile()
relationship1 = Relationship(node1.getID(), node2.getID(), relationshipFile)
# relationship2 = Relationship(node2.getID(), node3.getID(), relationshipFile)
node1.addRelationship(relationship1)
node2.addRelationship(relationship1)
# node2.addRelationship(relationship2)
# node3.addRelationship(relationship2)

propertyFile = PropertyFile()
property1 = Property("1", "2", propertyFile)
property2 = Property("3", "4", propertyFile)
property3 = Property("5", "1", propertyFile)
#node1.addProperty(property1)
node2.addProperty(property2)
node1.addProperty(property3)

labelFile = LabelFile()
label1 = Label("number", labelFile)
label2 = Label("number2", labelFile)
label3 = Label("number", labelFile)
label4 = Label("number", labelFile)
node1.addLabel(label1)
#node1.addLabel(label2)
#label1.setNextLabelID(label2.getLabelID())

node2.addLabel(label3)
# node3.addLabel(label4)

node1.writeNode()
node2.writeNode()
# node3.writeNode()

node1read = nodeFile.readNode(0, relationshipFile, propertyFile, labelFile)
node2read = nodeFile.readNode(1, relationshipFile, propertyFile, labelFile)
# node3read = nodeFile.readNode(3, relationshipFile, propertyFile, labelFile)

'''print(node1read.nodeID)
print(node1read.relationships)
print(node1read.properties)
print(node1read.labels)

print(node2read.nodeID)
print(node2read.relationships)
print(node2read.properties)
print(node2read.labels)'''

'''
print(node3read.nodeID)
print(node3read.relationships)
print(node3read.properties)
print(node3read.labels)
'''

