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
    
        self.labelID = labelID

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
        storeFilePath = self.labelFile.getFilePath()
        storeFile = open(storeFilePath, 'r+b')

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


        
