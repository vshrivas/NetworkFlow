class DummyNode:

    def __init__(self):
        self.relationships = []
        self.properties = []
        self.labels = []

    # This method adds property data to a node
    def addProperty(self, prop):
        self.properties.append(prop)

    # This method adds labels to a node
    def addLabel(self, nodeLabel):
        self.labels.append(nodeLabel)

    def getLabels(self):
        return self.labels