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

node0.addProperty(prop0)
node1.addProperty(prop1)

node0.addLabel(label0)
node1.addLabel(label1)

node0.writeNode()
node1.writeNode()

node1read = nodeFile.readNode(0, relationshipFile, propertyFile, labelFile)
node2read = nodeFile.readNode(1, relationshipFile, propertyFile, labelFile)










