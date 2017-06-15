class DummyRelationship:
    def __init__(self, relType):
        self.type = relType 
        self.properties = []

    # This method adds property data to a relationship
    def addProperty(self, prop):
        self.properties.append(prop)

    def getProperties(self):
        return self.properties

    def getRelType(self):
        return self.type