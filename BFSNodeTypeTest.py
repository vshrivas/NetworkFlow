from storage.Node import Node
from storage.NodeFile import NodeFile
from storage.NodePage import NodePage
from storage.Property import Property
from storage.PropertyFile import PropertyFile
from storage.Relationship import Relationship
from storage.RelationshipFile import RelationshipFile
from storage.Label import Label
from storage.LabelFile import LabelFile
from storage.StorageManager import StorageManager
from queryeval.degreeQueries import breadthFirstSearch

# initial set up
nodeFile = NodeFile()
relationshipFile = RelationshipFile()
propFile = PropertyFile()
labelFile = LabelFile()
storageManager = StorageManager(nodeFile, relationshipFile, propFile, labelFile)

# create nodes
harryPotter = storageManager.createNode()
propPotterName = storageManager.createProperty("Name", "Harry Potter")
harryPotter.addProperty(propPotterName)

ron = storageManager.createNode()
propRonName = storageManager.createProperty("Name", "Ronald Weasley")
ron.addProperty(propRonName)

hermione = storageManager.createNode()
propHermioneName = storageManager.createProperty("Name", "Hermione Granger")
hermione.addProperty(propHermioneName)

crookshanks = storageManager.createNode()
propCrookshanksName = storageManager.createProperty("Name", "Crookshanks")
catLabel = storageManager.createLabel("cat")
crookshanks.addProperty(propCrookshanksName)
crookshanks.addLabel(catLabel)

# create relationships
rel0 = storageManager.createRelationship(hermione, crookshanks, "ownership")
hermione.addRelationship(rel0)
crookshanks.addRelationship(rel0)

rel1 = storageManager.createRelationship(harryPotter, ron, "friendship")
harryPotter.addRelationship(rel1)
ron.addRelationship(rel1)

rel2 = storageManager.createRelationship(harryPotter, hermione, "friendship")
harryPotter.addRelationship(rel2)
hermione.addRelationship(rel2)

rel3 = storageManager.createRelationship(hermione, ron, "friendship")
hermione.addRelationship(rel3)
ron.addRelationship(rel3)

# write nodes to disk
harryPotter.writeNode()
ron.writeNode()
hermione.writeNode()
crookshanks.writeNode()

# find all friends of harry potter who own cats
resultQueue = breadthFirstSearch(harryPotter, [("friendship", "", 1), ("ownership", "cat", 0)], 
	nodeFile, relationshipFile, propFile, labelFile)

print("after breadth first search")

while(not resultQueue.empty()):
	result = resultQueue.get()
	print("got node")
	#print(friend.getID())
	#print(len(friend.properties))
	for prop in result.properties:
		print("key: {0}".format(prop.key))
		print("value: {0}".format(prop.value))





