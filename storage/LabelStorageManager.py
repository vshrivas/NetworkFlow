class LabelStorageManager(StorageManager):
	def writeLabels(labels):
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
            label.writeLabel(nextLabelID) 