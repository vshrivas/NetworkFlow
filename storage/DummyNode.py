class DummyNode:
    
    def __init__(self):
        self.relationships = []
        self.properties = []
        self.labels = []

    # This method adds a node with a relationship to this node's adj list
    def addRelationship(self, rel):
        self.relationships.append(rel)

    # This method adds property data to a node
    def addProperty(self, prop):
        self.properties.append(prop)

    # This method adds labels to a node
    def addLabel(self, nodeLabel):
        self.labels.append(nodeLabel)