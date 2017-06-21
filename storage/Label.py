import sys

DEBUG = False

class Label:

    """Label class: representation of a label, which stores a string label for 
    nodes or relationships.

    Storage: Labels are stored as fixed size records which are 106 bytes in
    length. This fixed size storage format makes looking up specific labels.
    in the database faster as to look up a label, only the label ID is needed. 
    The ID of the next label of the associated node or relationship is stored so 
    that labels can be traversed in a linked list fashion when reading nodes or 
    relationships.

    Storage
    Bytes 1-3: Label ID
    Bytes 4-103: Label
    Bytes 104-106: Next Label ID
    """

    # byte offsets from start of label
    LABEL_ID_OFFSET = 0
    LABEL_OFFSET = 3
    NEXT_LABEL_ID_OFFSET = 103
    MAX_LABEL_SIZE = 100

    labelIDByteLen = 3
    storageSize = 106
    # number of labels ever created (used for auto-incrementing the label ID)
    numLabels = 0

    def __init__(self, label, labelFile, labelID=None, nextLabelID=-1):
        """Constructor for Labels. Initializes a Label using the given label string and  
        writes it to the specified labelFile (a LabelFile object that represents a
        file storing Labels) based on the specified labelID. The next label ID is 
        also set to nextLabelID.

        Arguments:
        label: the label string of the Label
        labelFile: the LabelFile object that represents the file storing Labels 
        labelID: the ID of the Label to be initialized; default labelID of None 
        means the Label will be assigned an auto-incrementing label ID
        nextLabelID: the ID of the next label; default -1 for no next label
        """

        Label.numLabels = labelFile.getNumLabels()
        if DEBUG:
            print("**** Num Labels = {0} *****".format(Label.numLabels))
        
        # if labelID is None, use auto-incrementing for label ID
        if labelID is None:
            labelID = Label.numLabels

        self.labelID = labelID

        # increment number of labels when new label created
        if self.labelID != -1 and self.labelID >= Label.numLabels:
            Label.numLabels += 1

        # set label string
        self.label = label

        # label is not of max size
        if(sys.getsizeof(self.label) != self.MAX_LABEL_SIZE):
            # pad label string up to max size
            while len(self.label.encode('utf-8')) != self.MAX_LABEL_SIZE:
                self.label += ' '

        # set labelFile for label
        self.labelFile = labelFile

        # open label file
        storeFileName = self.labelFile.getFileName()
        storeFile = open(storeFileName, 'r+b')

        # write number of labels to first 3 bytes of label file
        storeFile.write((self.numLabels).to_bytes(Label.labelIDByteLen,
            byteorder = sys.byteorder, signed=True))

        # set starting offset for label in label file
        self.startOffset = self.labelID * Label.storageSize + Label.labelIDByteLen

        # set next label ID
        self.nextLabelID = nextLabelID

    def getLabelStr(self):
        """Return label string of label."""
        return self.label
        
    def getLabelID(self):
        """Return label ID of label.""" 
        return self.labelID

    def setNextLabelID(self, nextLabelID):
        """Set next label ID of label."""
        self.nextLabelID = nextLabelID

    def writeLabel(self, nextLabelID):
        """Write label to disk using specified next label ID."""
        # open label file
        storeFileName = self.labelFile.getFileName()
        storeFile = open(storeFileName, 'r+b')

        # seek to location for label and write label ID
        storeFile.seek(self.startOffset)
        storeFile.write(self.labelID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))

        # write label
        storeFile.seek(self.startOffset + Label.LABEL_OFFSET)
        # label is not of max size
        if(sys.getsizeof(self.label) != self.MAX_LABEL_SIZE):
            # pad label string up to max size
            while len(self.label.encode('utf-8')) != self.MAX_LABEL_SIZE:
                self.label += ' '
        storeFile.write(bytearray(self.label, "utf8"))

        # write next label's ID
        storeFile.seek(self.startOffset + Label.NEXT_LABEL_ID_OFFSET)

        if DEBUG:
            print("writing next label id: {0}".format(nextLabelID))
        storeFile.write(nextLabelID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))


        
