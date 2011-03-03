"""
Access utorrent config files, read and write
"""
import bencode, os, sys
from PyQt4 import QtGui

class uTorrent():
    
    def __init__(self):
        self.msgb = MessageBox()
    
    def isuTorrentRunning(self):
        utorrent = -1
        while utorrent == -1:
            if ''.join(os.popen('TASKLIST').readlines()).find('uTorrent.exe') >= 0:            
                if self.msgb.utRunning() == True:
                    continue
                else:
                    return False
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
        
        #if self.fileData[name] is None:
        #    return False
        
        self.fileData[name] = value
            
    def save(self):
        if self.isuTorrentRunning() == False:
            return False
        
        if self.fileData is None:
            return False
        
        l = bencode.bencode(self.fileData)
        f = open(self.confPath, 'wb')
        f.write(l)
        f.close() 
        self.msgb.msg("Configuration saved.")
        
class MessageBox(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

    def utRunning(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "uTorrent is running.\nPlease close uTorrent and click Retry.", QtGui.QMessageBox.Retry, QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Retry:
            return True
        else:
            return False
    
    def msg(self, text):
        QtGui.QMessageBox.question(self, 'Message', text, QtGui.QMessageBox.Ok)
        