from Node import Node
from NodeFile import NodeFile
from NodePage import NodePage
from Property import Property
from PropertyFile import PropertyFile
from Relationship import Relationship
from RelationshipFile import RelationshipFile
from Label import Label
from LabelFile import LabelFile

from StorageManager import StorageManager


nodeFile = NodeFile()
relationshipFile = RelationshipFile()
propFile = PropertyFile()
labelFile = LabelFile()

storageManager = StorageManager(nodeFile, relationshipFile, propFile, labelFile)

# create two nodes 
node0 = storageManager.createNode()
node1 = storageManager.createNode()

rel0 = storageManager.createRelationship(node0, node1)
node0.addRelationship(rel0)
node1.addRelationship(rel0)

prop0 = storageManager.createProperty("1", "2")
prop1 = storageManager.createProperty("3", "4")
prop2 = storageManager.createProperty("5", "1")

label0 = storageManager.createLabel("numb")
label1 = storageManager.createLabel("numb")
label2 = storageManager.createLabel("numb")
label3 = storageManager.createLabel("numb")

node0.addProperty(prop2)
node1.addProperty(prop1)

node0.addLabel(label0)
node1.addLabel(label1)

node0.writeNode()
node1.writeNode()

node1read = nodeFile.readNode(0, relationshipFile, propFile, labelFile)
node2read = nodeFile.readNode(1, relationshipFile, propFile, labelFile)

print()
print("printing nodes....")

print("printing node 1")
print("node1 id: {0}".format(node1read.nodeID))
print("print node1 relationships")
for rel in node1read.relationships:
	print("in a relationship with node: {0}".format(rel.getOtherNodeID(node1read.getID())))
print("print node1 properties")
for prop in node1read.properties:
	print("id {0}".format(prop.getID()))
	print("key: {0}".format(prop.getKey()))
	print("value: {0}".format(prop.getValue()))
print("print node1 labels")
for label in node1read.labels:
	print(label.getLabelStr())


print()
print("printing node 2")
print("node2 id: {0}".format(node2read.nodeID))
print("print node2 relationships")
for rel in node2read.relationships:
	print("in a relationship with node: {0}".format(rel.getOtherNodeID(node2read.getID())))
print("print node2 properties")
for prop in node2read.properties:
	print("id {0}".format(prop.getID()))
	print("key: {0}".format(prop.getKey()))
	print("value: {0}".format(prop.getValue()))
print("print node2 labels")
for label in node2read.labels:
	print(label.getLabelStr())


print(storageManager.node_free_space)
print(storageManager.rel_free_space)
print(storageManager.prop_free_space)
print(storageManager.label_free_space)

storageManager.deleteNode(0)

print(storageManager.node_free_space)
print(storageManager.rel_free_space)
print(storageManager.prop_free_space)
print(storageManager.label_free_space)

'''
print(node3read.nodeID)
print(node3read.relationships)
print(node3read.properties)
print(node3read.labels)
'''











