
import math
import wx
import os
 
class MainWindow(wx.Frame):
    
    def __init__(self, title):
        
        import ctypes
        myappid = 'calculator.scottiltd'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)        
        
        wx.Frame.__init__(self, None, wx.ID_ANY, title=title, style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        self.path = os.path.dirname(os.getcwd())
        
        self.settings = {"mode": "Default", "history": True, "HistoryMaxlenght": 10, "HistorySave": "All"}
        self.history = []
        self.text = ["0"]
        self.printer = ["0"]
        self.memory = ["0"]    

        self.font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline = False, faceName ="")
        self.operators_font = wx.Font(9, wx.DEFAULT, wx.BOLD, wx.NORMAL, underline = False, faceName ="")
        
        self.rootx = False
        self.new = True
        
################################################################################
##################################FRAME HEADER##################################
################################################################################
        
        optionsMenu = wx.Menu()
        
        self.menuHistory = wx.Menu()
        self.showHistory = self.menuHistory.Append(111, "Show History\tCTRL+h", "Show Calculator's History")
        self.Bind(wx.EVT_MENU, self.OnShowHistory, self.showHistory)
        self.copyHistory = self.menuHistory.Append(112, "Copy History\tALT+c", "Copy Calculator's History")
        self.Bind(wx.EVT_MENU, self.OnCopyHistory, self.copyHistory)
        self.deleteHistory = self.menuHistory.Append(113, "Delete History\tALT+d", "Delete Calculator's History")
        self.Bind(wx.EVT_MENU, self.OnDeleteHistory, self.deleteHistory)
        optionsMenu.AppendSubMenu(self.menuHistory, "History", "Options for Calculator's History")
        optionsMenu.AppendSeparator()
        
################################################################################
        
        settingsMenu = wx.Menu()
        
        menuHistorySettings = wx.Menu()
        self.enableHistory = menuHistorySettings.AppendCheckItem(211, "Enable History", "Enable History")
        self.Bind(wx.EVT_MENU, self.OnEnableHistory, self.enableHistory)
        if self.settings["history"] == True:
            self.enableHistory.Check()
        menuHistorySettings.AppendSeparator()
        self.pos10 = menuHistorySettings.AppendRadioItem(212, "10 items", "Max items in history: 10")
        self.Bind(wx.EVT_MENU, self.OnMax10Items, self.pos10)
        self.pos5 = menuHistorySettings.AppendRadioItem(213, "5 items", "Max items in history: 5")
        self.Bind(wx.EVT_MENU, self.OnMax5Items, self.pos5)
        self.pos3 = menuHistorySettings.AppendRadioItem(214, "3 items", "Max items in history: 3")
        self.Bind(wx.EVT_MENU, self.OnMax3Items, self.pos3)
        if self.settings["HistoryMaxlenght"] == 10:
            self.pos10.Check()
        elif self.settings["HistoryMaxlenght"] == 5:
            self.pos5.Check()
        elif self.settings["HistoryMaxlenght"] == 3:
            self.pos3.Check()    
        menuHistorySettings.AppendSeparator()
        self.CorrectOnly = menuHistorySettings.AppendRadioItem(215, "Save Correct Only", "Save Only Correct Operations")
        self.Bind(wx.EVT_MENU, self.OnCorrectOnly, self.CorrectOnly)
        self.All = menuHistorySettings.AppendRadioItem(216, "Save All", "Save All Operations")
        self.Bind(wx.EVT_MENU, self.OnAll, self.All)   
        if self.settings["HistorySave"] == "CorrectOnly":
            self.CorrectOnly.Check()
        elif self.settings["HistorySave"] == "All":
            self.All.Check()
        settingsMenu.AppendSubMenu(menuHistorySettings, "History", "History Settings")
        
################################################################################
        
        modeMenu = wx.Menu()
        self.defaultMode = modeMenu.AppendRadioItem(301, "Default\tCTRL+d", "Set Default Mode")
        self.Bind(wx.EVT_MENU, self.OnDefaultMode, self.defaultMode)
        self.scientificMode = modeMenu.AppendRadioItem(302, "Scientific\tCTRL+s", "Set Scientific Mode")
        self.Bind(wx.EVT_MENU, self.OnScientificMode, self.scientificMode)
        if self.settings["mode"] == "Default":
            self.defaultMode.Check()
        elif self.settings["mode"] == "Scientific":
            self.scientificMode.Check()
################################################################################
        
        infoMenu = wx.Menu()
        self.info = infoMenu.Append(400, "Info\tCTRL+i", "Information About Calculator")
        self.Bind(wx.EVT_MENU, self.OnAbout, self.info)
        
################################################################################
        
        fakeMenu = wx.Menu()
        self.m1 = fakeMenu.Append(1, "1", "1") 
        self.Bind(wx.EVT_MENU, self.On1, self.m1)
        self.m2 = fakeMenu.Append(2, "2", "2") 
        self.Bind(wx.EVT_MENU, self.On2, self.m2)
        self.m3 = fakeMenu.Append(3, "3", "3") 
        self.Bind(wx.EVT_MENU, self.On3, self.m3)
        self.m4 = fakeMenu.Append(4, "4", "4") 
        self.Bind(wx.EVT_MENU, self.On4, self.m4)
        self.m5 = fakeMenu.Append(5, "5", "5") 
        self.Bind(wx.EVT_MENU, self.On5, self.m5)
        self.m6 = fakeMenu.Append(6, "6", "6") 
        self.Bind(wx.EVT_MENU, self.On6, self.m6)
        self.m7 = fakeMenu.Append(7, "7", "7") 
        self.Bind(wx.EVT_MENU, self.On7, self.m7)
        self.m8 = fakeMenu.Append(8, "8", "8") 
        self.Bind(wx.EVT_MENU, self.On8, self.m8)
        self.m9 = fakeMenu.Append(9, "9", "9") 
        self.Bind(wx.EVT_MENU, self.On9, self.m9)
        self.m0 = fakeMenu.Append(10, "0", "0") 
        self.Bind(wx.EVT_MENU, self.On0, self.m0)
        self.mPlus = fakeMenu.Append(11, "Plus", "Plus") 
        self.Bind(wx.EVT_MENU, self.OnPlus, self.mPlus)
        self.mMinus = fakeMenu.Append(12, "Minus", "Minus") 
        self.Bind(wx.EVT_MENU, self.OnMinus, self.mMinus)
        self.mMultiply = fakeMenu.Append(13, "Multiply", "Multiply") 
        self.Bind(wx.EVT_MENU, self.OnMultiply, self.mMultiply)
        self.mDivide = fakeMenu.Append(14, "Divide", "Divide") 
        self.Bind(wx.EVT_MENU, self.OnDivide, self.mDivide)
        self.mPoint = fakeMenu.Append(15, "Point", "Point") 
        self.Bind(wx.EVT_MENU, self.OnPoint, self.mPoint)  
        self.mEqual = fakeMenu.Append(16, "Equal", "Equal") 
        self.Bind(wx.EVT_MENU, self.OnEqual, self.mEqual)        
        self.mCanc = fakeMenu.Append(17, "Canc", "Canc") 
        self.Bind(wx.EVT_MENU, self.OnCanc, self.mCanc)  
        self.mBack = fakeMenu.Append(18, "Back", "Back")
        self.Bind(wx.EVT_MENU, self.OnBack, self.mBack)                  
        self.mCopy = fakeMenu.Append(20, "Copy", "Copy") 
        self.Bind(wx.EVT_MENU, self.OnCopy, self.mCopy)          
        
################################################################################
        
        menuBar = wx.MenuBar()
        menuBar.Append(optionsMenu, "Options")
        menuBar.Append(settingsMenu, "Settings")
        menuBar.Append(modeMenu, "Mode")
        menuBar.Append(infoMenu, "?")
        self.SetMenuBar(menuBar)      
        
################################################################################
################################################################################
        
        self.accel_tab = wx.AcceleratorTable([wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('q'), wx.ID_EXIT),
                                              wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('i'), 400), 
                                              wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('c'), 20), 
                                              wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('s'), 302),
                                              wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('d'), 301),                                               
                                              wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('h'), 111),
                                              wx.AcceleratorEntry(wx.ACCEL_ALT, ord('c'), 112),
                                              wx.AcceleratorEntry(wx.ACCEL_ALT, ord('d'), 113),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD1, 1),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("1"), 1),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD2, 2),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("2"), 2),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD3, 3),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("3"), 3),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD4, 4),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("4"), 4),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD5, 5),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("5"), 5),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD6, 6),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("6"), 6),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD7, 7),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("7"), 7),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD8, 8),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("8"), 8),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD9, 9),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("9"), 9),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD0, 10),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("0"), 10),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD_ADD, 11),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_ADD, 11),                                              
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD_SUBTRACT, 12),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_SUBTRACT, 12),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD_MULTIPLY, 13),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_MULTIPLY, 13),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD_DIVIDE, 14),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_DIVIDE, 14),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD_DECIMAL, 15),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_DECIMAL, 15),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord(","), 15),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, ord("."), 15),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_NUMPAD_SPACE, 16),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_RETURN, 16),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_DELETE, 17),
                                              wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_BACK, 18),                                              
                                              ])
        
        self.SetAcceleratorTable(self.accel_tab)                  
        
################################################################################
################################################################################
        
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText("  Welcome to Calculator: Good Work")
        
################################################################################
################################################################################
        
        self.SetIcon(wx.Icon(self.path + '/favicon.ico'))
        
################################################################################
##################################FRAME BODY####################################
################################################################################
        

        self.display = wx.Button(self, id=wx.ID_ANY, label="\n", style=wx.BU_RIGHT, size=(310, 65))
        self.display.SetLabel("0  ")
        font1 = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline = False, faceName ="")
        self.display.SetFont(font1)
        
################################################################################
        
        mc = wx.Button(self, wx.ID_STATIC,  "mc")
        mc.Bind(wx.EVT_BUTTON, self.OnMemoryCanc)
        rm = wx.Button(self, wx.ID_STATIC,  "rm")
        rm.Bind(wx.EVT_BUTTON, self.OnMemoryCall)            
        mx = wx.Button(self, wx.ID_STATIC,  "m+")
        mx.Bind(wx.EVT_BUTTON, self.OnMemoryPlus)            
        canc = wx.Button(self, wx.ID_STATIC,  "canc")
        canc.Bind(wx.EVT_BUTTON, self.OnCanc) 
        
################################################################################
        
        one = wx.Button(self, wx.ID_STATIC,  "1")
        one.Bind(wx.EVT_BUTTON, self.On1) 
        two = wx.Button(self, wx.ID_STATIC,  "2")
        two.Bind(wx.EVT_BUTTON, self.On2) 
        three = wx.Button(self, wx.ID_STATIC, "3")
        three.Bind(wx.EVT_BUTTON, self.On3) 
        four = wx.Button(self, wx.ID_STATIC,  "4")
        four.Bind(wx.EVT_BUTTON, self.On4) 
        five = wx.Button(self, wx.ID_STATIC,  "5")
        five.Bind(wx.EVT_BUTTON, self.On5) 
        six = wx.Button(self, wx.ID_STATIC,  "6")
        six.Bind(wx.EVT_BUTTON, self.On6) 
        seven = wx.Button(self, wx.ID_STATIC,  "7")
        seven.Bind(wx.EVT_BUTTON, self.On7, seven) 
        eight = wx.Button(self, wx.ID_STATIC,  "8")
        eight.Bind(wx.EVT_BUTTON, self.On8) 
        nine = wx.Button(self, wx.ID_STATIC,  "9")
        nine.Bind(wx.EVT_BUTTON, self.On9) 
        zero = wx.Button(self, wx.ID_STATIC,  "0")
        zero.Bind(wx.EVT_BUTTON, self.On0)
        
################################################################################
        
        point = wx.Button(self, wx.ID_STATIC,  ",")
        point.Bind(wx.EVT_BUTTON, self.OnPoint) 
        sign = wx.Button(self, wx.ID_STATIC,  "+/-")
        sign.Bind(wx.EVT_BUTTON, self.OnChangeSign) 
        plus = wx.Button(self, wx.ID_STATIC,  "+")
        plus.Bind(wx.EVT_BUTTON, self.OnPlus)
        minus = wx.Button(self, wx.ID_STATIC,  "-")
        minus.Bind(wx.EVT_BUTTON, self.OnMinus)
        multiply = wx.Button(self, wx.ID_STATIC,  "*")
        multiply.Bind(wx.EVT_BUTTON, self.OnMultiply)
        divide = wx.Button(self, wx.ID_STATIC,  "/") 
        divide.Bind(wx.EVT_BUTTON, self.OnDivide)
        equal = wx.Button(self, wx.ID_STATIC,  label="=", size=(310, 45))
        equal.Bind(wx.EVT_BUTTON, self.OnEqual)

################################################################################
        
        exp2 = wx.Button(self,wx.ID_STATIC, "x\u00B2")
        exp2.Bind(wx.EVT_BUTTON, self.OnExp2)
        exp3 = wx.Button(self,wx.ID_STATIC, "x\u00B3")
        exp3.Bind(wx.EVT_BUTTON, self.OnExp3)
        expX = wx.Button(self, wx.ID_STATIC, "x\u02B8")
        expX.Bind(wx.EVT_BUTTON, self.OnExpX)
        root2 = wx.Button(self, wx.ID_STATIC, "\u00B2\u221Ax")
        root2.Bind(wx.EVT_BUTTON, self.OnRoot2)
        root3 = wx.Button(self, wx.ID_STATIC, "\u00B3\u221Ax")
        root3.Bind(wx.EVT_BUTTON, self.OnRoot3)
        rootx = wx.Button(self, wx.ID_STATIC, "\u02B8\u221Ax")
        sin = wx.Button(self, wx.ID_STATIC, "sin")
        sin.Bind(wx.EVT_BUTTON, self.OnSin)
        sinh = wx.Button(self, wx.ID_STATIC, "sin\u207B\u00B9")
        sinh.Bind(wx.EVT_BUTTON, self.OnSinh)
        cos = wx.Button(self, wx.ID_STATIC, "cos")
        cos.Bind(wx.EVT_BUTTON, self.OnCos)
        cosh = wx.Button(self, wx.ID_STATIC, "cos\u207B\u00B9")
        cosh.Bind(wx.EVT_BUTTON, self.OnCosh)
        tan = wx.Button(self, wx.ID_STATIC, "tan")
        tanh = wx.Button(self, wx.ID_STATIC, "tan\u207B\u00B9")
        back = wx.Button(self, wx.ID_STATIC, "\u001B")
        back.Bind(wx.EVT_BUTTON, self.OnBack)        
        greekP = wx.Button(self, wx.ID_STATIC, "\u03C0")
        greekP.Bind(wx.EVT_BUTTON, self.OnGreekP)
        per100 = wx.Button(self, wx.ID_STATIC, "\u0025")
        per100.Bind(wx.EVT_BUTTON, self.OnPer100)
        per1000 = wx.Button(self, wx.ID_STATIC, "\u2030")
        per1000.Bind(wx.EVT_BUTTON, self.OnPer1000)
        permilione = wx.Button(self, wx.ID_STATIC, "\u2031")
        permilione.Bind(wx.EVT_BUTTON, self.OnPerMilione)
        back = wx.Button(self, wx.ID_STATIC, "\u001B")
        back.Bind(wx.EVT_BUTTON, self.OnBack)        
        greekP = wx.Button(self, wx.ID_STATIC, "\u03C0")
        greekP.Bind(wx.EVT_BUTTON, self.OnGreekP)
        openpar = wx.Button(self, wx.ID_STATIC, "(")
        closepar = wx.Button(self, wx.ID_STATIC, ")")
        reverse = wx.Button(self, wx.ID_STATIC, "\u00B9/\u2093")
        reverse.Bind(wx.EVT_BUTTON, self.OnReverse)
        
################################################################################
################################FRAME SIZERS####################################
################################################################################
        
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.buttons1 = [back, greekP, openpar, closepar, reverse]
        for x in range(len(self.buttons1)):
            self.buttons1[x].SetFont(self.font)
            self.sizer1.Add(self.buttons1[x], 1, wx.EXPAND)       
        
        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.buttons2 = [tan, tanh, per100, per1000, permilione]
        for x in range(len(self.buttons2)):
            self.buttons2[x].SetFont(self.font)
            self.sizer2.Add(self.buttons2[x], 1, wx.EXPAND)
        
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.buttons3 = [sin, sinh, root2, exp2, expX]
        for x in range(len(self.buttons3)):
            self.buttons3[x].SetFont(self.font)
            self.sizer3.Add(self.buttons3[x], 1, wx.EXPAND) 
        
        self.sizer4 = wx.BoxSizer(wx.VERTICAL)
        self.buttons4 = [cos, cosh, root3, exp3, rootx]
        for x in range(len(self.buttons4)):
            self.buttons4[x].SetFont(self.font)
            self.sizer4.Add(self.buttons4[x], 1, wx.EXPAND)  
        
        self.sizer5 = wx.BoxSizer(wx.VERTICAL)
        self.buttons5 = [mc, nine, six, three, point]
        for x in range(len(self.buttons5)):
            self.buttons5[x].SetFont(self.font)
            self.sizer5.Add(self.buttons5[x], 1, wx.EXPAND)
        
        self.sizer6 = wx.BoxSizer(wx.VERTICAL)
        self.buttons6 = [rm, eight, five, two, zero]
        for x in range(len(self.buttons6)):
            self.buttons6[x].SetFont(self.font)
            self.sizer6.Add(self.buttons6[x], 1, wx.EXPAND) 
        
        self.sizer7 = wx.BoxSizer(wx.VERTICAL)
        self.buttons7 = [mx, seven, four, one, sign]
        for x in range(len(self.buttons7)):
            self.buttons7[x].SetFont(self.operators_font)
            self.sizer7.Add(self.buttons7[x], 1, wx.EXPAND) 
        
        self.sizer8 = wx.BoxSizer(wx.VERTICAL)
        self.buttons8 = [canc, plus, minus, multiply, divide]
        for x in range(len(self.buttons8)):
            self.buttons8[x].SetFont(self.font)
            self.sizer8.Add(self.buttons8[x], 1, wx.EXPAND)        
        
################################################################################
            
        self.parent_sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.sizers = [self.sizer1, self.sizer2, self.sizer3, self.sizer4, self.sizer5, self.sizer6, self.sizer7, self.sizer8]
        for x in range(len(self.sizers)):
            self.sizer.Add(self.sizers[x], 0, wx.EXPAND)
        
        self.parent_sizer.Add(self.display, 1, wx.EXPAND)
        self.parent_sizer.Add(self.sizer, 0, wx.EXPAND)
        self.parent_sizer.Add(equal, 1, wx.EXPAND)
        
        if self.settings["mode"] == "Default":
    
            self.sizer1.ShowItems(False)
            self.sizer2.ShowItems(False)
            self.sizer3.ShowItems(False)         
            self.sizer4.ShowItems(False)
            
            self.SetSize(310, 305)                
            
        else:
            
    
            self.sizer1.ShowItems(True)
            self.sizer2.ShowItems(True)
            self.sizer3.ShowItems(True)         
            self.sizer4.ShowItems(True)
            
            self.SetSize(615, 305)                
            
        
        self.SetSizer(self.parent_sizer)
        self.Show(True)

################################################################################   
############################### FRAME METHODS ##################################
################################################################################

    
    
    def timeout(self, time, target):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, target, self.timer)
        self.timer.Start(int(time))
    
    def SetDefaultStatus(self, event):
        self.statusbar.SetStatusText("  Welcome to Calculator: Good Work")   
        try:
            self.timer.Stop()
        except:
            pass
    
    def SetTemporaryStatus(self, status, time=3000):
        self.statusbar.SetStatusText(status)
        self.timeout(time, self.SetDefaultStatus)
    
    def SetStatus(self, event, status):
        self.statusbar.SetStatusText(status)  
    
    
################################################################################
################################################################################
    
    def OnAbout(self, event):
        wx.MessageDialog( self, """
Calculator was born to help students and common person in their work, from the 

most basic count to the more complecated operations.

It was developed by Leonardo Scotti using Python 3.8.3
The GUI was developed using the WxPython framework
(version: "4.1.1 msw (phoenix) wxWidgets 3.1.5")

The current version of Calculator is 0.20.8
""", "About Calculator", wx.OK|wx.ICON_INFORMATION).ShowModal()    
    
    def OnHotkeys(self, event):
        wx.MessageDialog( self, """
[CTRL + d] = default mode
[CTRL + s] = scientific mode
[CTRL + c] = copy text
[CTRL + i] = show info
[CTRL + h] = show history
[ALT + c] = copy history
[AlT + d] = delete history
""", "ACalculator Hotkeys", wx.OK|wx.ICON_INFORMATION).ShowModal()    
        
    
    def OnReadme(self, event):
        #opens the README.txt istruction file of the program
        subprocess.Popen(["notepad.exe", self.path + "/README.txt"])
    
    def OnDefaultMode(self, event):
        if self.settings["mode"] == "Scientific":
            self.defaultMode.Check()
            self.settings["mode"] = "Default"
    
            self.sizer1.ShowItems(False)
            self.sizer2.ShowItems(False)
            self.sizer3.ShowItems(False)
            self.sizer4.ShowItems(False)
            
            self.SetSize(310, 305) 
            self.parent_sizer.Layout()
    
    def OnScientificMode(self, event):
        if self.settings["mode"] == "Default":
            self.scientificMode.Check()
            self.settings["mode"] = "Scientific"
            
            self.sizer4.ShowItems(True)
            self.sizer3.ShowItems(True)
            self.sizer2.ShowItems(True)
            self.sizer1.ShowItems(True)
            
            self.SetSize(615, 305)
            self.parent_sizer.Layout()

    
    def OnDocumentation(self, event):
        pass    
    
    def OnEnableHistory(self, event):
        if self.settings["history"] == True:
            self.enableHistory.Check(False)
            self.pos10.Enable(False)
            self.pos5.Enable(False)
            self.pos3.Enable(False)
            self.CorrectOnly.Enable(False)
            self.All.Enable(False)
            self.showHistory.Enable(False)
            self.copyHistory.Enable(False)
            self.deleteHistory.Enable(False)
            self.settings["history"] = False
        else:
            self.enableHistory.Check(True)
            self.pos10.Enable(True)
            self.pos5.Enable(True)
            self.pos3.Enable(True)  
            self.CorrectOnly.Enable(True)
            self.All.Enable(True)            
            self.showHistory.Enable(True)
            self.copyHistory.Enable(True)
            self.deleteHistory.Enable(True)            
            self.settings["history"] = True

    
    def OnMax10Items(self, event):
        self.pos10.Check()
        self.settings["HistoryMaxlenght"] = 10
    
    def OnMax5Items(self, event):
        self.pos5.Check()
        self.settings["HistoryMaxlenght"] = 5
    
    def OnMax3Items(self, event):
        self.pos3.Check()
        self.settings["HistoryMaxlenght"] = 3

    def OnCorrectOnly(self, event):
        self.CorrectOnly.Check()
        self.settings["HistorySave"] = "CorrectOnly"
    
    def OnAll(self, event):
        self.All.Check()
        self.settings["HistorySave"] = "All"
    
    def OnShowHistory(self, event):
        txt =  "\u0007  "+ "\n \n \u0007  ".join(self.history)
        if txt.strip() == "\u0007":
            txt = "                                        EMPTY HISTORY "
        wx.MessageDialog( self, txt,  "Calculator's History", wx.OK|wx.ICON_NONE).ShowModal()
    
    def OnCopyHistory(self, event):
        txt =  "\u0007  "+ "\n \n \u0007  ".join(self.history)
        if txt.strip() != "\u0007":       
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
            wx.TheClipboard.Clear()
            wx.TheClipboard.SetData(wx.TextDataObject(txt))
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
            self.SetTemporaryStatus("History copied successfully", 3000)
    
    def OnDeleteHistory(self, event):
        self.history.clear()
        self.SetTemporaryStatus("History deleted successfully", 3000)

    def OnCopy(self, event):
        txt =  "".join(self.printer)
        if txt.strip() != "":       
            if not wx.TheClipboard.IsOpened():
                wx.TheClipboard.Open()
            wx.TheClipboard.Clear()
            wx.TheClipboard.SetData(wx.TextDataObject(txt))
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()    
            self.SetTemporaryStatus("Result copied successfully", 3000)

################################################################################
################################################################################
    

    def displayer(self):
        if self.printer == [] or len(self.printer) == 0 or "".join(self.printer) == "":
            self.display.SetLabel("0  ")
        elif self.printer == ["ERROR  "]:
            self.display.SetLabel(str("".join(self.printer)) + "  ")
            self.printer.clear()
        else:
            self.display.SetLabel(str("".join(self.printer)) + "  ")
        self.parent_sizer.Layout()
    
    
    def HistoryUpgrade(self, operation):
        
        if len(self.history) < int(self.settings["HistoryMaxlenght"]):
            self.history.append(operation)
        else:
            while len(self.history) >= self.settings["HistoryMaxlenght"]:
                self.history.pop(0)
            self.history.append(operation)
        
    
    def AddNumber(self, number):
        
        number = list(number)        
        if self.new == True:
            self.text.clear()
            self.printer.clear()
        if self.rootx == True:
            self.Root(number)
        else:        
            if self.text == ["0"]:
                self.text.pop(0)
            for elem in number:
                self.text.append(elem)
            if self.printer == ["0"]:
                self.printer.pop(0)
            for elem in number:
                self.printer.append(elem)
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))        
        self.new = False
    
    def AddOperator(self, operator):
        
        operators = [" / ", " * ", " + ", " - "]
        
        if operator not in self.text and self.text[-1] not in operators:
            
            for elem in operators:
                
                if elem in self.text:
                    
                    break
                 
                
            else:
                
                self.text.append(operator) 
                
            
        elif operator not in self.text and self.text[-1] in operators:
            
            self.text.pop(-1)
            self.text.append(operator)
            
        elif operator in self.text:
            
            pass
            
        
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))        
        self.printer.clear()
        self.new = False
    
    
################################################################################
################################################################################
    
    
    def On1(self, event):
        self.AddNumber("1")
        self.displayer()

    def On2(self, event):
        self.AddNumber("2")
        self.displayer()

    def On3(self, event):
        self.AddNumber("3")
        self.displayer()

    def On4(self, event):
        self.AddNumber("4")
        self.displayer()

    def On5(self, event):
        self.AddNumber("5")
        self.displayer()

    def On6(self, event):
        self.AddNumber("6")
        self.displayer()

    def On7(self, event):
        self.AddNumber("7")
        self.displayer()

    def On8(self, event):
        self.AddNumber("8")
        self.displayer()

    def On9(self, event):
        self.AddNumber("9")
        self.displayer()

    def On0(self, event):
        self.AddNumber("0")
        self.displayer()


################################################################################


    def OnChangeSign(self, event):
        if self.printer != ["0"] and self.printer != []:
            if self.printer[0] == "-":
                for elem in self.printer:
                    self.text.pop(-1)
                self.printer.pop(0)
                for elem in self.printer:
                    self.text.append(elem)
                self.displayer()
                
            else:
                for elem in self.printer:
                    self.text.pop(-1)
                self.printer.insert(0, "-")
                for elem in self.printer:
                    self.text.append(elem)
                self.displayer()
            if "".join(self.text) != "":
                self.SetStatus(None, "  Operation:  " + str("".join(self.text)))               

    def OnPoint(self, event):
        if "." not in self.printer:
            self.text.append(".")
            self.printer.append(".")
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))           
    
    def OnCanc(self, event):
        self.text.clear()
        self.printer.clear()
        self.printer.append("0")
        self.displayer()
        self.SetDefaultStatus(None)
    
    def OnPlus(self, event):
        self.AddOperator(" + ")
    
    def OnMinus(self, event):
        self.AddOperator(" - ")
    
    def OnMultiply(self, event):
        self.AddOperator(" * ")    
    
    def OnDivide(self, event):
        self.AddOperator(" / ")
    
    def OnEqual(self, event):
        
        operators = [" + ", " - ", " * ", " / "]
        
        try:
            x = "".join(self.text)
            text = x
            if x == "":
                pass
            elif "\u0025" in x:
                x = x.split("\u0025")
                if len(x) == 2 and x[1] == "":
                    x = str(x[0])
                    for elem in operators:
                        if elem in x:
                            x = x.split(elem)
                            a = x[0]
                            b = x[1]
                            y = (float(a) * float(b)) / 100
                            x.pop(-1)
                            x.append(str(y))
                            x = eval(str(elem.join(x)))
                            operation = "".join(self.text) + " = " + str(x)
                            self.HistoryUpgrade(operation)
                            self.printer.clear()
                            self.text.clear()
                            self.text.append(str(x))
                            self.printer.append(str(x))
                            self.displayer()
                            self.SetTemporaryStatus("  Result: " + str(x), 3000)                  
                            self.new = True
                else:
                    self.text.clear()
                    self.printer.clear()
                    self.printer.append("ERROR  ")
                    self.displayer()
                    self.printer.append("0")
                    self.SetTemporaryStatus("ERROR: Invalid sintax", 3000)
                    if self.settings["HistorySave"] == "All":
                        operation = text + " = ERROR: Invalid sintax"
                        self.HistoryUpgrade(operation)  
                    self.new = True                             
            elif "\u2030" in x:
                print("ok")
                x = x.split("\u2030")
                if len(x) == 2 and x[1] == "":
                    x = str(x[0])
                    for elem in operators:
                        if elem in str(x):
                            x = x.split(elem)
                            a = x[0]
                            b = x[1]
                            y = (float(a) * float(b)) / 1000
                            x.pop(-1)
                            x.append(str(y))
                            x = eval(str(elem.join(x)))
                            operation = "".join(self.text) + " = " + str(x)
                            self.HistoryUpgrade(operation)
                            self.printer.clear()
                            self.text.clear()
                            self.text.append(str(x))
                            self.printer.append(str(x))
                            self.displayer()
                            self.SetTemporaryStatus("  Result: " + str(x), 3000)                  
                            self.new = True  
                else:
                    self.text.clear()
                    self.printer.clear()
                    self.printer.append("ERROR  ")
                    self.displayer()
                    self.printer.append("0")
                    self.SetTemporaryStatus("ERROR: Invalid sintax", 3000)
                    if self.settings["HistorySave"] == "All":
                        operation = text + " = ERROR: Invalid sintax"
                        self.HistoryUpgrade(operation)  
                    self.new = True                             
            elif "\u2031" in x:
                x = x.split("\u2031")
                if len(x) == 2 and x[1] == "":
                    x = str(x[0])
                    for elem in operators:
                        if elem in x:
                            x = x.split(elem)
                            a = x[0]
                            b = x[1]
                            y = (float(a) * float(b)) / 1000000
                            x.pop(-1)
                            x.append(str(y))
                            x = eval(str(elem.join(x)))
                            operation = "".join(self.text) + " = " + str(x)
                            self.HistoryUpgrade(operation)
                            self.printer.clear()
                            self.text.clear()
                            self.text.append(str(x))
                            self.printer.append(str(x))
                            self.displayer()
                            self.SetTemporaryStatus("  Result: " + str(x), 3000)                  
                            self.new = True                                
                else:
                    self.text.clear()
                    self.printer.clear()
                    self.printer.append("ERROR  ")
                    self.displayer()
                    self.printer.append("0")
                    self.SetTemporaryStatus("ERROR: Invalid sintax", 3000)
                    if self.settings["HistorySave"] == "All":
                        operation = text + " = ERROR: Invalid sintax"
                        self.HistoryUpgrade(operation)  
                    self.new = True            
            else:
                x = eval(str(x))
                operation = "".join(self.text) + " = " + str(x)
                self.HistoryUpgrade(operation)
                self.printer.clear()
                self.text.clear()
                self.text.append(str(x))
                self.printer.append(str(x))
                self.displayer()
                self.SetTemporaryStatus("  Result: " + str(x), 3000)                  
                self.new = True
        except SyntaxError:
            self.text.clear()
            self.printer.clear()
            self.printer.append("ERROR  ")
            self.displayer()
            self.printer.append("0")
            self.SetTemporaryStatus("ERROR: Invalid sintax", 3000)  
            if self.settings["HistorySave"] == "All":
                operation = text + " = ERROR: Invalid sintax"
                self.HistoryUpgrade(operation)            
            self.new = True
        except ZeroDivisionError:
            self.text.clear()
            self.printer.clear()
            self.printer.append("ERROR  ")
            self.displayer() 
            self.printer.append("0")
            self.SetTemporaryStatus("ERROR: Division by zero", 3000)
            if self.settings["HistorySave"] == "All":
                operation = text + " = ERROR: Division by zero"
                self.HistoryUpgrade(operation)            
            self.new = True            
    
    def OnMemoryPlus(self, event):
        if self.text != []:
            self.memory.append("+" + str(eval("".join(self.text))))
    
    def OnMemoryCall(self, event):
        self.text.append(str(eval("".join(self.memory))))
        self.printer.clear()
        self.printer.append(str(eval("".join(self.memory))))
        self.displayer()
    
    def OnMemoryCanc(self, event):
        self.memory.clear()
        self.memory.append("0")
    
    
################################################################################
################################################################################
    
    def OnBack(self, event):
        operators = [" / ", " * ", " + ", " - ", "**"]
        try:
            if self.text[-1] not in operators:
                self.text.pop(-1)
                self.printer.pop(-1)
                self.displayer()
                if "".join(self.text) != "":
                    self.SetStatus(None, "  Operation:  " + str("".join(self.text)))
                else:
                    self.SetDefaultStatus(None)
        except IndexError:
            pass
    
    def OnExp2(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer.append("**2")
        self.printer = list(str(eval("".join(self.printer))))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))        
    
    def OnExp3(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer.append("**3")
        self.printer = list(str(eval("".join(self.printer))))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))  
    
    def OnExpX(self, event):
        self.printer.append("**")
        self.text.append("**")
        self.printer.clear()

    def Root(self, number):
        for elem in self.printer:
            self.text.pop(-1)
            self.printer = list(str(pow(float("".join(self.printer)), 1/number)))
        for elem in self.printer:
            self.text.append(elem)
            self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))        
    
    def OnRoot2(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer = list(str(math.sqrt(float("".join(self.printer)))))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))
    
    def OnRoot3(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer = list(str(pow(float("".join(self.printer)), 1/3)))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))
    
    def OnRootX(self, event):
        aelf.rootx = True
    
    def OnSin(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer = list(str(math.sin(math.radians(int(float("".join(self.printer)))))))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))        
    
    def OnCos(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer = list(str(math.cos(math.radians(float("".join(self.printer))))))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))
    
    def OnSinh(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer = list(str(math.asin(float("".join(self.printer))) / math.pi * 180))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))
    
    def OnCosh(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer = list(str(math.acos(float("".join(self.printer))) / math.pi * 180))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))
    
    def OnReverse(self, event):
        for elem in self.printer:
            self.text.pop(-1)
        self.printer.insert(0, "1/")
        self.printer = list(str(eval("".join(self.printer))))
        for elem in self.printer:
            self.text.append(elem)
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))
    
    def OnGreekP(self, event):
        self.AddNumber("3.141592654")
        self.displayer()
    
    def OnPer100(self, event):
        self.printer.append("\u0025")
        self.text.append("\u0025")
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))   
    
    def OnPer1000(self, event):
        self.printer.append("\u2030")
        self.text.append("\u2030")
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))     
    
    def OnPerMilione(self, event):
        self.printer.append("\u2031")
        self.text.append("\u2031")
        self.displayer()
        if "".join(self.text) != "":
            self.SetStatus(None, "  Operation:  " + str("".join(self.text)))    


################################################################################
################################################################################
    
    
app = wx.App(False)
frame = MainWindow("Calculator")
app.MainLoop()
