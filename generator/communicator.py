import os
import sys
import tempfile
path = os.path.abspath(__file__)
sys.path.append(os.path.join(os.path.dirname(path), "../"))
import utils2

class Communicator(object):
    def __init__(self):
    	done = False
        """try:
            os.mkfifo('cppToPy', 0666);
        except OSError, e:
            pass
        try:
            os.mkfifo('pyToCpp', 0666);
        except OSError, e:
            pass"""
        while not done:
            try:
                self.readFifo = os.open('cppToPy', os.O_RDONLY);
                self.writeFifo = os.open('pyToCpp', os.O_WRONLY);
                done = True
                print 'Pipe opened.'
            except OSError, e:
                pass
                #print 'ERROR OPENING PIPE', e
        
    
    def readTags(self):
        print 'Reading tags...'
        tagString = os.read(self.readFifo, 1024)
        tagList = utils2.tokenize(tagString)
        print tagList
        return tagList
    
    def readColor(self):
        colorString = os.read(self.readFifo, 128)
        print colorString
        list1 = colorString.split(',')
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
        c.writeID('0')
        if listy[0] is -1:
            print 'Mosaic is done'
            break
    c.close()
    
