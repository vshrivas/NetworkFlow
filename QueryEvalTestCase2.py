from .storage.Node import Node
from .storage.NodeFile import NodeFile
from .storage.NodePage import NodePage
from .storage.Property import Property
from .storage.PropertyFile import PropertyFile
from .storage.Relationship import Relationship
from .storage.RelationshipFile import RelationshipFile
from .storage.Label import Label
from .storage.LabelFile import LabelFile
from .storage.StorageManager import StorageManager

#from storage.DummyNode import DummyNode
#from storage.DummyRelationship import DummyRelationship

from parse.SimpleTypes import DummyNode, DummyRelationship

from .queryeval.degreeQueries import breadthFirstSearch

# initial set up
nodeFile = NodeFile()
relationshipFile = RelationshipFile()
propFile = PropertyFile()
labelFile = LabelFile()
storageManager = StorageManager(nodeFile, relationshipFile, propFile, labelFile)

# create nodes
harryPotter = storageManager.createNode()
propPotterName = storageManager.createProperty("Name", "Harry Potter")
hpLabel1 = storageManager.createLabel("Harry Potter")
hpLabel2 = storageManager.createLabel("Half Blood")
harryPotter.addProperty(propPotterName)
harryPotter.addLabel(hpLabel1)
harryPotter.addLabel(hpLabel2)

ron = storageManager.createNode()
propRonName = storageManager.createProperty("Name", "Ronald Weasley")
ronLabel = storageManager.createLabel("Pure Blood")
ron.addProperty(propRonName)
ron.addLabel(ronLabel)

hermione = storageManager.createNode()
propHermioneName = storageManager.createProperty("Name", "Hermione Granger")
hermioneLabel = storageManager.createLabel("Muggle Born")
hermione.addProperty(propHermioneName)
hermione.addLabel(hermioneLabel)

crookshanks = storageManager.createNode()
propCrookshanksName = storageManager.createProperty("Name", "Crookshanks")
propBlue = storageManager.createProperty("Color", "Blue")
catLabel = storageManager.createLabel("cat")
crookshanks.addProperty(propCrookshanksName)
crookshanks.addProperty(propBlue)
crookshanks.addLabel(catLabel)

hermione2 = storageManager.createNode()
propHermioneName2 = storageManager.createProperty("Name", "Hermione Granger_clone")
hermione2.addProperty(propHermioneName2)
hermione2.addLabel(hermioneLabel)

crookshanks2 = storageManager.createNode()
propCrookshanksName2 = storageManager.createProperty("Name", "Crookshanks_clone")
crookshanks2.addProperty(propCrookshanksName2)
crookshanks2.addProperty(propBlue)
crookshanks2.addLabel(catLabel)

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

rel4 = storageManager.createRelationship(hermione2, crookshanks2, "ownership")
hermione2.addRelationship(rel4)
crookshanks2.addRelationship(rel4)

rel5 = storageManager.createRelationship(harryPotter, hermione2, "friendship")
harryPotter.addRelationship(rel5)
hermione2.addRelationship(rel5)

rel6 = storageManager.createRelationship(hermione2, ron, "friendship")
hermione2.addRelationship(rel6)
ron.addRelationship(rel6)

# write nodes to disk
harryPotter.writeNode()
ron.writeNode()
hermione.writeNode()
crookshanks.writeNode()
hermione2.writeNode()
crookshanks2.writeNode()

# query: find all friends of muggle born people who own blue cats

# [Blue cats (node 1), ownership (rel 1), Muggle Born (node 2), friendship (rel 2), (node 3)]
# Last nodes of chains should be nodes with names Harry Potter and Ronald Weasley
dummyNode1 = DummyNode()
dummyNode1.addLabel("cat")
dummyNode1.addProperty(("Color", "Blue"))

dummyRel1 = DummyRelationship("ownership")

dummyNode2 = DummyNode()
dummyNode2.addLabel("Muggle Born")

dummyRel2 = DummyRelationship("friendship")

dummyNode3 = DummyNode()

nodes = [dummyNode1, dummyNode2, dummyNode3]
rels = [dummyRel1, dummyRel2]

goodChains = breadthFirstSearch(nodes, rels, nodeFile, relationshipFile, propFile, labelFile)

print("after breadth first search")

for chain in goodChains:
    print("got chain")
    #print(friend.getID())
    #print(len(friend.properties))
    for element in chain:
        for prop in element[0].properties:
            print("key: {0}".format(prop.key))
            print("value: {0}".format(prop.value))
