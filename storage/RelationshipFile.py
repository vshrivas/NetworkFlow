class RelationshipFile:
    numFiles = 0

    def __init__(self, createFile=True):
        RelationshipFile.numFiles += 1
        self.fileID = RelationshipFile.numFiles

        # create relationship file if it doesn't already exist
        self.fileName = "RelationshipFile{0}.store".format(self.fileID)
        try:
            relFile = open(self.fileName, 'r+b')
        except FileNotFoundError:
            relFile = open(self.fileName, 'wb')
        relFile.close()

    def getFileName(self):
        return self.fileName
