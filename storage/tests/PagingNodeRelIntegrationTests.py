from storage.Node import Node
from storage.Property import Property
from storage.Relationship import Relationship
from storage.Label import Label
from storage.NodeStorageManager import NodeStorageManager
from storage.RelationshipStorageManager import RelationshipStorageManager
from storage.UserThread import UserThread

''' This test creates nodes and relationships, and adds the relationships to the nodes.
Checks to make sure that nodes and relationships read at each stage are correct.
This test should fail as data page parameters are currently set, since IDs
don't match with their expected pages. Increase DataPage.MAX_PAGE_ENTRIES to 5
to see test pass. If no assertions fail, test behaves as expected. '''

def fun():
	NodeStorageManager()
	RelationshipStorageManager()

	node0 = NodeStorageManager.createNode()

	node0ID = [[0,0], 0]
	readNode0 = NodeStorageManager.readNode(node0ID)

	print('node ID is {0}'.format(node0.getID()))
	print('read node ID is {0}'.format(readNode0.getID()))
	print('node is in page {0}'.format(readNode0.nodeID[0][1]))

	assert(node0.getID()[1] == readNode0.getID()[1]), 'read and written nodes do not match!'
	assert(node0.getID()[0][1] == readNode0.getID()[0][1]), 'read and written nodes do not match!'

	##################################################################################################
	node1 = NodeStorageManager.createNode()

	readNode0 = NodeStorageManager.readNode(node0ID)

	print('node ID is {0}'.format(node0.getID()))
	print('read node ID is {0}'.format(readNode0.getID()))
	print('node is in page {0}'.format(readNode0.nodeID[0][1]))

	assert(node0.getID()[1] == readNode0.getID()[1]), 'read and written nodes do not match!'
	assert(node0.getID()[0][1] == readNode0.getID()[0][1]), 'read and written nodes do not match!'
	##########################################################

	node1ID = [[0,0], 1]
	readNode1 = NodeStorageManager.readNode(node1ID)
	print('node is in page {0}'.format(readNode1.nodeID[0][1]))

	assert(node1.getID()[1] == readNode1.getID()[1]), 'read and written nodes do not match!'
	assert(node1.getID()[0][1] == readNode1.getID()[0][1]), 'read and written nodes do not match!'

	##################################################################################################

	readNode0 = NodeStorageManager.readNode(node0ID)

	print('node ID is {0}'.format(node0.getID()))
	print('read node ID is {0}'.format(readNode0.getID()))
	print('node is in page {0}'.format(readNode0.nodeID[0][1]))

	assert(node0.getID()[1] == readNode0.getID()[1]), 'read and written nodes do not match!'
	assert(node0.getID()[0][1] == readNode0.getID()[0][1]), 'read and written nodes do not match!'

	#####################################################
	node2 = NodeStorageManager.createNode()

	node2ID = [[0,0], 2]
	readNode2 = NodeStorageManager.readNode(node2ID)

	print('node is in page {0}'.format(readNode2.nodeID[0][1]))

	assert(node2.getID()[1] == readNode2.getID()[1]), 'read and written nodes do not match!'
	assert(node2.getID()[0][1] == readNode2.getID()[0][1]), 'read and written nodes do not match!'
	##################################################################################################

	rel0 = RelationshipStorageManager.createRelationship(node0, node1, 'friendship')

	rel0ID = [[1,0], 0]
	readRel0 = RelationshipStorageManager.readRelationship(rel0ID)

	print('rel0 ID:{0}'.format(rel0.getID()[1]))
	print('readRel0 ID:{0}'.format(readRel0.getID()[1]))
	assert(rel0.getID()[1] == readRel0.getID()[1]), 'read and written relationships do not match!'

	print('rel0 first node ID:{0}'.format(rel0.firstNodeID[1]))
	print('readRel0 first node ID:{0}'.format(readRel0.firstNodeID[1]))
	assert(rel0.firstNodeID[1] == readRel0.firstNodeID[1]), 'read and written relationships do not match!'

	print('rel0 second node ID:{0}'.format(rel0.secondNodeID[1]))
	print('readRel0 second node ID:{0}'.format(readRel0.secondNodeID[1]))
	assert(rel0.secondNodeID[1] == readRel0.secondNodeID[1]), 'read and written relationships do not match!'

	print('rel0 rel type:{0}'.format(rel0.getRelType()))
	print('readRel0 rel type:{0}'.format(readRel0.getRelType()))
	assert(rel0.getRelType() == readRel0.getRelType()), 'read and written relationships do not match!'

	##################################################################################################

	rel1 = RelationshipStorageManager.createRelationship(node0, node2, 'animosity')

	rel1ID = [[1,0], 1]
	readRel1 = RelationshipStorageManager.readRelationship(rel1ID)

	print('rel1 ID:{0}'.format(rel1.getID()[1]))
	print('readRel1 ID:{0}'.format(readRel1.getID()[1]))
	assert(rel1.getID()[1] == readRel1.getID()[1]), 'read and written relationships do not match!'

	print('rel1 first node ID:{0}'.format(rel1.firstNodeID[1]))
	print('readRel1 first node ID:{0}'.format(readRel1.firstNodeID[1]))
	assert(rel1.firstNodeID[1] == readRel1.firstNodeID[1]), 'read and written relationships do not match!'

	print('rel1 second node ID:{0}'.format(rel1.secondNodeID[1]))
	print('readRel1 second node ID:{0}'.format(readRel1.secondNodeID[1]))
	assert(rel1.secondNodeID[1] == readRel1.secondNodeID[1]), 'read and written relationships do not match!'

	print('rel1 rel type:{0}'.format(rel1.getRelType()))
	print('readRel1 rel type:{0}'.format(readRel1.getRelType()))
	assert(rel1.getRelType() == readRel1.getRelType()), 'read and written relationships do not match!'

	###################################################################################################
	rel2 = RelationshipStorageManager.createRelationship(node1, node2, 'pet')

	rel2ID = [[1,0], 2]
	readRel2 = RelationshipStorageManager.readRelationship(rel2ID)

	print('rel2 ID:{0}'.format(rel2.getID()[1]))
	print('readRel2 ID:{0}'.format(readRel2.getID()[1]))
	assert(rel2.getID()[1] == readRel2.getID()[1]), 'read and written relationships do not match!'

	print('rel2 first node ID:{0}'.format(rel2.firstNodeID[1]))
	print('readRel2 first node ID:{0}'.format(readRel2.firstNodeID[1]))
	assert(rel2.firstNodeID[1] == readRel2.firstNodeID[1]), 'read and written relationships do not match!'

	print('rel2 second node ID:{0}'.format(rel2.secondNodeID[1]))
	print('readRel2 second node ID:{0}'.format(readRel2.secondNodeID[1]))
	assert(rel2.secondNodeID[1] == readRel2.secondNodeID[1]), 'read and written relationships do not match!'

	print('rel2 rel type:{0}'.format(rel2.getRelType()))
	print('readRel2 rel type:{0}'.format(readRel2.getRelType()))
	assert(rel2.getRelType() == readRel2.getRelType()), 'read and written relationships do not match!'

	###################################################################################################

	print('***Testing Integration***')
	node0.addRelationship(rel0)

	node0.addRelationship(rel1)

	NodeStorageManager.writeNode(node0, False)

	readNode0 = NodeStorageManager.readNode(node0ID)

	assert(node0.getID()[1] == readNode0.getID()[1]), 'read and written nodes do not match!'
	assert(node0.getID()[0][1] == readNode0.getID()[0][1]), 'read and written nodes do not match!'

	readRel0 = readNode0.relationships[0]

	readRel1 = readNode0.relationships[1]

	print('rel0 ID:{0}'.format(rel0.getID()[1]))
	print('readRel0 ID:{0}'.format(readRel0.getID()[1]))
	assert(rel0.getID()[1] == readRel0.getID()[1]), 'read and written relationships do not match!'

	print('rel0 first node ID:{0}'.format(rel0.firstNodeID[1]))
	print('readRel0 first node ID:{0}'.format(readRel0.firstNodeID[1]))
	assert(rel0.firstNodeID[1] == readRel0.firstNodeID[1]), 'read and written relationships do not match!'

	print('rel0 second node ID:{0}'.format(rel0.secondNodeID[1]))
	print('readRel0 second node ID:{0}'.format(readRel0.secondNodeID[1]))
	assert(rel0.secondNodeID[1] == readRel0.secondNodeID[1]), 'read and written relationships do not match!'

	print('rel0 rel type:{0}'.format(rel0.getRelType()))
	print('readRel0 rel type:{0}'.format(readRel0.getRelType()))
	assert(rel0.getRelType() == readRel0.getRelType()), 'read and written relationships do not match!'

	print('rel1 ID:{0}'.format(rel1.getID()[1]))
	print('readRel1 ID:{0}'.format(readRel1.getID()[1]))
	assert(rel1.getID()[1] == readRel1.getID()[1]), 'read and written relationships do not match!'

	print('rel1 first node ID:{0}'.format(rel1.firstNodeID[1]))
	print('readRel1 first node ID:{0}'.format(readRel1.firstNodeID[1]))
	assert(rel1.firstNodeID[1] == readRel1.firstNodeID[1]), 'read and written relationships do not match!'

	print('rel1 second node ID:{0}'.format(rel1.secondNodeID[1]))
	print('readRel1 second node ID:{0}'.format(readRel1.secondNodeID[1]))
	assert(rel1.secondNodeID[1] == readRel1.secondNodeID[1]), 'read and written relationships do not match!'

	print('rel1 rel type:{0}'.format(rel1.getRelType()))
	print('readRel1 rel type:{0}'.format(readRel1.getRelType()))
	assert(rel1.getRelType() == readRel1.getRelType()), 'read and written relationships do not match!'

	#######################################################################################################

	node2.addRelationship(rel2)

	node2.addRelationship(rel1)

	NodeStorageManager.writeNode(node2, False)

	readNode2 = NodeStorageManager.readNode(node2ID)

	readRel2 = readNode2.relationships[0]

	readRel1 = readNode2.relationships[1]

	print('rel2 ID:{0}'.format(rel2.getID()[1]))
	print('readRel2 ID:{0}'.format(readRel2.getID()[1]))
	assert(rel2.getID()[1] == readRel2.getID()[1]), 'read and written relationships do not match!'

	print('rel2 first node ID:{0}'.format(rel2.firstNodeID[1]))
	print('readRel2 first node ID:{0}'.format(readRel2.firstNodeID[1]))
	assert(rel2.firstNodeID[1] == readRel2.firstNodeID[1]), 'read and written relationships do not match!'

	print('rel2 second node ID:{0}'.format(rel2.secondNodeID[1]))
	print('readRel2 second node ID:{0}'.format(readRel2.secondNodeID[1]))
	assert(rel2.secondNodeID[1] == readRel2.secondNodeID[1]), 'read and written relationships do not match!'

	print('rel2 rel type:{0}'.format(rel2.getRelType()))
	print('readRel2 rel type:{0}'.format(readRel2.getRelType()))
	assert(rel2.getRelType() == readRel2.getRelType()), 'read and written relationships do not match!'


	print('rel1 ID:{0}'.format(rel1.getID()[1]))
	print('readRel1 ID:{0}'.format(readRel1.getID()[1]))
	assert(rel1.getID()[1] == readRel1.getID()[1]), 'read and written relationships do not match!'

	print('rel1 first node ID:{0}'.format(rel1.firstNodeID[1]))
	print('readRel1 first node ID:{0}'.format(readRel1.firstNodeID[1]))
	assert(rel1.firstNodeID[1] == readRel1.firstNodeID[1]), 'read and written relationships do not match!'

	print('rel1 second node ID:{0}'.format(rel1.secondNodeID[1]))
	print('readRel1 second node ID:{0}'.format(readRel1.secondNodeID[1]))
	assert(rel1.secondNodeID[1] == readRel1.secondNodeID[1]), 'read and written relationships do not match!'

	print('rel1 rel type:{0}'.format(rel1.getRelType()))
	print('readRel1 rel type:{0}'.format(readRel1.getRelType()))
	assert(rel1.getRelType() == readRel1.getRelType()), 'read and written relationships do not match!'


user = UserThread(target=fun)

user.start()
