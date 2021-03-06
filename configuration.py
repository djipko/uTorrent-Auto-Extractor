'''
Created on Mar 2, 2011

@author: Vladimir Cvetic
'''
import sys, uconfig
from PyQt4 import QtGui, QtCore
from autoextractor import hook2utorrent

class ConfUi(QtGui.QWidget):
  
    def __init__(self):
        super(ConfUi, self).__init__()
        self.l = []
        self.e = []
        self.b = []
        self.initUI()
        
    def initUI(self):
        
        useImdbLabel = QtGui.QLabel('Use imdb.com')
        useTorrentLabelsLabel = QtGui.QLabel('Use uTorrent Labels')
        storageLabel = QtGui.QLabel('Storage directory:')

        self.useImdbCheckbox = QtGui.QCheckBox()
        self.useTorrentLabelsCheckbox = QtGui.QCheckBox()

        self.storageDirEdit = QtGui.QLineEdit()
        storageDirButton = QtGui.QPushButton('Browse...', self)
        self.connect(storageDirButton, QtCore.SIGNAL('clicked()'), 
                     self.directoryDialogFactory(self.storageDirEdit)) 
  
         
        addLabelBtn = QtGui.QPushButton('add label', self)
        self.connect(addLabelBtn, QtCore.SIGNAL('clicked()'), 
                     self.createLabelStorageInput) 
        
        saveButton = QtGui.QPushButton('Save and hook to uTorrent', self)
        self.connect(saveButton, QtCore.SIGNAL('clicked()'), 
                     self.save)
        
        resetButton = QtGui.QPushButton('Reset to default', self)
        self.connect(resetButton, QtCore.SIGNAL('clicked()'), 
                     self.resetToDefaultWrap)
        
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
        self.grid.addWidget(self.useImdbCheckbox, 2, 1)

        self.grid.addWidget(useTorrentLabelsLabel, 3, 0)
        self.grid.addWidget(self.useTorrentLabelsCheckbox, 3, 1)
        
        self.grid.addWidget(storageGLabel, 5, 0)

        self.grid.addWidget(storageLabel, 6, 0)
        self.grid.addWidget(self.storageDirEdit, 6, 1)
        self.grid.addWidget(storageDirButton, 6, 2)
        
        self.grid.addWidget(labelsGLabel, 7, 0)
        self.grid.addWidget(addLabelBtn, 7, 2)
        
        lbl = QtGui.QLabel('Label')
        lbl1 = QtGui.QLabel('Target directory')
        self.grid.addWidget(lbl, 8, 0)
        self.grid.addWidget(lbl1, 8, 1)
                
        self.grid2 = QtGui.QGridLayout()
        self.grid2.setSpacing(8)
        self.grid2.addWidget(saveButton, 0, 0)
        self.grid2.addWidget(resetButton, 0, 1)
        self.grid2.addWidget(quitButton, 0, 2)
        
        top.setLayout(self.grid)
        bottom.setLayout(self.grid2)
        self.setLayout(hbox)
        
        self.setWindowTitle('uTorrent Auto Extractor Configuration')
        self.populateFields()
    
    def createLabelStorageInput(self, label_name=None, label_dir=None):
        sze = len(self.l)
        self.l.append(QtGui.QLineEdit(label_name))
        self.e.append(QtGui.QLineEdit(label_dir))
        self.b.append(QtGui.QPushButton('Browse...', self))
        
        self.connect(self.b[sze], QtCore.SIGNAL('clicked()'), 
                     self.directoryDialogFactory(self.e[sze])) 
        
        cnt = int(self.grid.rowCount())
        self.grid.addWidget(self.l[sze], cnt+2, 0)
        self.grid.addWidget(self.e[sze], cnt+2, 1)
        self.grid.addWidget(self.b[sze], cnt+2, 2)
        
    def directoryDialogFactory(self, param):
        def showDirectoryDialog():
            param.setText(str(QtGui.QFileDialog.getExistingDirectory(self, 'Select directory')))
        return showDirectoryDialog       
 
    def resetToDefaultWrap(self):
        uconfig.resetToDefault()
        self.populateFields()
 
    def populateFields(self):
        options = uconfig.read_config()
        
        for label in options['Labels']:
            self.createLabelStorageInput(label, options['Labels'][label])
            
        self.storageDirEdit.setText(options['Global']['storage_dir'])

        if int(options['Global']['imdb']) == 1:
            self.useImdbCheckbox.setChecked(True)
            
        if int(options['Global']['use_labels']) == 1:
            self.useTorrentLabelsCheckbox.setChecked(True)    

    
    def save(self):
        options = uconfig.read_config()
             
        i = 0
        s = len(self.l)
        while i<s:
            if self.l[i] is not None and str(self.l[i].text()) is not '':
                options['Labels'][str(self.l[i].text())] = str(self.e[i].text())
            i += 1       
            
        options['Global']['storage_dir'] = str(self.storageDirEdit.text())
        
        options['Global']['imdb'] = self.useImdbCheckbox.isChecked() and '1' or '0'
        options['Global']['use_labels'] = self.useTorrentLabelsCheckbox.isChecked() and '1' or '0'

        uconfig.write_config(options)
        hook2utorrent()
            
if __name__ == "__main__":     
    app = QtGui.QApplication(sys.argv)
    ex = ConfUi()
    ex.show()
    sys.exit(app.exec_())