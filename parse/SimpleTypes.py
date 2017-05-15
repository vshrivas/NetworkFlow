class SimpleNode:
    def __init__(self, varName):
        self.varName = varName

        self.relationships = []
        self.labels = []
        self.properties = {}

class SimpleRelationship:
    def __init__(self, label, node1, node2):
        self.label = label
        self.node1 = node1
        self.node2 = node2

        self.varname = None
        self.properties = {}

class MatchRelationship:
    def __init__(self, label):
        self.label = label

        self.varname = None
        self.properties = 