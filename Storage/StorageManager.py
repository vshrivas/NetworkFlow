from Label import Label
from LabelFile import LabelFile
from Node import Node
from NodeFile import NodeFile
from Property import Property
from PropertyFile import PropertyFile
from Relationship import Relationship
from RelationshipFile import RelationshipFile

# Storage manager that manages where nodes, relationships, properties, and labels
# are allocated in their respective files.
class StorageManager:

    def __init__(self, nodeFile, relationshipFile, propertyFile, labelFile):
        self.nodeFile = nodeFile
        self.relationshipFile = relationshipFile
        self.propertyFile = propertyFile
        self.labelFile = labelFile
        # list of locations in node file with free space for nodes (specified by nodeIDs)
        self.free_space = [0]
    
    # Finds free space for node (potentially location to the right of all nodes if 
    # there is no free space), creates a node, and writes the node to the node file.
    # It returns the created node.
    def createNode(self):
        if len(free_space) > 0:
            node = Node(nodeFile, self.free_space[len(self.free_space) - 1])
            node.writeNode()
            self.free_space.pop()
            return node
        node = Node(nodeFile, Node.numNodes)
        node.writeNode()
        return node
        
    
    
