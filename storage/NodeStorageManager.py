# has metadata keeping track of number of node files
class NodeStorageManager(StorageManager):
	nodeFiles = []
	metaDataPath = "datastore"
	def __init__(self):
		# open node storage meta data file
		# read number of node files 
		# create file objects for each of the node files, and make a list of these

	readNode(pageID, nodeID):
		# file number of node file page is in
		fileNo = pageID / DataFile.MAX_FILE_SIZE 
		nodeFile = nodeFiles[fileNo - 1]

		# returns a list of first relationship, first property, and first label associated with node
		nodeAttributes = nodeFile.readNode(pageID, nodeID)

		firstRelID = nodeAttributes[0]
		firstPropID = nodeAttributes[1]
		firstLabelID = nodeAttributes[2]

		nodeRelationships = RelationshipStoreManager.getRelChain(firstRelID)
		nodeProperties = PropertyStoreManager.getPropChain(firstPropID)
		nodeLabels = LabelStoreManager.getLabelChain(firstLabelID)

		node = Node(pageID, nodeID)
		node.addRelationships(nodeRelationships)
		node.addProperties(nodeProperties)
		node.addLabels(nodeLabels)

		return node

	createNode():

	writeNode(pageID, nodeID):