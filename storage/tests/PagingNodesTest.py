from storage.Node import Node
from storage.NodeFile import NodeFile
from storage.Property import Property
from storage.PropertyFile import PropertyFile
from storage.Relationship import Relationship
from storage.RelationshipFile import RelationshipFile
from storage.Label import Label
from storage.LabelFile import LabelFile
from storage.NodeStorageManager import NodeStorageManager
from storage.UserThread import UserThread

def fun():
	node0 = NodeStorageManager.createNode()

	node0ID = [[0,0], 0]
	readNode0 = NodeStorageManager.readNode(node0ID)

	assert(node0.getID()[1] == readNode0.getID()[1]), 'read and written nodes do not match!'

	node1 = NodeStorageManager.createNode()

	node1ID = [[0,1], 0]
	readNode1 = NodeStorageManager.readNode(node1ID)

	assert(node1.getID()[1] == readNode1.getID()[1]), 'read and written nodes do not match!'

	node2 = NodeStorageManager.createNode()

	node2ID = [[0,2], 0]
	readNode2 = NodeStorageManager.readNode(node2ID)

	assert(node2.getID()[1] == readNode2.getID()[1]), 'read and written nodes do not match!'

	node3 = NodeStorageManager.createNode()

	node3ID = [[0,3], 0]
	readNode3 = NodeStorageManager.readNode(node3ID)

	assert(node3.getID()[1] == readNode3.getID()[1]), 'read and written nodes do not match!'

	node4 = NodeStorageManager.createNode()

	node4ID = [[0,4], 0]
	readNode4 = NodeStorageManager.readNode(node4ID)

	assert(node4.getID()[1] == readNode4.getID()[1]), 'read and written nodes do not match!'

user = UserThread(target=fun)

user.start()
