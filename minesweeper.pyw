
import wx
import random
 
class MainWindow(wx.Frame):
    
    def __init__(self, title):
        
        import ctypes
        myappid = 'minesweeper.scottiltd'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)        
        
        wx.Frame.__init__(self, None, wx.ID_ANY, title=title, style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        self.sizes = {"small": (466, 292),
                      "medium": (556, 412),
                      "big": (826, 502),
                      "fullscreen": None}
        
        self.mines = {"classic1": u"\u26ED", "classic2": u"\u26EF", 
                      "nuke": u"\u2622", "biological": u"\u2623", 
                      "pirate": u"\u2620", 
                      "nazi": u"\u2720", "communist": u"\u262D"}
        
        self.difficulty = {"small": {"veryeasy": 10, "easy": 15, "medium": 20, "hard": 25},
                           "medium": {"veryeasy": 20, "easy": 30, "medium": 40, "hard": 50},
                           "big": {"veryeasy": 50, "easy": 60, "medium": 70, "hard": 80},
                           "fullscreen": None}
        
        self.flag = u"\u26F3"
        self.smiles = {"sad": u"\u2639", "happy": u"\u263A"}
        self.grid = {"small": (7, 15), "medium": (11, 18), "big": (14, 27), "fullscreen": None}
        self.back = (243, 245, 153)
        
        self.settings = {"size": "small", "theme": "classic1", "difficulty": "veryeasy", "restartcode": "1"}
        
        self.colours = {"1": "blue", "2": "green", "3": "red", "4": "brown", "5": "red", "6": "blue", "7": "brown", "8": "blue"}
        
        wx.number_font1 = wx.Font(13, wx.DEFAULT, wx.BOLD, wx.NORMAL, underline = False, faceName ="")
        wx.number_font = wx.Font(18, wx.DEFAULT, wx.BOLD, wx.NORMAL, underline = False, faceName ="")
        
        self.finish = False
        self.first = True
        self.remainingmines = self.difficulty[self.settings["size"]][self.settings["difficulty"]]
        self.time = 0
        
################################################################################
##################################FRAME HEADER##################################
################################################################################
        
        self.optionsMenu = wx.Menu()
        self.restart = self.optionsMenu.Append(100, "restart\tCTRL+r", "                         start a new game")
        self.Bind(wx.EVT_MENU, self.OnRestart, self.restart)
        self.exit = self.optionsMenu.Append(101, "exit\tCTRL+q", "                          leave the game") 
        self.Bind(wx.EVT_MENU, self.OnExit, self.exit)
        
################################################################################
        
        self.modeMenu = wx.Menu()
        
        self.sizeMenu = wx.Menu()
        self.small = self.sizeMenu.AppendRadioItem(210, "small", "                                  Size: Small")
        self.Bind(wx.EVT_MENU, lambda event, size="small": self.OnSizeChange(event, size), self.small)
        self.medium = self.sizeMenu.AppendRadioItem(211, "medium", "                                  Size: Medium")
        self.Bind(wx.EVT_MENU, lambda event, size="medium": self.OnSizeChange(event, size), self.medium)
        self.big = self.sizeMenu.AppendRadioItem(212, "big", "                                  Size: Big")
        self.Bind(wx.EVT_MENU, lambda event, size="big": self.OnSizeChange(event, size), self.big)
        self.fullscreen = self.sizeMenu.AppendRadioItem(213, "fullscreen", "                                Size: Fullscreen")
        self.Bind(wx.EVT_MENU, lambda event, size="fullscreen": self.OnSizeChange(event, size), self.fullscreen)
        {"small": self.small, "medium": self.medium, "big": self.big, "fullscreen": self.fullscreen}[self.settings["size"]].Check()    
        
        self.themeMenu = wx.Menu()
        self.classic1 = self.themeMenu.AppendRadioItem(220, "classic1 \u26ED", "                           Theme: Classic1")
        self.Bind(wx.EVT_MENU, lambda event, theme="classic1": self.OnThemeChange(event, theme), self.classic1)
        self.classic2 = self.themeMenu.AppendRadioItem(221, "classic2 \u26EF", "                           Theme: Classic2")
        self.Bind(wx.EVT_MENU, lambda event, theme="classic2": self.OnThemeChange(event, theme), self.classic2)
        self.nuke = self.themeMenu.AppendRadioItem(222, "nuke \u2622", "                           Theme: Nuke")
        self.Bind(wx.EVT_MENU, lambda event, theme="nuke": self.OnThemeChange(event, theme), self.nuke)
        self.biological = self.themeMenu.AppendRadioItem(223, "biological \u2623", "                           Theme: Biological")
        self.Bind(wx.EVT_MENU, lambda event, theme="biological": self.OnThemeChange(event, theme), self.biological)
        self.pirate = self.themeMenu.AppendRadioItem(224, "pirate \u2620", "                           Theme: Pirate")
        self.Bind(wx.EVT_MENU, lambda event, theme="pirate": self.OnThemeChange(event, theme), self.pirate)
        self.nazi = self.themeMenu.AppendRadioItem(215, "nazi \u2720", "                           Theme: Nazi")
        self.Bind(wx.EVT_MENU, lambda event, theme="nazi": self.OnThemeChange(event, theme), self.nazi)
        self.communist = self.themeMenu.AppendRadioItem(226, "communist \u262D", "                           Theme: Communist")
        self.Bind(wx.EVT_MENU, lambda event, theme="communist": self.OnThemeChange(event, theme), self.communist)
        {"classic1": self.classic1, "classic2": self.classic2, "nuke": self.nuke, "biological": self.biological, "pirate": self.pirate, "nazi": self.nazi, "communist": self.communist}[self.settings["theme"]].Check()        
       
        self.difficultyMenu = wx.Menu()
        self.veryeasy = self.difficultyMenu.AppendRadioItem(230, "very easy", "                                Difficulty: Very Easy")
        self.Bind(wx.EVT_MENU, lambda event, difficulty="veryeasy": self.OnDifficultyChange(event, difficulty), self.veryeasy)
        self.easy = self.difficultyMenu.AppendRadioItem(231, "easy", "                                Difficulty: Easy")
        self.Bind(wx.EVT_MENU, lambda event, difficulty="easy": self.OnDifficultyChange(event, difficulty), self.easy)
        self.medium = self.difficultyMenu.AppendRadioItem(232, "medium", "                                Difficulty: Medium")
        self.Bind(wx.EVT_MENU, lambda event, difficulty="medium": self.OnDifficultyChange(event, difficulty), self.medium)
        self.hard = self.difficultyMenu.AppendRadioItem(233, "hard", "                                Difficuty: Hard")
        self.Bind(wx.EVT_MENU, lambda event, difficulty="hard": self.OnDifficultyChange(event, difficulty), self.hard)
        {"veryeasy": self.veryeasy, "easy": self.easy, "medium": self.medium, "hard": self.hard}[self.settings["difficulty"]].Check()
        
        self.modeMenu.AppendSubMenu(self.sizeMenu, "size")
        self.modeMenu.AppendSubMenu(self.themeMenu, "theme")       
        self.modeMenu.AppendSubMenu(self.difficultyMenu, "difficulty")
       
################################################################################
        
        self.settingsMenu = wx.Menu()
        
        self.restartgameif = wx.Menu()
        self.when_finished = self.restartgameif.AppendRadioItem(300, "Restart if the game is finished", "When change the mode restart the game only if the game is finished")
        self.Bind(wx.EVT_MENU, lambda event, code="2": self.OnRestartSettingsChange(event, code), self.when_finished)
        self.when_notstarted = self.restartgameif.AppendRadioItem(301, "Restart also if the game isn't started yet", "When change the mode restart the game only if the game is finished or not started")
        self.Bind(wx.EVT_MENU, lambda event, code="1": self.OnRestartSettingsChange(event, code), self.when_notstarted)
        self.when_playing = self.restartgameif.AppendRadioItem(302, "Restart always the game", "When change the mode restart always the game")
        self.Bind(wx.EVT_MENU, lambda event, code="0": self.OnRestartSettingsChange(event, code), self.when_playing)
        {"0": self.when_playing, "1": self.when_notstarted, "2": self.when_finished}[self.settings["restartcode"]].Check()
        self.settingsMenu.AppendSubMenu(self.restartgameif, "When Change Mode")
       
################################################################################
       
        self.infoMenu = wx.Menu()
        self.info = self.infoMenu.Append(400, "info\tCTRL+i", "         Information About Minesweeper")
        self.Bind(wx.EVT_MENU, self.OnAbout, self.info)
        
################################################################################
        
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.optionsMenu, "options")
        self.menubar.Append(self.modeMenu, "mode")
        self.menubar.Append(self.settingsMenu, "settings")
        self.menubar.Append(self.infoMenu, "?")
        self.SetMenuBar(self.menubar)
        
################################################################################
        
        self.accel_tab = wx.AcceleratorTable([wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('r'), 100),
                                              wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('q'), 101),                                         
                                              wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('i'), 400),                                         
                                              ])
        
        self.SetAcceleratorTable(self.accel_tab)                  
        
################################################################################
        
        self.statusbar = self.CreateStatusBar(3)
        self.SetStatusBarPane(1)
        self.statusbar.SetStatusWidths((-1, -3, -1))
        self.statusbar.SetStatusText("        Welcome to Minesweeper: Have Fun", 1) 
        self.statusbar.SetStatusText("0", 2)        
        
################################################################################
        
        self.SetIcon(wx.Icon('C:/Users/Barbara/Desktop/python/minesweeper/favicon.ico'))
        
################################################################################
        

        self.board = []
        self.representation = []
        self.sizer = wx.GridBagSizer()         
        self.CreateBoard()
        
        self.timeout(1000, self.OnTimer)
        self.statusbar.SetStatusText("            " + str(self.remainingmines), 0)
        self.MakeFullScreen()
        self.OnSizeChange(None, "small")
        
        self.Show(True)
        
        
################################################################################
      
    
    def timeout(self, time, target):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, target, self.timer)
        self.timer.Start(int(time))    
    
    def timeout1(self, time, target):
        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, target, self.timer1)
        self.timer1.Start(int(time))
    
    def SetDefaultStatus(self, event):
        self.statusbar.SetStatusText("        Welcome to Minesweeper: Have Fun", 1)   
        try:
            self.timer1.Stop()
        except:
            pass
    
    def SetTemporaryStatus(self, status, time):
        self.statusbar.SetStatusText(status, 1)
        self.timeout(time, self.SetDefaultStatus)
    
    def SetStatus(self, event, status):
        self.statusbar.SetStatusText(status, 1)    
    
################################################################################
    
    def OnTimer(self, event):
        
        if self.finish == False and self.first==False:
            self.time+=1
            self.statusbar.SetStatusText(str(self.time), 2) 
        
    
    def OnAbout(self, event):
        wx.MessageDialog( self, " A Complete, Fully Customizable and  Funny version of the Classic Minesweeper: \n\n - 7 different themes \n - 4 different levels of difficulty \n - 4 diferent screen-sizes \n\n developed by Leonardo Scotti \u2122, \n All right reserved", "About Calculator", wx.OK|wx.ICON_INFORMATION).ShowModal()      
    
    def OnRestart(self, event):
        self.CreateBoard()
        self.finish = False
        self.first = True
        self.time = 0
        self.remainingmines = self.difficulty[self.settings["size"]][self.settings["difficulty"]]
        self.SetDefaultStatus(None)
        self.statusbar.SetStatusText("0", 2)
    
    def OnExit(self, event):
        self.Finish()  
    
    def OnRestartSettingsChange(self, event, code):
        self.settings["restartcode"] == code
    
    def OnDifficultyChange(self, event, difficulty):
    
        self.settings["difficulty"] = difficulty
        if self.settings["restartcode"] == "0" or (self.settings["restartcode"] == "2" and self.first == True) or (self.settings["restartcode"] == "1" and (self.first == True or self.finish == True)):
            self.OnRestart(None)

    def OnThemeChange(self, event, theme):
        
        self.settings["theme"] = theme        
        if self.settings["restartcode"] == "0" or (self.settings["restartcode"] == "2" and self.first == True) or (self.settings["restartcode"] == "1" and (self.first == True or self.finish == True)):
            self.OnRestart(None)
        
    
    def OnSizeChange(self, event, size):
        
        self.settings["size"] = size
        self.SetSize(self.sizes[self.settings["size"]])
        self.OnRestart(None)
        
    
    def MakeFullScreen(self):
        
        width = int(wx.GetDisplaySize()[0])
        height = int(wx.GetDisplaySize()[1])
        
        self.sizes["fullscreen"] = wx.GetDisplaySize()
        self.grid["fullscreen"] = (int(height/20), int(width/20))

        x = self.grid["fullscreen"][0] * self.grid["fullscreen"][1]
        self.difficulty["fullscreen"] = {"veryeasy": int((x*13)/100), "easy": int((x*16)/100), "medium": int((x*19)/100), "hard": int((x*21)/100)}
        self.SetSize((466, 292))        
        
    
################################################################################
    
    def FindAll(self, pos):
        
        x = []
        
        if pos[1] < self.grid[self.settings["size"]][1]-1:
            x.append((pos[0], pos[1]+1))
        if pos[1] > 0:
            x.append((pos[0], pos[1]-1))
        
        if pos[0] > 0:
            if pos[1] < self.grid[self.settings["size"]][1]-1:            
                x.append((pos[0]-1, pos[1]+1))
            x.append((pos[0]-1, pos[1]))       
            if pos[1] > 0:
                x.append((pos[0]-1, pos[1]-1))
        
        if pos[0] < self.grid[self.settings["size"]][0]-1:
            if pos[1] < self.grid[self.settings["size"]][1]-1:            
                x.append((pos[0]+1, pos[1]+1))
            x.append((pos[0]+1, pos[1]))           
            if pos[1] > 0:
                x.append((pos[0]+1, pos[1]-1))                       
        
        return x
        
    
    def GetMinesCount(self, pos):
        
        mines = 0
        x = self.FindAll(pos)
        
        for elem in x:
            if self.representation[elem[0]][elem[1]] == self.mines[self.settings["theme"]]:
                mines+=1
        
        if mines != 0:
            return str(mines)
        else:
            return ""
     
    
    def CreateBoard(self):       

        self.board.clear()
        self.representation.clear()
        self.sizer.Clear(True)
        self.remainingmines = self.difficulty[self.settings["size"]][self.settings["difficulty"]]
        

        for r in range(self.grid[self.settings["size"]][0]):
            
            self.board.append([])
            self.representation.append([])
            
            for c in range(self.grid[self.settings["size"]][1]):

                self.board[r].append(wx.Button(self, id=wx.ID_ANY, size=(30, 30), label=""))
                self.sizer.Add(self.board[r][c], (r, c))
                self.representation[r].append("")
                self.board[r][c].Bind(wx.EVT_BUTTON, lambda event, cord = (r, c): self.OnLeftClick(event, cord))
                self.board[r][c].Bind(wx.EVT_RIGHT_DOWN, lambda event, cord = (r, c): self.OnRightClick(event, cord))
                
            
        
        targets = []
        range1 = self.grid[self.settings["size"]][0]
        range2 = self.grid[self.settings["size"]][1]
        
        while True:
            
            x = random.randint(0, range1-1)
            y = random.randint(0, range2-1)
            cords = (x, y)
            
            if cords not in targets:
                targets.append(cords)
            
            if len(targets) == self.difficulty[self.settings["size"]][self.settings["difficulty"]]:
                break
            
        
        for elem in targets:
            
            self.representation[elem[0]][elem[1]] = self.mines[self.settings["theme"]]
            
        
        for x in range(self.grid[self.settings["size"]][0]):
            
            for y in range(self.grid[self.settings["size"]][1]):
                
                if self.representation[x][y] != self.mines[self.settings["theme"]]:
                    
                    self.representation[x][y] = self.GetMinesCount((x, y))
                    
                
            
        
        self.SetSizer(self.sizer)         
        self.sizer.Layout()
        
        self.statusbar.SetStatusText("            " + str(self.remainingmines), 0)            
        
    
################################################################################
    
    def Finish(self):
        
        self.finish = True

        for x in range(self.grid[self.settings["size"]][0]):
            
            for y in range(self.grid[self.settings["size"]][1]):
                
                self.OnLeftClick(None, (x, y), True)
                
            
        
        for x in range(self.grid[self.settings["size"]][0]):
            
            for y in range(self.grid[self.settings["size"]][1]):
                
                if self.board[x][y].GetLabel() == self.flag and self.representation[x][y] != self.mines[self.settings["theme"]]:
                    
                    self.board[x][y].SetForegroundColour("black")
                    self.remainingmines+=1
                    
                
            
        
        self.statusbar.SetStatusText("            " + str(self.remainingmines), 0)
        if self.remainingmines > 0:
            self.SetStatus(None, "                                  You Lose")
        else:
            self.SetStatus(None, "                                   You Win")            
        
        
    
    
    def Terminal(self):
        
        count = self.difficulty[self.settings["size"]][self.settings["difficulty"]]
        
        for x in range(self.grid[self.settings["size"]][0]):
            
            for y in range(self.grid[self.settings["size"]][1]):
                
                if self.representation[x][y] == self.mines[self.settings["theme"]]:
                    
                    if self.board[x][y].GetLabel() == self.flag:
                        
                        count-=1
                        
                    else:
                        
                        return False
                        
                    
                    
                
            
        
        return True
        
    
    def ClearField(self, pos):
        
        stack = []
        targets = []
        targets.append(pos)

        def Expand(x):
            all = self.FindAll(x)
            for elem in all:
                if self.representation[elem[0]][elem[1]] == "":
                    if elem not in stack and elem not in targets:
                        stack.append(elem)
                if elem not in targets:
                    targets.append(elem)
                
            
        
        Expand(pos)
        
        while len(stack) > 0:
            Expand(stack[0])
            stack.pop(0)

        for elem in targets:
            if self.board[elem[0]][elem[1]].GetLabel() != self.flag:
                txt = str(self.representation[elem[0]][elem[1]])
                if txt == "":
                    self.board[elem[0]][elem[1]].SetLabel("")
                else:
                    self.board[elem[0]][elem[1]].SetLabel(txt)
                    self.board[elem[0]][elem[1]].SetForegroundColour(self.colours[txt])
                self.board[elem[0]][elem[1]].SetBackgroundColour(self.back)
                self.board[elem[0]][elem[1]].SetWindowStyle(wx.BORDER_NONE)
                self.sizer.Layout()            
            
        
    
    def OnLeftClick(self, event, pos, fwrite=False):
        
        self.first = False
        
        label = self.representation[pos[0]][pos[1]]
        
        if self.finish == True and fwrite == False:
            
            pass
            
        elif self.board[pos[0]][pos[1]].GetLabel() == self.flag:
            
            pass
         
        elif self.board[pos[0]][pos[1]].GetLabel() == self.mines[self.settings["theme"]]:
            
            pass
         
        elif label == "":
            self.board[pos[0]][pos[1]].SetLabel(label)            
            if self.finish == False:
                self.ClearField(pos)
            else:
                self.board[pos[0]][pos[1]].SetBackgroundColour(self.back)
                self.board[pos[0]][pos[1]].SetWindowStyle(wx.BORDER_NONE)
            self.sizer.Layout()                            
            
        elif label in ["1", "2", "3", "4", "5", "6", "7", "8"]:
           
            self.board[pos[0]][pos[1]].SetLabel(label)
            self.board[pos[0]][pos[1]].SetForegroundColour(self.colours[label])
            self.board[pos[0]][pos[1]].SetBackgroundColour(self.back)
            self.board[pos[0]][pos[1]].SetWindowStyle(wx.BORDER_NONE)                
            self.sizer.Layout()
         
        elif label == self.mines[self.settings["theme"]]:

            self.board[pos[0]][pos[1]].SetLabel(label)
            if self.finish == False:
                self.board[pos[0]][pos[1]].SetBackgroundColour("red")
            else:
                x = self.GetBackgroundColour()
                self.board[pos[0]][pos[1]].SetBackgroundColour(x)                
            self.board[pos[0]][pos[1]].SetForegroundColour("black")
            self.board[pos[0]][pos[1]].SetWindowStyle(wx.BORDER_NONE)  
            self.sizer.Layout()
            
            if self.finish == False:
                self.Finish()
            
        

    def OnRightClick(self, event, pos):
        
        if self.board[pos[0]][pos[1]].GetLabel() == "" and self.remainingmines > 0:
            self.board[pos[0]][pos[1]].SetLabel(self.flag)
            self.board[pos[0]][pos[1]].SetForegroundColour("red")
            self.board[pos[0]][pos[1]].SetWindowStyle(wx.BORDER_NONE) 
            self.remainingmines-=1
        elif self.board[pos[0]][pos[1]].GetLabel() == self.flag:
            self.board[pos[0]][pos[1]].SetLabel("")
            self.board[pos[0]][pos[1]].SetWindowStyle(0) 
            self.remainingmines+=1
        
        self.statusbar.SetStatusText("            " + str(self.remainingmines), 0)            
        
        if self.remainingmines == 0:

            if self.Terminal():
                
                self.Finish()
                
            
        
        self.sizer.Layout()
        
    
################################################################################    

app = wx.App(False)
frame = MainWindow("Minesweeper")
app.MainLoop()    
    