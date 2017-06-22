import parse.Cypher as cyp
from parse.SimpleTypes import *

import storage.StorageManager as sm
import storage.LabelFile as lf
import storage.NodeFile as nf
import storage.PropertyFile as pf
import storage.RelationshipFile as rf
from storage.Node import Node
from storage.Label import Label
from storage.Relationship import Relationship
from storage.Property import Property
import queryeval.degreeQueries as qeval
from output.printing import printAllResults

import os
from subprocess import run

if __name__ == '__main__':
    print("Welcome to graphospasm.")
    print("Version -112.")
    print("Enjoy your stay.")
    print("Type 'EXIT' to turn me off.")
    
    dataDirectory = "datafiles"
    if not os.path.exists(dataDirectory):
        os.mkdir(dataDirectory)

    n = nf.NodeFile()
    r = rf.RelationshipFile()
    p = pf.PropertyFile()
    l = lf.LabelFile()
    s = sm.StorageManager(n, r, p, l)

    while True:
        print(">", end=" ")
        query = input()

        # Check if we want to leave.
        if query.lower() == 'exit':
            break

        # Check if we want to clean out the database.
        if query.lower() == 'clean':
            print('Are you sure you want to delete all data? (Y/n)')
            answer = input('> ')
            if answer.lower() != 'n':
                run('rm datafiles/*', shell=True)
                print('Data cleaned out.')
                nf.NodeFile.numFiles = 0
                rf.RelationshipFile.numFiles = 0
                pf.PropertyFile.numFiles = 0
                lf.LabelFile.numFiles = 0
                n = nf.NodeFile()
                r = rf.RelationshipFile()
                p = pf.PropertyFile()
                l = lf.LabelFile()
                s = sm.StorageManager(n, r, p, l)
            continue


        # Get the "query_dict", which represents what needs to be created
        # given the query that just occurred.
        query_dict = cyp.parse(query)

        # One invariant on query_dict that we shall use is that if the query
        # needed relationships to be created, those relationships reference only
        # nodes that are also in the query_dict in the "nodes" section.
        # Maybe this sentiment is better demonstrated than stated.

        # An interesting note. Nodes reference the relationships they are a
        # part of, and relationships reference the two nodes they connect.
        # We must create the nodes in an incomplete form, then create the
        # relationships that refer to them, then fill in the rest of the info
        # associated with the nodes to have them know their relationships.
        # We endearingly call this method "crabbing". (\/) o,,o (\/)

        # We'll need to keep track of this mapping to do what the previous
        # paragraph just said.
        simpleNodeToNode = {}
        for simpleNode in query_dict["create_nodes"]:
            node = s.createNode()
            print(" * Creating node %s; has ID %d" % (simpleNode.varname, node.nodeID))

            for label in simpleNode.labels:
                print(" * Adding label %s to node %s" % (label, simpleNode.varname))
                node.addLabel(s.createLabel(label))
            for prop_key, prop_val in simpleNode.properties.items():
                print(" * Adding property {%s: %s} to node %s" % (prop_key, prop_val, simpleNode.varname))
                node.addProperty(s.createProperty(prop_key, prop_val))

            # This node isn't done yet. We still need to add its relationships!
            # To be continued...
            simpleNodeToNode[simpleNode] = node

        # OK, we have semi-filled-in nodes for each node, but we need to make
        # the relationships now...
        nodesToRelationships = {}
        for relationship in query_dict["create_relationships"]:
            print(" * Creating relationship %s" % relationship.label)
            print("   * It connects nodes %s and %s" % (relationship.node1.varname,
                                                    relationship.node2.varname))
            node1 = simpleNodeToNode[relationship.node1]
            node2 = simpleNodeToNode[relationship.node2]
            # TODO: We're only able to give one label to each relationship at
            # the moment :(
            rel = s.createRelationship(node1, node2, relationship.label[0])

            # Cool! We can add this relationship to the nodes.
            node1.addRelationship(rel)
            node2.addRelationship(rel)

        # The nodes should be written back to disk now. They're done.
        for node in simpleNodeToNode.values():
            print(" * Writing node with ID %d back to disk" % node.nodeID)
            node.writeNode()

        # Maybe creation needed to occur, maybe not. If it did, it's done.
        # However, there is still more to do. Perhaps we need to match, and then
        # return, some patterns in the database. This will require some query
        # evaluation.
        results = None
        tried_to_match = False
        if query_dict["match_nodes"]:
            # Perform a breadth-first-search on the database with the given
            # patterns to evaluate.
            # TODO: we only handle one match at a time, i.e. only things that
            # look like (n) -[]-> (m) -[]-> ...
            # rather than (n) -[]-> (m), (p) -[]-> (q), ...
            # Once we fix this, this call to this function will become more
            # complicated, likely a loop.
            results = qeval.breadthFirstSearch(query_dict["match_nodes"],
                query_dict["match_relationships"], n, r, p, l)
            tried_to_match = True

        if query_dict["return_exprs"]:
            # Unfortunately, those results don't necessarily match with what
            # we need to print to the screen, which is something dictated
            # by RETURN statements. RETURN statements can involve variable
            # names, as well as completely-unrelated expressions (like 1 + 1),
            # as well as column names to give these things. We need to breathe
            # meaning into our "results".
            #
            # This is done in printing.
            printAllResults(results, query_dict["match_nodes"],
                query_dict["match_relationships"],  query_dict["return_exprs"],
                tried_to_match)
