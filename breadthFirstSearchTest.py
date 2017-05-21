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

# tests friends
nodeFile = NodeFile()
relationshipFile = RelationshipFile()
propFile = PropertyFile()
labelFile = LabelFile()
storageManager = StorageManager(nodeFile, relationshipFile, propFile, labelFile)

# create nodes 
vaish = storageManager.createNode()
propVaishName = storageManager.createProperty("Name", "Vaishnavi")
vaish.addProperty(propVaishName)

noosho = storageManager.createNode()
propNooshName = storageManager.createProperty("Name", "Anusha")
noosho.addProperty(propNooshName)

claro = storageManager.createNode()
propClaroName = storageManager.createProperty("Name", "Clara")
claro.addProperty(propClaroName)

ayyo = storageManager.createNode()
propAyyoName = storageManager.createProperty("Name", "Aya")
ayyo.addProperty(propAyyoName)

emilo = storageManager.createNode()
propEmiloName = storageManager.createProperty("Name", "Emily")
emilo.addProperty(propEmiloName)

frand2 = storageManager.createNode()
propFrand2Name = storageManager.createProperty("Name", "Frand2")
frand2.addProperty(propFrand2Name)

frand3 = storageManager.createNode()
propFrand3Name = storageManager.createProperty("Name", "Frand3")
frand3.addProperty(propFrand3Name)

frand4 = storageManager.createNode()
propFrand4Name = storageManager.createProperty("Name", "Frand4")
frand4.addProperty(propFrand4Name)

frand5 = storageManager.createNode()
propFrand5Name = storageManager.createProperty("Name", "Frand5")
frand5.addProperty(propFrand5Name)

# create relationships
rel0 = storageManager.createRelationship(vaish, noosho, "friendship")
vaish.addRelationship(rel0)
noosho.addRelationship(rel0)

rel1 = storageManager.createRelationship(vaish, claro, "friendship")
vaish.addRelationship(rel1)
claro.addRelationship(rel1)

rel2 = storageManager.createRelationship(vaish, ayyo, "friendship")
vaish.addRelationship(rel2)
ayyo.addRelationship(rel2)

rel3 = storageManager.createRelationship(vaish, emilo, "friendship")
vaish.addRelationship(rel3)
emilo.addRelationship(rel3)

rel4 = storageManager.createRelationship(emilo, frand2, "friendship")
frand2.addRelationship(rel4)
emilo.addRelationship(rel4)

rel5 = storageManager.createRelationship(frand3, frand2, "friendship")
frand2.addRelationship(rel5)
frand3.addRelationship(rel5)

rel6 = storageManager.createRelationship(claro, frand4, "friendship")
claro.addRelationship(rel6)
frand4.addRelationship(rel6)

rel7 = storageManager.createRelationship(frand4, frand5, "friendship")
frand4.addRelationship(rel7)
frand5.addRelationship(rel7)

# write nodes to disk
vaish.writeNode()
noosho.writeNode()
claro.writeNode()
emilo.writeNode()
ayyo.writeNode()
frand2.writeNode()
frand3.writeNode()
frand4.writeNode()
frand5.writeNode()

# find all friends of friends of friends of Vaishnavi
friendQueue = breadthFirstSearch(vaish, [("friendship", ""), ("friendship", ""), ("friendship", "")], 
	nodeFile, relationshipFile, propFile, labelFile)

print("after breadth first search")

while(not friendQueue.empty()):
	friend = friendQueue.get()
	print("got node")
	print(friend.getID())
	print(len(friend.properties))
	for prop in friend.properties:
		print("key: {0}".format(prop.key))
		print("value: {0}".format(prop.value))

# tests friends of friends

