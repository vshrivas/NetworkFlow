class BasicNode:
    def __init__(self, varName):
        self.varName = varName

        self.relationships = []
        self.labels = []
        self.properties = {}

class BasicRelationship:
    def __init__(self, label, node1, node2):
        self.label = label
        self.node1 = node1
        self.node2 = node2

        self.varname = None
        self.properties = {}

class SimpleNode(BasicNode):
    pass

class SimpleRelationship(BasicRelationship):
    pass

class DummyNode(BasicNode):
    pass

class DummyRelationship(BasicRelationship):
    pass