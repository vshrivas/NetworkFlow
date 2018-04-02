import threading 
from storage.Node import Node
from storage.Property import Property
from storage.Relationship import Relationship
from storage.Label import Label
from storage.NodeStorageManager import NodeStorageManager
from storage.RelationshipStorageManager import RelationshipStorageManager

''' Creates 5 user threads each manipulating same field of same relationships.
Each thread adds a letter to the relationship type. Make sure all letters are
present in type at the end. Test passes if assertion passes. '''

def user0(rel):
	rel.type += 'a'
	print('user 0 writing rel...')
	rel = RelationshipStorageManager.writeRelationship(rel, False)
	print('user 0 reading rel...')
	readRel = RelationshipStorageManager.readRelationship(rel.getID())

def user1(rel):
	rel.type += 'a'
	print('user 1 writing rel...')
	rel = RelationshipStorageManager.writeRelationship(rel, False)
	print('user 1 reading rel...')
	readRel = RelationshipStorageManager.readRelationship(rel.getID())

def user2(rel):
	rel.type += 'a'
	print('user 2 writing rel...')
	rel = RelationshipStorageManager.writeRelationship(rel, False)
	print('user 2 reading rel...')
	readRel = RelationshipStorageManager.readRelationship(rel.getID())

def user3(rel):
	rel.type += 'a'
	print('user 3 writing rel...')
	rel = RelationshipStorageManager.writeRelationship(rel, False)
	print('user 3 reading rel...')
	readRel = RelationshipStorageManager.readRelationship(rel.getID())

def user4(rel):
	rel.type += 'a'
	print('user 4 writing rel...')
	rel = RelationshipStorageManager.writeRelationship(rel, False)
	print('user 4 reading rel...')
	readRel = RelationshipStorageManager.readRelationship(rel.getID())

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

node1 = NodeStorageManager.createNode()
node1ID = [[0,1], 0]
readNode1 = NodeStorageManager.readNode(node1ID)
print('node is in page {0}'.format(readNode1.nodeID[0][1]))

assert(node1.getID()[1] == readNode1.getID()[1]), 'read and written nodes do not match!'
assert(node1.getID()[0][1] == readNode1.getID()[0][1]), 'read and written nodes do not match!'

rel0 = RelationshipStorageManager.createRelationship(node0, node1, '')

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


u0 = threading.Thread(target=user0, args=(rel0,))
u1 = threading.Thread(target=user1, args=(rel0,))
u2 = threading.Thread(target=user2, args=(rel0,))
u3 = threading.Thread(target=user3, args=(rel0,))
u4 = threading.Thread(target=user4, args=(rel0,))

u0.start()
u1.start()
u2.start()
u3.start()
u4.start()

assert(rel0.type == 'aaaaa')
