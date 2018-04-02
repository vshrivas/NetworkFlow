from .LabelFile import LabelFile
from .LockManager import LockManager
import threading

''' LabelStorageManager is responsible for handling the top level methods for creating, reading,
and writing of labels. Creates new label pages and files when necessary. Has a meta data file
to keep track of number of label files. '''
class LabelStorageManager():
    numLabelFiles = 0
    directory = "labelstore"

    DEBUG = False

    def __init__(self):
        # open label storage meta data file
        # read number of label files 
        self.fileName = "metadata"
        self.filePath = os.path.join(NodeStorageManager.directory, self.fileName)

        # storage manager metadata file exists
        if os.path.exists(self.filePath):
            metadataFile = open(self.filePath, 'r+b')
            LabelStorageManager.numLabelFiles = int.from_bytes(metadataFile.read(Label.labelIDByteLen), sys.byteorder, signed=True)

        # storage manager metadata file does not exist
        else:
            # label store directory does not exist, make it
            if not os.path.exists(self.directory):
                os.makedirs(LabelStorageManager.directory)

            # open metadata file    
            metadataFile = open(self.filePath, 'wb')
            # write number of label files
            metadataFile.write((0).to_bytes(Label.labelIDByteLen,
                byteorder = sys.byteorder, signed=True))

        # there are no label files
        if LabelStorageManager.numLabelFiles == 0:
            # make a new one 
            LabelFile(0)
            LabelStorageManager.numLabelFiles += 1

            metadataFile = open(self.filePath, 'r+b')
            metadataFile.write((LabelStorageManager.numNodeFiles).to_bytes(Label.labelIDByteLen,
                byteorder = sys.byteorder, signed=True))

    # takes in labelID, returns corresponding label from DB
    def readLabel(labelID):
        pageID = labelID[0]
        labelIndex = labelID[1]

        pageIndex = pageID[1]

        fileID = int(pageIndex / LabelFile.MAX_PAGES)

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        labelPage = BufferManager.getLabelPage(pageIndex, LabelFile(fileID))

        # check for potential deadlock
        threading.currentThread().waiting = labelPage
        if LockManager.detectRWDeadlock(threading.currentThread(), threading.currentThread()):
            raise Exception('Deadlock detected!')

        # acquire read lock
        labelPage.pageLock.acquire_read()
        threading.currentThread().waiting = None
        LockManager.makePageOwner(threading.currentThread(), labelPage)

        label = labelPage.readLabel(labelIndex)

        # release read lock
        labelPage.pageLock.release_read()
        LockManager.removePageOwner(threading.currentThread(), labelPage)
        return label

    # takes in label to either create or write, returns same label
    def writeLabel(label, create):
        labelID = label.getID()
        pageID = labelID[0]           # pageID[0] = 0, pageID[1] = pageIndex

        pageIndex = pageID[1]        

        fileID = int(pageIndex / LabelFile.MAX_PAGES)

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        labelPage = BufferManager.getLabelPage(pageIndex, LabelFile(fileID))

        # detect potential deadlock
        threading.currentThread().waiting = labelPage
        if LockManager.detectRWDeadlock(threading.currentThread(), threading.currentThread()):
            raise Exception('Deadlock detected!')

        # acquire write lock
        labelPage.pageLock.acquire_write()
        threading.currentThread().waiting = None
        LockManager.makePageOwner(threading.currentThread(), labelPage)

        labelPage.writeLabel(label, create)

        # release lock
        labelPage.pageLock.release_write()
        LockManager.removePageOwner(threading.currentThread(), labelPage)
        return label

    # get chain of labels based on first label ID
    def getLabelChain(firstLabelID):
        nextLabelID = firstLabelID

        chainedLabels = []
        
        # while there is a next label
        while nextLabelID[1] != -1:
            label = LabelStorageManager.readLabel(nextLabelID)
            chainedLabels.append(label)

            nextLabelID = label.nextLabelID

        return chainedLabels

    # creates a label based on key and value
    def createLabel(key, value):
        # get label file
        lastFileID = LabelStorageManager.numlabelFiles - 1
        lastFile = LabelFile(lastFileID)

        if lastFile.numPages == 0:
            lastFile.createPage()

        # get last label page
        lastPage = BufferManager.getLabelPage(lastFile.numPages - 1, lastFile)
        
        propPage = lastPage
        propFile = lastFile

        # if last page is full
        if lastPage.numEntries == DataPage.MAX_PAGE_ENTRIES:
            # if file is at max pages
            if lastFile.numPages == LabelFile.MAX_PAGES:
                # make a new file
                newLastFile = LabelFile(lastFileID + 1)
                LabelStorageManager.numLabelFiles += 1

                metadataFile = open(self.filePath, 'r+b')
                metadataFile.write((LabelStorageManager.numLabelFiles).to_bytes(Label.labelIDByteLen,
                byteorder = sys.byteorder, signed=True))

                labelFile = newLastFile

                # make a new page in the file
                newLastFile.createPage()
                labelPage = BufferManager.getLabelPage(newLastFile.numPages - 1, newLastFile)

            # else make new page
            else:
                lastFile.createPage()
                labelPage = BufferManager.getLabelPage(lastFile.numPages - 1, lastFile)

        # create label object
        labelID = [[3, labelPage.pageID[1]], labelPage.numEntries]
        label = Label(labelString, labelFile, labelID, [[3, 0], -1])
        
        print('creating label {0} in page {1}'.format(labelPage.numEntries, labelPage.pageID[1]))

        LabelStorageManager.writeLabel(label, True)

        return label