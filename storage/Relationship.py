from .Property import Property
import sys

DEBUG = False

class Relationship:

    """Relationship class: representation of a relationship connecting two different 
    Nodes. Relationships have a type (a string) and properties (key-value pairs) that specify 
    information about relationships. Relationships serve as the edges of the graph 
    representation of a graph database.


    Storage: Relationships are stored as fixed size records which are 130 bytes in
    length. This fixed size storage format makes looking up specific relationships
    in the database faster as to look up a Relationship, only the relationship ID is needed. 
    For convenience of traversing through the relationships of the nodes in a relationship, 
    the previous and next relationship IDs are included for both nodes in a relationship.
    Since every property stores the ID of the next property, the relationship only needs to store 
    the ID of the first property for the relationship.

    Bytes 1-4: Relationship ID
    Bytes 5-7: Node 1 ID
    Bytes 8-10: Node 2 ID 
    Bytes 11-14: Node 1 Next Rel ID
    Bytes 15-18: Node 1 Prev Rel ID
    Bytes 19-22: Node 2 Next Rel ID
    Bytes 23-26: Node 2 Prev Rel ID
    Bytes 27-126: Relationship Type
    Bytes 127-130: ID of first property for relationship

    Bidirectionality:
    If relationship with node 1 = A and node 2 = B exists, a relationship with 
    node 1 = B and node 2 = A should also exist.
    """

    # byte offsets from start of relationship
    RELATIONSHIP_ID_OFFSET = 0
    NODE1_ID_OFFSET = 4
    NODE2_ID_OFFSET = 7
    NODE1_NEXT_REL_ID_OFFSET = 10
    NODE1_PREV_REL_ID_OFFSET = 14
    NODE2_NEXT_REL_ID_OFFSET = 18
    NODE2_PREV_REL_ID_OFFSET = 22
    RELATIONSHIP_TYPE_OFFSET = 26
    PROPERTY_ID_OFFSET = 126

    MAX_TYPE_SIZE = 100

    # number of relationships ever created (used for auto-incrementing the relationship ID)
    storageSize = 130
    numRelationships = 0

    relIDByteLen = 4

    def __init__(self, node1ID, node2ID, relType, relationshipFile, relationshipID=None):
        """Constructor for Relationship, which sets the first node ID and second node ID 
        of the relationship, the relationship type, the file the relationship is stored in, 
        and the relationship ID.

        Arguments:
        node1ID: the ID of the first node in the relationship
        node2ID: the ID of the second node in the relationship
        relType: the type of the relationship 
        relationshipFile: the RelationshipFile object that represents the file storing Relationships
        relationshipID: the ID of the Relationship to be initialized; default relationshipID of None 
        means the Relationship will be assigned an auto-incrementing relationship ID
        """
        # If relationshipFile object passed exists, get number of relationships 
        if relationshipFile != "":
            Relationship.numRelationships = relationshipFile.getNumRelationships()

        if DEBUG:
            print("**** Num Relationships = {0} *****".format(Relationship.numRelationships))

        # if relationshipID is None, use auto-incrementing for relationship ID
        if relationshipID is None:
            relationshipID = Relationship.numRelationships

        # set first and second node IDs
        self.firstNodeID = node1ID
        self.secondNodeID = node2ID

        # set relationship type
        self.type = relType 

        self.properties = []

        # set relationship ID
        self.relationshipID = relationshipID

        # increment number of relationships when new relationship created
        if relationshipID != -1 and relationshipID >= Relationship.numRelationships:
            Relationship.numRelationships += 1

        # set relationship file
        self.relationshipFile = relationshipFile

        if relationshipFile != "":
            # open relationship file
            storeFilePath = self.relationshipFile.getFilePath()
            storeFile = open(storeFilePath, 'r+b')

            # write number of relationships to first 4 bytes of relationship file
            storeFile.write((self.numRelationships).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))

        # set starting offset of relationship in relationship file
        self.startOffset = self.relationshipID * Relationship.storageSize + Relationship.relIDByteLen

    def getID(self):
        """Return relationship ID of relationship."""
        return self.relationshipID 

    def getFirstNodeID(self):
        """Return first node ID of relationship."""
        return self.firstNodeID

    def getSecondNodeID(self):
        """Return second node ID of relationship."""
        return self.secondNodeID
    
    def getOtherNodeID(self, nodeID):
        """Return ID of other node of relationship given node ID of one of the nodes."""
        if(nodeID == self.firstNodeID):
            return self.secondNodeID

        return self.firstNodeID

    def getRelType(self):
        """Return type of relationship."""
        return self.type

    def addProperty(self, prop):
        """Add property to relationship."""
        self.properties.append(prop)

    def getProperties(self):
        """Return properties of relationship."""
        return self.properties

    def writeRelationship(self, node, prevRel, nextRel):
        """Write relationship to relationship file for specified node and relationship's 
        properties to property file.

        Arguments:
        node: node relationship being written for
        prevRel: previous relationship for specified node
        nextRel: next relationship for specified node
        """
        # open relationship file
        if DEBUG:
            print(self.relationshipFile)
        storeFilePath = self.relationshipFile.getFilePath()
        storeFile = open(storeFilePath, 'r+b')

        # seek to location for relationship
        storeFile.seek(self.startOffset)

        # write relationship ID
        storeFile.write(self.relationshipID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))
        if DEBUG:
            print("wrote relationship id")

        # write node 1 id
        storeFile.seek(self.startOffset + Relationship.NODE1_ID_OFFSET)
        storeFile.write(self.firstNodeID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))
        if DEBUG:
            print("wrote first node id")

        # write node 2 id
        storeFile.seek(self.startOffset + Relationship.NODE2_ID_OFFSET)
        storeFile.write(self.secondNodeID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))
        if DEBUG:
            print("wrote second node id")

        # find which node relationship is being written for and write next and previous 
        # relationship IDs appropriately
        if node.getID() == self.firstNodeID:
            if DEBUG:
                print("writing relationship for first node")

            storeFile.seek(self.startOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
            storeFile.write(nextRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed=True))

            storeFile.seek(self.startOffset + Relationship.NODE1_PREV_REL_ID_OFFSET)
            storeFile.write(prevRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed=True))

        else:
            if DEBUG:
                print("writing relationship for second node")
            storeFile.seek(self.startOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
            storeFile.write(nextRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed = True))

            storeFile.seek(self.startOffset + Relationship.NODE2_PREV_REL_ID_OFFSET)
            storeFile.write(prevRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed = True))

        # write relationship type
        if DEBUG:
            print("writing relationship type")
        storeFile.seek(self.startOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)

        # type is not of max size
        if(sys.getsizeof(self.type) != self.MAX_TYPE_SIZE):
            # pad relationship type string up to max size
            while len(self.type.encode('utf-8')) != self.MAX_TYPE_SIZE:
                self.type += ' '

        storeFile.write(bytearray(self.type, 'utf8'))
        # strip out additional whitespace used for padding from type
        self.type = self.type.rstrip(' ')

        # write first property ID
        storeFile.seek(self.startOffset + Relationship.PROPERTY_ID_OFFSET)

        # if no properties write -1 for first ID
        if len(self.properties) == 0:
            firstProp = -1
            storeFile.write((-1).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first property ID: -1")
        # otherwise write id of first property
        else:
            firstProp = self.properties[0]
            storeFile.write(firstProp.getID().to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first property ID: {0}". format(firstProp.getID()))


        # write properties to property file
        if DEBUG:
            print("writing properties to property file ...")

        # write properties to property file
        for propIndex in range(0, len(self.properties)):
            prop = self.properties[propIndex]
            if DEBUG:
                print("writing {0} property ".format(prop.getID()))

            # case of no next property
            if propIndex == len(self.properties) - 1:
                if DEBUG:
                    print("no next property")
                # A placeholder property since there is no next property
                nullProperty = Property("", "", "", -1)
                prop.writeProperty(nullProperty)
            # case of next property
            else:
                prop.writeProperty(self.properties[propIndex + 1])

    





