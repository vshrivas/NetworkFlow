from .Node import Node
from .Property import Property
from .Relationship import Relationship
from .Label import Label
from .DataPage import DataPage
import sys, struct, os

class LabelPage(DataPage):
    PAGES_OFFSET = 100

    def __init__(self, pageIndex, datafile, create):
        # 3 indicates that this is a property page
        pageID = [3, pageIndex]
        super().__init__(pageID, datafile)

        self.labelData = []  # list of label objects the page contains

        self.pageStart = self.getPageIndex() * (self.MAX_PAGE_ENTRIES * Label.storageSize + DataPage.DATA_OFFSET) + self.PAGES_OFFSET
        
        if create == False:
          # read in all page data
            self.readPageData()
        else:
            self.writePageData()

    # reads in all of the label objects stored in this page
    # stores them in self.labelData
    def readPageData(self):
        # open property file
        filePath = (self.file).getFilePath()
        labelFile = open(filePath, 'rb')

        # read in number of entries
        labelFile.seek(self.pageStart + DataPage.NUM_ENTRIES_OFFSET)
        self.numEntries = int.from_bytes(labelFile.read(DataPage.NUM_ENTRIES_SIZE), sys.byteorder, signed=True)

        # read in owner of page
        labelFile.seek(self.pageStart + DataPage.OWNER_ID_OFFSET)
        self.ownerID = int.from_bytes(labelFile.read(DataPage.OWNER_ID_SIZE), sys.byteorder, signed=True)

        # read in all data items
        for labelIndex in range(0, self.numEntries):
            label = self.readLabelData(labelIndex)
            self.labelData.append(label)

    def readLabelData(self, labelID):
        """Reads label corresponding to label ID and returns a label object for label."""
        labelStore = open(self.filePath, 'rb')
        # Starting offset for label 
        labelStartOffset = self.pageStart + self.DATA_OFFSET + labelID * Label.storageSize

        # Read label string
        labelStore.seek(labelStartOffset + Label.LABEL_OFFSET)
        # Remove padding from label string
        labelString = labelStore.read(Label.MAX_LABEL_SIZE).decode('utf8').rstrip(' ')

        # Read next label ID
        labelStore.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
        absNextLabelID = int.from_bytes(labelStore.read(Label.storageSize), byteorder=sys.byteorder, signed=True)
        if absNextLabelID == -1:
            nextLabelID = [[3, 0], -1]
        else:
            labelPageIndex = int(absNextLabelID / DataPage.MAX_PAGE_ENTRIES)
            labelIndex = int(((absNextLabelID / DataPage.MAX_PAGE_ENTRIES) - labelPageIndex) *  DataPage.MAX_PAGE_ENTRIES)
            nextLabelID = [[3, labelPageIndex], labelIndex]

        label = Label(labelString, datafile, labelID, nextLabelID)
        return label


    def readLabel(self, labelIndex):
        return self.labelData[labelIndex]

    def writeLabel(self, label, create):
        labelID = label.getID()

        labelIndex = labelID[1]
        
        if create:
            self.labelData.append(label)
        else:
            self.labelData[labelIndex] = label

        self.writePageData()

    def writePageData(self):
        filePath = (self.file).getFilePath()
        labelFile = open(filePath, 'r+b')

        # write number of entries
        labelFile.seek(self.pageStart + DataPage.NUM_ENTRIES_OFFSET)
        labelFile.write((self.numEntries).to_bytes(DataPage.NUM_ENTRIES_SIZE,
            byteorder = sys.byteorder, signed=True))

        # write owner ID
        labelFile.seek(self.pageStart + DataPage.OWNER_ID_OFFSET)
        labelFile.write((self.ownerID).to_bytes(DataPage.OWNER_ID_SIZE,
            byteorder = sys.byteorder, signed=True))

        for label in labelData:
            self.writeLabelData(label, labelFile)

    def writeLabelData(self, label, storeFile):
        labelIndex = label.getID()[1]
        
        # Starting offset for label 
        labelStartOffset = self.pageStart + DataPage.DATA_OFFSET + labelIndex * Label.storageSize

        # seek to location for label and write label ID
        storeFile.seek(labelStartOffset + Label.LABEL_ID_OFFSET)
        absLabelID = self.getPageIndex() * DataPage.MAX_PAGE_ENTRIES + label.labelID[1]
        storeFile.write(self.absLabelID.to_bytes(Label.labelIDByteLen, byteorder = sys.byteorder, signed=True))

        # write label
        storeFile.seek(labelStartOffset + Label.LABEL_OFFSET)
        # label is not of max size
        if(sys.getsizeof(label.label) != Label.MAX_LABEL_SIZE):
            # pad label string up to max size
            while len(label.label.encode('utf-8')) != Label.MAX_LABEL_SIZE:
                label.label += ' '
        storeFile.write(bytearray(label.label, "utf8"))

        # write next label's ID
        storeFile.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
        if label.nextLabelID[1] == -1:
            absNextLabelID = -1
        else:
            absNextLabelID = label.nextLabelID[0][1] * DataPage.MAX_PAGE_ENTRIES + label.nextLabelID[1]
        storeFile.write(nextLabelID.to_bytes(Label.labelIDByteLen, byteorder = sys.byteorder, signed=True))