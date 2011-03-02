'''
Created on Mar 2, 2011

@author: Vladimir Cvetic
'''
import sys
from PyQt4 import QtGui, QtCore

class ConfUi(QtGui.QWidget):
  
    def __init__(self):
        super(ConfUi, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        useImdbLabel = QtGui.QLabel('Use imdb.com')
        useTorrentLabelsLabel = QtGui.QLabel('Use uTorrent Labels')
        sevenZipLabel = QtGui.QLabel('7-Zip location:')
        storageLabel = QtGui.QLabel('Storage directory:')

        useImdbCheckbox = QtGui.QCheckBox()
        useTorrentLabelsCheckbox = QtGui.QCheckBox()
        
        sevenZipEdit = QtGui.QLineEdit()
        sevenZipButton = QtGui.QPushButton('Browse...', self)
        self.inputBox = sevenZipEdit
        self.connect(sevenZipButton, QtCore.SIGNAL('clicked()'), 
                     self.showFileDialog)

        storageDirEdit = QtGui.QLineEdit()
        storageDirButton = QtGui.QPushButton('Browse...', self)
        self.inputBox = storageDirEdit
        self.connect(storageDirButton, QtCore.SIGNAL('clicked()'), 
                     self.showDirectoryDialog) 
  
         
        addLabelBtn = QtGui.QPushButton('add label', self)
        self.connect(addLabelBtn, QtCore.SIGNAL('clicked()'), 
                     self.createLabelStorageInput) 
        
        saveButton = QtGui.QPushButton('Save and hook to uTorrent', self)
        quitButton = QtGui.QPushButton('Quit', self)
        self.connect(quitButton, QtCore.SIGNAL('clicked()'), 
                     sys.exit)

        generalLabel = QtGui.QLabel('<b>General Configuration</b>')
        storageGLabel = QtGui.QLabel('<b>Storage</b>')
        labelsGLabel = QtGui.QLabel('<b>Per Label Storage</b>')
 
        hbox = QtGui.QHBoxLayout(self)
        
        top = QtGui.QFrame(self)
        top.setFrameShape(QtGui.QFrame.StyledPanel)        
        
        bottom = QtGui.QFrame(self)
        bottom.setFrameShape(QtGui.QFrame.StyledPanel)

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(top)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        
        hbox.addWidget(splitter2)
         
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(8)

        self.grid.addWidget(generalLabel, 1, 0)

        self.grid.addWidget(useImdbLabel, 2, 0)
        self.grid.addWidget(useImdbCheckbox, 2, 1)

        self.grid.addWidget(useTorrentLabelsLabel, 3, 0)
        self.grid.addWidget(useTorrentLabelsCheckbox, 3, 1)

        self.grid.addWidget(sevenZipLabel, 4, 0)
        self.grid.addWidget(sevenZipEdit, 4, 1)
        self.grid.addWidget(sevenZipButton, 4, 2)
        
        self.grid.addWidget(storageGLabel, 5, 0)

        self.grid.addWidget(storageLabel, 6, 0)
        self.grid.addWidget(storageDirEdit, 6, 1)
        self.grid.addWidget(storageDirButton, 6, 2)
        
        self.grid.addWidget(labelsGLabel, 7, 0)
        self.grid.addWidget(addLabelBtn, 7, 2)
            
        self.grid2 = QtGui.QGridLayout()
        self.grid2.setSpacing(8)
        self.grid2.addWidget(saveButton, 0, 0)
        self.grid2.addWidget(quitButton, 0, 1)
        
        top.setLayout(self.grid)
        bottom.setLayout(self.grid2)
        self.setLayout(hbox)
        
        self.setWindowTitle('uTorrent Auto Extractor Configuration')
    
    def createLabelStorageInput(self):
        self.l = QtGui.QLabel("Label:")
        self.e = QtGui.QLineEdit()
        self.b = QtGui.QPushButton('Browse...', self)
        self.inputBox = self.e
        self.connect(self.b, QtCore.SIGNAL('clicked()'), 
                     self.showDirectoryDialog) 
        cnt = int(self.grid.rowCount())
        self.grid.addWidget(self.l, cnt+1, 0)
        self.grid.addWidget(self.e, cnt+1, 1)
        self.grid.addWidget(self.b, cnt+1, 2)
    
    def showFileDialog(self):
        self.inputBox.setText(str(QtGui.QFileDialog.getOpenFileName(self, 'Select file')))
        
    def showDirectoryDialog(self):
        self.inputBox.setText(str(QtGui.QFileDialog.getExistingDirectory(self, 'Select directory')))
        
app = QtGui.QApplication(sys.argv)
ex = ConfUi()
ex.show()
sys.exit(app.exec_())