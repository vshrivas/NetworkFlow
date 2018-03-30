class LabelStorageManager():
    def readLabel(self, labelID):
        pageID = labelID[0]
        labelIndex = labelID[1]

        pageIndex = pageID[1]

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        labelPage = BufferManager.getLabelPage(pageIndex, self)
        return labelPage.readLabel(labelIndex)

    def writeLabel(label):
        labelID = label.getID()
        pageID = labelID[0]           # pageID[0] = 0, pageID[1] = pageIndex

        pageIndex = pageID[1]        # which page node is in, page IDs are unique across all files

        labelPage = BufferManager.getLabelPage(pageIndex, self)

        labelPage.writeLabel(label)

    def getLabelChain(firstLabelID):
        nextLabelID = firstLabelID

        chainedLabels = []
        
        # while there is a next property for the relationship
        while nextLabelID != -1:
            label = readLabel(nextLabelID)
            chainedLabels.append(label)

            nextLabelID = label.nextLabelID

        return chainedLabels

    '''def writeLabels(self, labels):
        # write labels to label file
        for labelIndex in range(0, len(labels)):
            label = labels[labelIndex]
            if DEBUG:
                print("writing {0} label ".format(label.getLabelID()))

            # case of last label
            if labelIndex == len(labels) - 1:
                if DEBUG:
                    print("no next label")
                # set next label's id to -1
                nextLabelID = -1
            # case of any other label
            else:
                nextLabelID = (labels[labelIndex + 1]).getLabelID()
            # write label
            label.writeLabel(nextLabelID)'''