class RelationshipFile:
	numFiles = 0

	def _init_(self):
		numFiles += 1
		self.fileID = numFiles
		self.fileName = "RelationshipFile{0}".format(self.fileID)
		self.file = open(self.fileName, 'w')

	def getFile():
		return self.file