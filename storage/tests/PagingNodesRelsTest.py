from Node import Node
from NodeFile import NodeFile
from Property import Property
from PropertyFile import PropertyFile
from Relationship import Relationship
from RelationshipFile import RelationshipFile
from Label import Label
from LabelFile import LabelFile
from NodeStorageManager import NodeStorageManager

node0 = NodeStorageManager.createNode()

node0ID = [[0,0], 0]
readNode0 = NodeStorageManager.readNode(node0ID)

assert(node0.getID()[1] == readNode0.getID()[1]), 'read and written nodes do not match!'

node1 = NodeStorageManager.createNode()

node1ID = [[0,0], 1]
readNode1 = NodeStorageManager.readNode(node1ID)

assert(node1.getID()[1] == readNode1.getID()[1]), 'read and written nodes do not match!'

rel0 = RelationshipStorageManager.createRelationship(node0, node1, 'friendship')

rel0ID = [[1,0], 0]
readRel0 = RelationshipStorageManager.readRelationship(rel0ID)

assert(rel0.getRelType() == readRel0.getRelType()), 'read and written relationships do not match!'
