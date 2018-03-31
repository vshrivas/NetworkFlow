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

node2 = NodeStorageManager.createNode()

node2ID = [[0,0], 2]
readNode2 = NodeStorageManager.readNode(node2ID)

assert(node2.getID()[1] == readNode2.getID()[1]), 'read and written nodes do not match!'

node3 = NodeStorageManager.createNode()

node3ID = [[0,0], 3]
readNode3 = NodeStorageManager.readNode(node3ID)

assert(node3.getID()[1] == readNode3.getID()[1]), 'read and written nodes do not match!'

node4 = NodeStorageManager.createNode()

node4ID = [[0,0], 4]
readNode4 = NodeStorageManager.readNode(node4ID)

assert(node4.getID()[1] == readNode4.getID()[1]), 'read and written nodes do not match!'

