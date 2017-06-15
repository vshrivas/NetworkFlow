class DummyNode:

    def __init__(self):
        self.properties = []
        self.labelStrs = []

    # This method adds property data to a node
    def addProperty(self, prop):
        self.properties.append(prop)

    # This method adds labels to a node
    def addLabel(self, nodeLabelStr):
        self.labelStrs.append(nodeLabelStr)

    def getLabels(self):
        return self.labelStrs

    def getProperties(self):
        return self.properties

