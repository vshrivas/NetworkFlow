# has metadata keeping track of number of node files
class NodeStorageManager(StorageManager):
	nodeFiles = []
	metaDataPath = "datastore"
	def __init__(self):
		# open node storage meta data file
		# read number of node files 
		# create file objects for each of the node files, and make a list of these

	readNode(pageID):
		pageID = nodeID[0] 			# pageID[0] = 0, pageID[1] = pageIndex
		nodeIndex = nodeID[1]

		pageIndex = pageID[1]		# which page node is in, page IDs are unique across all files

		# file number of node file page is in
		fileNo = pageIndex / DataFile.MAX_FILE_PAGES 
		nodeFile = nodeFiles[fileNo]

		# returns a list of first relationship, first property, and first label associated with node
		nodeID = [pageID, nodeIndex]
		nodeAttributes = nodeFile.readNode(pageID, nodeIndex)

		firstRelID = nodeAttributes[0]
		firstPropID = nodeAttributes[1]
		firstLabelID = nodeAttributes[2]

	# takes in a node object 
	def writeNode(node):
        """Writes this node to the node's node file according to the storage 
        format given in the class description and writes this node's relationships, 
        properties, and labels to the node's relationship file, property file, and 
        label file, respectively.
        """
        if DEBUG:
            print("properties in node")
            for prop in node.properties:
                print(prop.getID())

            print("labels in node:")
            for label in node.labels:
                print(label.getLabelID())

            print("writing node...")

        nodeID = node.nodeID
        pageID = nodeID[0] 			# pageID[0] = 0, pageID[1] = pageIndex
		nodeIndex = nodeID[1]

		pageIndex = pageID[1]		# which page node is in, page IDs are unique across all files
		# file number of node file page is in
		fileNo = pageIndex / DataFile.MAX_FILE_PAGES 
		nodeFile = nodeFiles[fileNo - 1]

        nodeFile.writeNode(node)

        if DEBUG:
            print("writing relationships to relationship file ...")

        RelationshipStoreManager.writeRelationships(node.relationships)
        
        if DEBUG:
            print("writing properties to property file ...")

        PropertyStoreManager.writeProperties(node.properties)

        if DEBUG:
            print("writing labels to property file ...")

        LabelStoreManager.writeLabels(node.labels)

	def createNode():
		# find if last file's last page has space
		lastFile = nodeFiles[len(nodeFiles) - 1]
		nodePage = lastFile.hasSpace()

		# last node file is full
		if nodePage == None:
			# make new file
			newFile = NodeFile(len(nodeFiles))