# Storage: 
# Bytes 1-4: Relationship ID
# Bytes 5-7: Node 1 ID
# Bytes 8-10: Node 2 ID 
# Bytes 11-14: Node 1 Next Rel ID
# Bytes 15-18: Node 1 Prev Rel ID
# Bytes 19-22: Node 2 Next Rel ID
# Bytes 23-26: Node 2 Prev Rel ID
class Relationship:
	storageSize = 26
	numRelationships = 0

	def _init_(self, node1, node2):
			self.firstNode = node1
			self.secondNode = node2

			self.relationshipID = numRelationships
			numRelationships += 1
