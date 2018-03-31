from Node import Node

from Property import Property

from Relationship import Relationship

from Label import Label

from NodeStorageManager import NodeStorageManager
from RelationshipStorageManager import RelationshipStorageManager

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

print('rel0 ID:{0}'.format(rel0.getID()[1]))
print('readRel0 ID:{0}'.format(readRel0.getID()[1]))

print('rel0 first node ID:{0}'.format(rel0.firstNodeID[1]))
print('readRel0 first node ID:{0}'.format(readRel0.firstNodeID[1]))

print('rel0 second node ID:{0}'.format(rel0.secondNodeID[1]))
print('readRel0 second node ID:{0}'.format(readRel0.secondNodeID[1]))

print('rel0 rel type:{0}'.format(rel0.getRelType()))
print('readRel0 rel type:{0}'.format(readRel0.getRelType()))
assert(rel0.getRelType() == readRel0.getRelType()), 'read and written relationships do not match!'
