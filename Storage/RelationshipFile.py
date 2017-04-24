class RelationshipFile:
	numFiles = 0

	def __init__(self):
		RelationshipFile.numFiles += 1
		self.fileID = RelationshipFile.numFiles

		# create relationship file
		self.fileName = "RelationshipFile{0}".format(self.fileID)
		relFile = open(self.fileName, 'w')
		relFile.close()

	def getFileName(self):
		return self.fileName
