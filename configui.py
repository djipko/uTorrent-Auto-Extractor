import configobj, sys, os
import wx
from uconfig import read_config
 
########################################################################
class PreferencesDialog(wx.Dialog):
    """
    Creates and displays a preferences dialog that allows the user to
    change some settings.
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the dialog
        """
        wx.Dialog.__init__(self, None, wx.ID_ANY, 'Configuration', size=(550,300))
        self.createWidgets()
 
    #----------------------------------------------------------------------
    def createWidgets(self):
        """
        Create and layout the widgets in the dialog
        """
        lblSizer = wx.BoxSizer(wx.VERTICAL)
        valueSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.StdDialogButtonSizer()
        colSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
 
        conf_filename = os.path.join(os.path.dirname(sys.argv[0]), 'config.ini')
        self.config = configobj.ConfigObj(conf_filename)
        labels = self.config["Labels"]
        values = self.config["Values"]
        self.widgetNames = values
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_NORMAL)
 
        for key in labels:
            value = labels[key]
            lbl = wx.StaticText(self, label=value)
            lbl.SetFont(font)
            lblSizer.Add(lbl, 0, wx.ALL, 6)
 
        for key in values:
            value = values[key]
            if value == '1' or value == '0':
                cb1 = wx.CheckBox(self, wx.ALL, '', name=key)
                if value == '1':
                    bl = True
                else:
                    bl = False
                cb1.SetValue(bl)
                valueSizer.Add(cb1, 0, wx.ALL, 5)
            else:
                txt = wx.TextCtrl(self, value=value, name=key)
                valueSizer.Add(txt, 0, wx.ALL|wx.EXPAND, 5)

        saveBtn = wx.Button(self, wx.ID_OK, label="Save and Hook to uTorrent")
        saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        btnSizer.AddButton(saveBtn)
 
        cancelBtn = wx.Button(self, wx.ID_CANCEL)
        btnSizer.AddButton(cancelBtn)
        btnSizer.Realize()
 
        colSizer.Add(lblSizer)
        colSizer.Add(valueSizer, 1, wx.EXPAND)
        mainSizer.Add(colSizer, 0, wx.EXPAND)
        mainSizer.Add(btnSizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.SetSizer(mainSizer)
 
    #----------------------------------------------------------------------
    def onSave(self, event):
        """
        Saves values to disk
        """
        for name in self.widgetNames:
            widget = wx.FindWindowByName(name)
            if isinstance(widget, wx.CheckBox):
                selection = widget.GetValue()
                if selection:
                    self.widgetNames[name] = '1'
                else:
                    self.widgetNames[name] = '0'
            else:
                value = widget.GetValue()
                self.widgetNames[name] = value
        self.config.write()
        os.system('autoextractor.exe --hook')
        self.EndModal(0)
 
########################################################################
class App(wx.App):
    """"""
 
    #----------------------------------------------------------------------
    def OnInit(self):
        """Constructor"""
        dlg = PreferencesDialog()
        dlg.ShowModal()
        dlg.Destroy()
 
        return True
 
if __name__ == "__main__":
    options = read_config()
    app = App(False)
    app.MainLoop()