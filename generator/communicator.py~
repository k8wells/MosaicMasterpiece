import os
import sys
import tempfile
path = os.path.abspath(__file__)
sys.path.append(os.path.join(os.path.dirname(path), "../"))
import utils2

class Communicator(object):
    def __init__(self):
        try:
            os.mkfifo('cppToPy', 0666);
        except OSError, e:
            pass
        try:
            os.mkfifo('pyToCpp', 0666);
        except OSError, e:
            pass
        try:
            self.readFifo = os.open('cppToPy', os.O_RDONLY);
            self.writeFifo = os.open('pyToCpp', os.O_WRONLY);
        except OSError, e:
            print 'ERROR OPENING PIPE', e
        print 'Pipe opened.'
    
    def readTags(self):
        print 'Reading tags...'
        tagString = os.read(self.readFifo, 1024)
        tagList = utils2.tokenize(tagString)
        print tagList
        return tagList
    
    def readColor(self):
        colorString = os.read(self.readFifo, 128)
        print colorString
        #colorString = '255,255,255'
        list1 = colorString.split(',')
        print list1
        colorList = map(int, list1)
        print 'Received:', colorList
        return colorList
    
    def writeID(self, ID):
    	os.write(self.writeFifo, ID)
    	print 'ID', ID, 'sent.'
    	
    def close(self):
        os.close(self.readFifo)
        os.close(self.writeFifo)

if __name__=="__main__":
    c = Communicator()
    c.readTags()
    while True:
        listy = c.readColor()
        writeID = "0000000000"
        if listy is [-1, -1, -1]:
            break
    c.close()
    
