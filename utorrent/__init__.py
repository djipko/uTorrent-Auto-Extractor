"""
Access utorrent config files, read and write
"""
import bencode, os, sys

class uTorrent():
    
    def __init__(self):
        """
        """
    
    def isuTorrentRunning(self):
        utorrent = -1
        while utorrent == -1:
            if ''.join(os.popen('TASKLIST').readlines()).find('uTorrent.exe') >= 0:
                print "uTorrent is running. Please close uTorrent and try again."
                print
                os.system('PAUSE')
            else:
                utorrent = 1        
    
    def setConfPath(self, confPath):
        if os.path.exists(confPath):
            self.confPath = confPath
            self.readFile()
        else:
            return False
    
    def readFile(self):
        f = open(self.confPath, 'rb')
        l = f.read()
        f.close()
        self.fileData = bencode.bdecode(l)
         
    def getOption(self, name):
        if self.fileData is None:
            return False
        
        return self.fileData[name]       
       
    def setOption(self, name, value):
        self.isuTorrentRunning()
        if self.fileData is None:
            return False
        
        if self.fileData[name] is None:
            return False
        
        self.fileData[name] = value
            
    def save(self):
        self.isuTorrentRunning()
        if self.fileData is None:
            return False
        
        l = bencode.bencode(self.fileData)
        f = open(self.confPath, 'wb')
        f.write(l)
        f.close() 