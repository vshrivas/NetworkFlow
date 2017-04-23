class RelationshipFile:
	numFiles = 0

	def _init_(self):
		numFiles += 1
		self.fileID = numFiles

		# create relationship file
		self.fileName = "RelationshipFile{0}".format(self.fileID)
		relFile = open(self.fileName, 'w')
		relFile.close()

	def getFileName():
		return self.fileName