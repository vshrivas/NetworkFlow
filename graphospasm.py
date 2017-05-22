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

        # Get the "create_dict", which represents what needs to be created
        # given the query that just occurred.
        create_dict = cyp.parse(query)

        # One invariant on create_dict that we shall use is that if the query
        # needed relationships to be created, those relationships reference only
        # nodes that are also in the create_dict in the "nodes" section.
        # Maybe this sentiment is better demonstrated than stated.

        # An interesting note. Nodes reference the relationships they are a
        # part of, and relationships reference the two nodes they connect.
        # We must create the nodes in an incomplete form, then create the
        # relationships that refer to them, then fill in the rest of the info
        # associated with the nodes to have them know their relationships.

        # We'll need to keep track of this mapping to do what the previous
        # paragraph just said.
        simpleNodeToNode = {}
        for simpleNode in create_dict["create_nodes"]:
            node = s.createNode()
            print(" * Creating node %s; has ID %d" % (simpleNode.varName, node.nodeID))

            for label in simpleNode.labels:
                print(" * Adding label %s to node %s" % (label, simpleNode.varName))
                node.addLabel(s.createLabel(label))
            for prop_key, prop_val in simpleNode.properties.items():
                print(" * Adding property {%s: %s} to node %s" % (prop_key, prop_val, simpleNode.varName))
                node.addProperty(s.createProperty(prop_key, prop_val))

            # This node isn't done yet. We still need to add its relationships!
            # To be continued...
            simpleNodeToNode[simpleNode] = node

        # OK, we have semi-filled-in nodes for each node, but we need to make
        # the relationships now...
        nodesToRelationships = {}
        for relationship in create_dict["create_relationships"]:
            print(" * Creating relationship %s" % relationship.label)
            print("   * It connects nodes %s and %s" % (relationship.node1.varName,
                                                    relationship.node2.varName))
            node1 = simpleNodeToNode[relationship.node1]
            node2 = simpleNodeToNode[relationship.node2]
            rel = s.createRelationship(node1, node2)

            # Cool! We can add this relationship to the nodes.
            node1.addRelationship(rel)
            node2.addRelationship(rel)

        # The nodes should be written back to disk now. They're done.
        for node in simpleNodeToNode.values():
            print(" * Writing node with ID %d back to disk" % node.nodeID)
            node.writeNode()

