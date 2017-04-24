# Node class: stores data

# Storage: Nodes will be stored as fixed size records which are 9 bytes in 
# length.
# Bytes 1-3: Node ID
# Byte 4: In-use flag (1 for in-use, 0 for not)
# Bytes 5-8: ID of first relationship connected to node
# Bytes 9-11: ID of first property (key-value pair) for node
# Bytes 12-14: points to label store for node
# Byte 15: flags  
class Node:
    NODE_ID_OFFSET = 0
    IN_USE_FLAG_OFFSET = 3 
    REL_ID_OFFSET = 4
    PROPERTY_ID_OFFSET = 8
    LABEL_STORE_PTR_OFFSET = 11
    FLAGS_OFFSET = 14

    storageSize = 15
    numNodes = 0

    def __init__(self, nodeFile, nodeID=numNodes):
		# relationships is the list of relationships this node is in 
        self.relationships = []
		# key-value pairs or properties stored within node
		# e.g. name: Jane
        self.properties = []
		# labels indicate the type of a node, a node can have multiple labels
		# e.g. person, bank account, id
        self.labels = []

        self.nodeID = nodeID
		# increment number of nodes 
        Node.numNodes += 1

        self.nodeFile = nodeFile

        self.startOffset = self.nodeID * Node.storageSize

	# This method adds a node with a relationship to this node's adj list
    def addRelationship(self, rel):
        self.relationships.append(rel)

	# This method adds data to a node 
    def addProperty(self, key, value):
        self.properties[key] = value

	# This method adds labels to a node
    def addLabel(self, nodeLabel):
        self.labels.append(nodeLabel)

    def getID(self):
        return self.nodeID

    def getRelationships(self):
        return self.relationships

    def getData(self):
        return self.data

    def getLabels(self):
        return self.labels

    # This method writes this node to the given node file
    def writeNode(self):
        # open node file
        storeFileName = self.nodeFile.getFileName()
        storeFile = open(storeFileName, 'a')

        # write node id
        storeFile.seek(self.startOffset + NODE_ID_OFFSET)
        storeFile.write(self.nodeID)

        # write in-use flag
        storeFile.seek(self.startOffset + IN_USE_FLAG_OFFSET)
        storeFile.write(1)

        # write first relationship ID
        storeFile.seek(self.startOffset + REL_ID_OFFSET)
        firstRel = self.relationships[0]
        storeFile.write(firstRel.getID())

		# write first property ID
        storeFile.seek(self.startOffset + PROPERTY_ID_OFFSET)
        firstProp = self.properties[0]
        storeFile.write(firstProp.getID())

        # write relationships to relationship file
        for relIndex in range(0, len(self.relationships)):
            rel = self.relationships[relIndex]
            if relIndex == 0:
                nullRelationship = Relationship(-1, -1, -1, "")
                rel.writeRelationship(self, nullRelationship, self.relationships[relIndex + 1])
            elif relIndex == len(self.relationships) - 1:
                nullRelationship = Relationship(-1, -1, -1, "")
                rel.writeRelationship(self, self.relationships[relIndex - 1], nullRelationship)
            else:
                rel.writeRelationship(self, self.relationships[relIndex - 1], 
                    self.relationships[relIndex + 1])

		# write properties to property file
        for propIndex in range(0, len(self.properties)):
            prop = self.properties[propIndex]

            # no next property
            if propIndex == len(self.properties) - 1:
                nullProperty = Property(-1, -1, -1, "")
                prop.writeProperty(nullProperty)

            else:
                prop.writeProperty(self.properties[propIndex + 1])


        # write labels
        for labelIndex in range(0, len(self.labels)):
            label = self.labels[labelIndex]

            # no next label
            if labelIndex == len(self.labels) - 1:
                nextLabel = -1
            
            else:
                nextLabel = self.labels[labelIndex + 1]

            label.writeLabel(nextLabel)


















