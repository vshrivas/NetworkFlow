from DataPage import DataPage
from Relationship import Relationship
from Node import Node
from Property import Property
import sys, struct, os

class RelationshipPage(DataPage):
    PAGES_OFFSET = 100

    def __init__(self, pageIndex, datafile, create):
        # 1 indicates that this is a relationship page
        pageID = [1, pageIndex]
        super().__init__(pageID, datafile)

        self.pageStart = self.getPageIndex() * (self.MAX_PAGE_ENTRIES * Relationship.storageSize + DataPage.DATA_OFFSET) + self.PAGES_OFFSET

        self.relationshipData = []  # list of relationship objects the page contains
        
        if create == False:
        # read in all page data
            self.readPageData()
        else:
            self.writePageData()

    # reads in all of the relationship objects stored in this page
    # stores them in self.relationshipData
    def readPageData(self):
        print('reading rel page data...')
        # open relationship file
        filePath = (self.file).getFilePath()
        relationshipFile = open(filePath, 'rb')

        # read in number of entries
        relationshipFile.seek(self.pageStart + DataPage.NUM_ENTRIES_OFFSET)
        self.numEntries = int.from_bytes(relationshipFile.read(DataPage.NUM_ENTRIES_SIZE), sys.byteorder, signed=True)

        # read in owner of page
        relationshipFile.seek(self.pageStart + DataPage.OWNER_ID_OFFSET)
        self.ownerID = int.from_bytes(relationshipFile.read(DataPage.OWNER_ID_SIZE), sys.byteorder, signed=True)

        # read in all data items
        for relationshipIndex in range(0, self.numEntries):
            print('reading rel {0}'.format(relationshipIndex))
            relationship = self.readRelationshipData(relationshipIndex)
            self.relationshipData.append(relationship)

    # returns relationship from relationshipIndex
    # used while reading in page data
    def readRelationshipData(self, relationshipIndex):
        # open relationship file
        filePath = (self.file).getFilePath()
        relationshipStore = open(filePath, 'rb')

        # offset from start of file to start of node
        relationshipStartOffset = self.pageStart + DataPage.DATA_OFFSET + relationshipIndex * Relationship.storageSize

        # find ID of relationship, technically should be index
        relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_ID_OFFSET)
        absRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)
        relPageIndex = int(absRelID / DataPage.MAX_PAGE_ENTRIES)
        relIndex = int((absRelID / DataPage.MAX_PAGE_ENTRIES - relPageIndex) * DataPage.MAX_PAGE_ENTRIES)
        relID = [[1, relPageIndex], relIndex]

        # find ID of first node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_ID_OFFSET)
        absNode1ID = int.from_bytes(relationshipStore.read(Node.nodeIDByteLen), sys.byteorder, signed=True)
        node1PageIndex = int(absNode1ID / DataPage.MAX_PAGE_ENTRIES)
        node1Index = int((absNode1ID / DataPage.MAX_PAGE_ENTRIES - node1PageIndex) * DataPage.MAX_PAGE_ENTRIES)
        node1ID = [[0, node1PageIndex], node1Index]

        # find ID of second node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_ID_OFFSET)
        absNode2ID = int.from_bytes(relationshipStore.read(Node.nodeIDByteLen), sys.byteorder, signed=True)
        node2PageIndex = int(absNode2ID / DataPage.MAX_PAGE_ENTRIES)
        node2Index = int((absNode2ID / DataPage.MAX_PAGE_ENTRIES - node2PageIndex) * DataPage.MAX_PAGE_ENTRIES)
        node2ID = [[0, node2PageIndex], node2Index]

        # find ID of next rel for node1 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
        absNode1NextRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)
        if absNode1NextRelID == -1:
            node1NextRelID = [[1, 0], -1]
        else:
            node1NextRelPageIndex = int(absNode1NextRelID / DataPage.MAX_PAGE_ENTRIES)
            node1NextRelIndex = int((absNode1NextRelID  / DataPage.MAX_PAGE_ENTRIES - node1NextRelPageIndex) * DataPage.MAX_PAGE_ENTRIES)
            node1NextRelID = [[1, node1NextRelPageIndex], node1NextRelIndex]

        # find ID of prev rel for node1 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_PREV_REL_ID_OFFSET)
        absNode1PrevRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)
        if absNode1PrevRelID == -1:
            node1PrevRelID = [[1, 0], -1]
        else:
            node1PrevRelPageIndex = int(absNode1PrevRelID / DataPage.MAX_PAGE_ENTRIES)
            node1PrevRelIndex = int((absNode1PrevRelID  / DataPage.MAX_PAGE_ENTRIES - node1PrevRelPageIndex) * DataPage.MAX_PAGE_ENTRIES)
            node1PrevRelID = [[1, node1PrevRelPageIndex], node1PrevRelIndex]

        # find ID of next rel for node2 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
        absNode2NextRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)
        if absNode2NextRelID == -1:
            node2NextRelID = [[1, 0], -1]
        else:
            node2NextRelPageIndex = int(absNode2NextRelID / DataPage.MAX_PAGE_ENTRIES)
            node2NextRelIndex = int((absNode2NextRelID  / DataPage.MAX_PAGE_ENTRIES - node2NextRelPageIndex) * DataPage.MAX_PAGE_ENTRIES)
            node2NextRelID = [[1, node2NextRelPageIndex], node2NextRelIndex]

        # find ID of prev rel for node2 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_PREV_REL_ID_OFFSET)
        absNode2PrevRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)
        if absNode2PrevRelID == -1:
            node2PrevRelID = [[1, 0], -1]
        else:
            node2PrevRelPageIndex = int(absNode2PrevRelID / DataPage.MAX_PAGE_ENTRIES)
            node2PrevRelIndex = int((absNode2PrevRelID  / DataPage.MAX_PAGE_ENTRIES - node2PrevRelPageIndex) * DataPage.MAX_PAGE_ENTRIES)
            node2PrevRelID = [[1, node2PrevRelPageIndex], node2PrevRelIndex]

        # read in type of relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)
        relType = relationshipStore.read(Relationship.MAX_TYPE_SIZE).decode("utf-8")
        relType = relType.rstrip(' ')

        print('read {0} type for rel'.format(relType))

        relationshipStore.seek(relationshipStartOffset + Relationship.PROPERTY_ID_OFFSET)
        absPropertyID = int.from_bytes(relationshipStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
        absPropertyPageIndex = int(absPropertyID / DataPage.MAX_PAGE_ENTRIES)
        absPropertyIndex = int((absPropertyID  / DataPage.MAX_PAGE_ENTRIES - absPropertyPageIndex) * DataPage.MAX_PAGE_ENTRIES)
        propertyID = [[2,absPropertyPageIndex], absPropertyIndex]

        # create relationship and add to node
        rel = Relationship(relID, node1ID, node2ID, node1NextRelID, node1PrevRelID,
                node2NextRelID, node2PrevRelID, relType, propertyID, self.file)

        return rel

    def readRelationship(self, relationshipIndex):
        return self.relationshipData[relationshipIndex]

    def writeRelationship(self, rel, create):
        relID = rel.getID()

        relIndex = relID[1]

        if create:
            self.relationshipData.append(rel)
        else:
            self.relationshipData[relIndex] = rel

        self.writePageData()

    def writePageData(self):
        print('writing rel page data...')
        filePath = (self.file).getFilePath()
        relFile = open(filePath, 'r+b')

        # write number of entries
        relFile.seek(self.pageStart + DataPage.NUM_ENTRIES_OFFSET)
        relFile.write((self.numEntries).to_bytes(DataPage.NUM_ENTRIES_SIZE,
            byteorder = sys.byteorder, signed=True))

        # write owner ID
        relFile.seek(self.pageStart + DataPage.OWNER_ID_OFFSET)
        relFile.write((self.ownerID).to_bytes(DataPage.OWNER_ID_SIZE,
            byteorder = sys.byteorder, signed=True))

        for rel in self.relationshipData:
            print('writing data for rel {0}'.format(rel.getID()[1]))
            self.writeRelationshipData(rel, relFile)

    def writeRelationshipData(self, rel, relationshipStore):
        relationshipIndex = rel.getID()[1]

        # offset from start of file to start of node
        relationshipStartOffset = self.pageStart + DataPage.DATA_OFFSET + relationshipIndex * Relationship.storageSize

        # write ID of relationship, technically should be index
        relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_ID_OFFSET)
        absRelID = self.getPageIndex() * DataPage.MAX_PAGE_ENTRIES + relationshipIndex
        relationshipStore.write(absRelID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of first node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_ID_OFFSET)
        absFirstNodeID = rel.firstNodeID[0][1] * DataPage.MAX_PAGE_ENTRIES + rel.firstNodeID[1]
        relationshipStore.write(absFirstNodeID.to_bytes(Node.nodeIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of second node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_ID_OFFSET)
        absSecondNodeID = rel.secondNodeID[0][1] * DataPage.MAX_PAGE_ENTRIES + rel.secondNodeID[1]
        relationshipStore.write(absSecondNodeID.to_bytes(Node.nodeIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of next rel for node1 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
        if rel.node1NextRelID[1] == -1:
            absNode1NextRelID = -1
        else:
            absNode1NextRelID = rel.node1NextRelID[0][1] * DataPage.MAX_PAGE_ENTRIES + rel.node1NextRelID[1]       
        relationshipStore.write(absNode1NextRelID.to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed=True))   

        # write ID of prev rel for node1 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_PREV_REL_ID_OFFSET)
        if rel.node1PrevRelID[1] == -1:
            absNode1PrevRelID = -1
        else:
            absNode1PrevRelID = rel.node1PrevRelID[0][1] * DataPage.MAX_PAGE_ENTRIES + rel.node1PrevRelID[1]
        relationshipStore.write(absNode1PrevRelID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of next rel for node2 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
        if rel.node2NextRelID[1] == -1:
            absNode2NextRelID = -1
        else:
            absNode2NextRelID = rel.node2NextRelID[0][1] * DataPage.MAX_PAGE_ENTRIES + rel.node2NextRelID[1]
        relationshipStore.write(absNode2NextRelID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of prev rel for node2 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_PREV_REL_ID_OFFSET)
        if rel.node2PrevRelID[1] == -1:
            absNode2PrevRelID = -1
        else:
            absNode2PrevRelID = rel.node2PrevRelID[0][1] * DataPage.MAX_PAGE_ENTRIES + rel.node2PrevRelID[1]
        relationshipStore.write(absNode2PrevRelID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write type of relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)
        print('wrote {0} type for rel'.format(rel.type))

        # type is not of max size
        if(sys.getsizeof(rel.type) != Relationship.MAX_TYPE_SIZE):
            # pad relationship type string up to max size
            while len(rel.type.encode('utf-8')) != Relationship.MAX_TYPE_SIZE:
                rel.type += ' '

        relationshipStore.write(bytearray(rel.type, 'utf8'))

        # strip out additional whitespace used for padding from type
        rel.type = rel.type.rstrip(' ')

        # write first property ID
        print('writing first propertyID {0}'.format(rel.propertyID))
        relationshipStore.seek(relationshipStartOffset + Relationship.PROPERTY_ID_OFFSET)
        absPropID = rel.propertyID[0][1] * DataPage.MAX_PAGE_ENTRIES + rel.propertyID[1]
        relationshipStore.write(rel.propertyID[1].to_bytes(Property.propIDByteLen, 
            byteorder = sys.byteorder, signed=True))


    '''def OLDwriteRelationshipData(self, node, prevRel, nextRel):
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
                prop.writeProperty(self.properties[propIndex + 1])'''
