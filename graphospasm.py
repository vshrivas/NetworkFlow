import parse.Cypher as cyp

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

    while True:
        print(">", end=" ")
        query = input()
        create_dict = cyp.parse(query)

        n = nf.NodeFile()
        r = rf.RelationshipFile()
        p = pf.PropertyFile()
        l = lf.LabelFile()
        s = sm.StorageManager(n, r, p, l)

        for node_name in create_dict:
            node = s.createNode()
            for prop_key, prop_val in create_dict[node_name].items():
                node.addProperty(s.createProperty(prop_key, prop_val))
