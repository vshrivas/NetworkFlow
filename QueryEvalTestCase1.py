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
from .storage.DummyNode import DummyNode
from .storage.DummyRelationship import DummyRelationship
from .queryeval.degreeQueries import breadthFirstSearch_

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
harryPotter.addProperty(propPotterName)
harryPotter.addLabel(hpLabel1)

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

# query: find all muggle friends of harry potter who own cats

# [Harry Potter (node 1), friendship (rel 1), Muggle Born (node 2), ownership (rel 2), cat (node 3)]
dummyNode1 = DummyNode()
dummyNode1.addLabel("Harry Potter")

dummyRel1 = DummyRelationship("friendship")

dummyNode2 = DummyNode()
dummyNode2.addLabel("Muggle Born")

dummyRel2 = DummyRelationship("ownership")

dummyNode3 = DummyNode()
dummyNode3.addLabel("cat")

nodes = [dummyNode1, dummyNode2, dummyNode3]
rels = [dummyRel1, dummyRel2]

print("STARTING BFS!!!")

goodChains = breadthFirstSearch_(nodes, rels, nodeFile, relationshipFile, propFile, labelFile)

print("after breadth first search")

for chain in goodChains:
    print("got chain")
    #print(friend.getID())
    #print(len(friend.properties))
    for tup in chain:
        element = tup[0]
        if isinstance(element, Node):
            print("NODE:")
            for prop in element.properties:
                print("key: {0}".format(prop.key))
                print("value: {0}".format(prop.value))

        else:
            print("REL:")
            print(element.getRelType())
