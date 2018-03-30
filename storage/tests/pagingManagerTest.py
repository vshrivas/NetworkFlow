from storage.Node import Node
from storage.NodeFile import NodeFile
from storage.Property import Property
from storage.PropertyFile import PropertyFile
from storage.Relationship import Relationship
from storage.RelationshipFile import RelationshipFile
from storage.Label import Label
from storage.LabelFile import LabelFile
from storage.StorageManager import StorageManager

nodeStorageManager = NodeStorageManager()

node0 = nodeStorageManager.createNode()
node1 = nodeStorageManager.createNode()

