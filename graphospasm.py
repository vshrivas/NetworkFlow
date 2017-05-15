import parse.Cypher as cyp
from parse.SimpleTypes import *

import storage.StorageManager as sm
import storage.LabelFile as lf
import storage.NodeFile as nf
import storage.PropertyFile as pf
import storage.RelationshipFile as rf
from storage.Node import Node

if __name__ == '__main__':
    print("Welcome to graphospasm.")
    print("Version -112.")
    print("Enjoy your stay.")

    n = nf.NodeFile()
    r = rf.RelationshipFile()
    p = pf.PropertyFile()
    l = lf.LabelFile()
    s = sm.StorageManager(n, r, p, l)

    while True:
        print(">", end=" ")
        query = input()
        create_dict = cyp.parse(query)

        for relationship in create_dict["relationships"]:
            # TODO.
            s.createRelationship(relationship)

        for simpleNode in create_dict["nodes"]:
            print(" * Creating node %s" % simpleNode.varName)
            node = s.createNode()

            # TODO: relationship
            for label in simpleNode.labels:
                print(" * Adding label %s to node %s" % (label, simpleNode.varName))
                node.addLabel(s.createLabel(label))
            print(" * here it is: %s" % simpleNode.properties)
            for prop_key, prop_val in simpleNode.properties.items():
                print(" * Adding property {%s: %s} to node %s" % (prop_key, prop_val, simpleNode.varName))
                node.addProperty(s.createProperty(prop_key, prop_val))

            node.writeNode()