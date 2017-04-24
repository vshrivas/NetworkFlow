# Storage: 
# Bytes 1-4: Relationship ID
# Bytes 5-7: Node 1 ID
# Bytes 8-10: Node 2 ID 
# Bytes 11-14: Node 1 Next Rel ID
# Bytes 15-18: Node 1 Prev Rel ID
# Bytes 19-22: Node 2 Next Rel ID
# Bytes 23-26: Node 2 Prev Rel ID

# Uniqueness:
# If relationship with node 1 = A and node 2 = B exists, a relationship with 
# node 1 = B and node 2 = A should not exist 

class Relationship:
	RELATIONSHIP_ID_OFFSET = 0
	NODE1_ID_OFFSET = 4
	NODE2_ID_OFFSET = 7
	NODE1_NEXT_REL_ID_OFFSET = 10
	NODE1_PREV_REL_ID_OFFSET = 14
	NODE2_NEXT_REL_ID_OFFSET = 18
	NODE2_PREV_REL_ID_OFFSET = 22

	storageSize = 26
	numRelationships = 0

	def _init_(self, node1ID, node2ID, relationshipFile, relationshipID=numRelationships):
		self.firstNodeID = node1ID
		self.secondNodeID = node2ID

		self.relationshipID = relationshipID
		numRelationships += 1

		self.relationshipFile = relationshipFile

		self.startOffset = self.relationshipID * Relationship.storageSize 

	def writeRelationship(self, node, prevRel, nextRel):
		# open relationship file
		storeFileName = self.relationshipFile.getFileName()
		storeFile = open(storeFileName, 'a')

		# seek to location for relationship
		storeFile.seek(startOffset)

		# write relationship ID
		storeFile.write(self.relationshipID)

		# write node 1 id
		storeFile.seek(startOffset + NODE1_ID_OFFSET)
		storeFile.write(self.firstNodeID)

		# write node 2 id
		storeFile.seek(startOffset + NODE2_ID_OFFSET)
		storeFile.write(self.secondNodeID)

		# find which node relationship is being written for
		if node.getID() == node1.getID():
			storeFile.seek(startOffset + NODE1_NEXT_REL_ID_OFFSET)
			storeFile.write(nextRel.getID())

			storeFile.seek(startOffset + NODE1_PREV_REL_ID_OFFSET)
			storeFile.write(prevRel.getID())

		else:
			storeFile.seek(startOffset + NODE2_PREV_REL_ID_OFFSET)
			storeFile.write(nextRel.getID())

			storeFile.seek(startOffset + NODE2_PREV_REL_ID_OFFSET)
			storeFile.write(prevRel.getID())





