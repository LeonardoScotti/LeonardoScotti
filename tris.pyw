
import wx
import time
import copy
import socket
import random

class Socket():
    
    def __init__(type, port=None):
        
        self.type = type
        
        if port == None:
            self.port = ('127.0.0.1', 50000)
        else:
            self.port = port        

        if self.type == "server":
            self.operator="X"
            self.comms_socket = socket.socket()
            self.comms_socket.bind(self.port)
            self.comms_socket.listen(10)
            self.connection, self.address = self.comms_socket.accept()        
        elif self.type == "client":
            self.operator="O"
            self.comms_socket = socket.socket()
            self.comms_socket.connect(self.port)            
        
    
    def MainLoop():
        
        while True:
            if self.type == "server":
                data = connection.recv(4096).decode("UTF-8")
            else:
                data = comms_socket.send(bytes(send_data, "UTF-8"))            
        
        return data
        

    def send(data):
        
        if self.type == "server":
            self.connection.send(bytes(send_data, "UTF-8"))
        else:
            self.comms_socket.send(bytes(send_data, "UTF-8"))
        
    
class AI():    
    
    def get_current_board(self, window):
        
        board = [[window.btn1.GetLabel(), window.btn2.GetLabel(), window.btn3.GetLabel()],
                [window.btn4.GetLabel(), window.btn5.GetLabel(), window.btn6.GetLabel()],
                [window.btn7.GetLabel(), window.btn8.GetLabel(), window.btn9.GetLabel()]]
        
        return board
        
    
    def player(self, board):
        
        players = {"X": 0, "O": 0}
        
        for line in board:
            
            for elem in line:
                
                if elem == "X":
                    
                    players["X"]+=1
                    
                elif elem == "O":
                    
                    players["O"]+=1
                    
                
            
        
        return min(players)
        
    
    
    def actions(self, board):
        
        #Returns set of all possible actions (i, j) available on the board.
        
        possible_actions = []
        row = -1
        column = -1
        
        for line in board:
            
            row +=1
            
            for elem in line:
                
                column +=1
                
                if elem == "":
                    
                    cord = (row, column)
                    possible_actions.append(cord)
                    
                
            
            column = -1
            
        
        return possible_actions
        
    
    
    
    def result(self, board, action, operator="O"):
        
        #Returns the board that results from making move (i, j) on the board.
        
        x = copy.deepcopy(board)
        
        x[action[0]][action[1]] = operator
        
        return x
        
    
    
    def winner(self, board):
        
        #Returns the winner of the game, if there is one.
     
        def three_X(board):
            if board[0][0] == board[0][1] == board[0][2] == "X":
                return True
            if board[1][0] == board[1][1] == board[1][2] == "X":
                return True
            if board[2][0] == board[2][1] == board[2][2] == "X":
                return True
            if board[0][0] == board[1][0] == board[2][0] == "X":
                return True
            if board[0][1] == board[1][1] == board[2][1] == "X":
                return True
            if board[0][2] == board[1][2] == board[2][2] == "X":
                return True
            if board[0][0] == board[1][1] == board[2][2] == "X":
                return True
            if board[0][2] == board[1][1] == board[2][0] == "X":
                return True
            
        def three_O(board):
            if board[0][0] == board[0][1] == board[0][2] == "O":
                return True
            if board[1][0] == board[1][1] == board[1][2] == "O":
                return True
            if board[2][0] == board[2][1] == board[2][2] == "O":
                return True
            if board[0][0] == board[1][0] == board[2][0] == "O":
                return True
            if board[0][1] == board[1][1] == board[2][1] == "O":
                return True
            if board[0][2] == board[1][2] == board[2][2] == "O":
                return True
            if board[0][0] == board[1][1] == board[2][2] == "O":
                return True
            if board[0][2] == board[1][1] == board[2][1] == "O":
                return True
        
        def Tie(board):
            if board[0][0] == board[0][1] == board[0][2] == board[1][0] == board[1][1] == board[1][2] == board[2][0] == board[2][1] == board[2][2] == "O":            
                
                return True
                
            else:
                
                return False
                
            
        
        if three_X(board) == True:
            return "X"
        elif three_O(board) == True:
            return "O"
        elif Tie(board) == True:
            return "Tie"
        else:
            return None
      
    
    def terminal(self, board):
        
        #Returns True if game is over, False otherwise.
        
        win =  self.winner(board)
        
        if win != None:
            return True
        else:
            return False
        

    
    
    
    def utility(self, board):
        
        #Returns -1 if X has won the game, 1 if O has won, 0 otherwise.
        
        win =  self.winner(board)
        
        if win == "X":
            return -1
        elif win =="O":
            return 1
        else:
            return 0
        
    
    
    
    def minmax(self, board):
        
        #Returns the optimal action for the current player on the board.
        
        act = self.actions(board)
        allresults = {}
        results = []
        
        
        for action in act:
            x = copy.deepcopy(board)
            res1 = self.result(x, action, "O")
            res2 = self.result(x, action, "X")
            allresults[str(res1)] = action
            allresults[str(res2)] = action
            results.append(res1)
            results.append(res2)
            
       
        wins = [allresults[str(elem)] for elem in results if self.utility(elem) == 1]
        losts = [allresults[str(elem)] for elem in results if self.utility(elem) == -1]
        ties = [allresults[str(elem)] for elem in results if self.utility(elem) == 0]
      
        if len(wins) > 0:
            
            return wins
         
        elif len(losts) > 0:
            
            return losts
            
        else:
            
            return ties
            
        
        
    
    def play(self, window, level):
        
        
        levels = {"easy": 2,
                  "medium": 4,
                  "hard": 6,
                  "impossible": 8}
        
        current_board = self.get_current_board(window)
        turn = self.player(current_board)
        
        possible_actions = self.minmax(current_board)
        if len(possible_actions) > 1:
            act = possible_actions[random.randint(0, int(len(possible_actions))-1)]
        else:
            act = possible_actions[0]
        return act
        

class MainWindow(wx.Frame):
    
    
    def __init__(self, title):
      
        import ctypes
        myappid = 'tris.scottiltd'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)      
      
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=title, size=(240,250), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        
        self.font = wx.Font(13, wx.DEFAULT, wx.BOLD, wx.NORMAL, underline = False, faceName ="")
        
        self.font1 = wx.Font(23, wx.DEFAULT, wx.BOLD, wx.NORMAL, underline = False, faceName ="")

        self.turn = 0
        self.operator = ["X", "O", "X", "O", "X", "O", "X", "O", "X", "O"]
        self.mode = "user"
        self.level = "easy"
        self.new = False
        
################################################################################
        
        self.optionsMenu = wx.Menu()
        self.restart = self.optionsMenu.Append(100, "restart", "start a new game")
        self.Bind(wx.EVT_MENU, self.OnRestart, self.restart)
        self.exit = self.optionsMenu.Append(101, "exit", "leave the game")       
        self.modeMenu = wx.Menu()
        self.ai = self.modeMenu.AppendRadioItem(200, "Ai", "play againist AI")
        self.Bind(wx.EVT_MENU, self.OnAI, self.ai)
        self.user = self.modeMenu.AppendRadioItem(201, "User", "play againist Computer User")
        self.Bind(wx.EVT_MENU, self.OnUser, self.user)
        self.online = self.modeMenu.AppendRadioItem(202, "Online", "play online")
        if self.mode == "ai":
            self.ai.Check()
        elif self.mode == "user":
            self.user.Check()
        elif self.mode == "online":
            self.online.Check()
        self.infoMenu = wx.Menu()
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.optionsMenu, "options")
        self.menubar.Append(self.modeMenu, "mode")
        self.menubar.Append(self.infoMenu, "?")
        self.SetMenuBar(self.menubar)
        
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText("  Welcome to Tris: Have Fun")
        
        
        self.SetIcon(wx.Icon('C:/Users/Barbara/Desktop/python/tris/favicon.ico'))
        
        
        self.accel_tab = wx.AcceleratorTable([wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('r'), 100),
                                              wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('q'), wx.ID_EXIT)])
        
        self.SetAcceleratorTable(self.accel_tab)
        
################################################################################
        
        self.btn1 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn1.Bind(wx.EVT_BUTTON, lambda event, btn="1": self.OnBtn(event, btn))
        self.btn2 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn2.Bind(wx.EVT_BUTTON, lambda event, btn="2": self.OnBtn(event, btn))
        self.btn3 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn3.Bind(wx.EVT_BUTTON, lambda event, btn="3": self.OnBtn(event, btn))
        self.btn4 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn4.Bind(wx.EVT_BUTTON, lambda event, btn="4": self.OnBtn(event, btn))
        self.btn5 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn5.Bind(wx.EVT_BUTTON, lambda event, btn="5": self.OnBtn(event, btn))
        self.btn6 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn6.Bind(wx.EVT_BUTTON, lambda event, btn="6": self.OnBtn(event, btn))
        self.btn7 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn7.Bind(wx.EVT_BUTTON, lambda event, btn="7": self.OnBtn(event, btn))
        self.btn8 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn8.Bind(wx.EVT_BUTTON, lambda event, btn="8": self.OnBtn(event, btn))
        self.btn9 = wx.Button(self, id=wx.ID_STATIC, label="")
        self.btn9.Bind(wx.EVT_BUTTON, lambda event, btn="9": self.OnBtn(event, btn))
        
################################################################################
        
        self.board = [[self.btn1, self.btn2, self.btn3],
                      [self.btn4, self.btn5, self.btn6],
                      [self.btn7, self.btn8, self.btn9]]        
        
################################################################################
        
        self.finish = wx.Button(self, id=wx.ID_STATIC, size=(240, 0))
        self.finish.SetFont(self.font1)
        self.btnrestart = wx.Button(self, id=wx.ID_STATIC, label="restart", size=(120, 20))
        self.btnrestart.Bind(wx.EVT_BUTTON, self.OnRestart)
        self.btnexit = wx.Button(self, id=wx.ID_STATIC, label="exit", size=(120, 50))
        self.btnexit.Bind(wx.EVT_BUTTON, self.OnExit)
        
################################################################################
        
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.buttons1 = [self.btn1, self.btn4, self.btn7]
        for x in range(len(self.buttons1)):
            self.buttons1[x].SetFont(self.font)
            self.sizer1.Add(self.buttons1[x], 1, wx.EXPAND)         
       
        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.buttons2 = [self.btn2, self.btn5, self.btn8]
        for x in range(len(self.buttons2)):
            self.buttons2[x].SetFont(self.font)
            self.sizer2.Add(self.buttons2[x], 1, wx.EXPAND) 
        
        self.sizer3 = wx.BoxSizer(wx.VERTICAL)
        self.buttons3 = [self.btn3, self.btn6, self.btn9]
        for x in range(len(self.buttons3)):
            self.buttons3[x].SetFont(self.font)
            self.sizer3.Add(self.buttons3[x], 1, wx.EXPAND) 
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizers = [self.sizer1, self.sizer2, self.sizer3]
        for x in range(len(self.sizers)):
            self.sizer.Add(self.sizers[x], 0, wx.EXPAND)         
        
################################################################################
    
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons4 = [self.btnrestart, self.btnexit]
        for x in range(len(self.buttons4)):
            self.buttons4[x].SetFont(self.font)
            self.sizer4.Add(self.buttons4[x], 1, wx.EXPAND) 
        
        self.finish_sizer = wx.BoxSizer(wx.VERTICAL)
        self.finish_sizer.Add(self.finish, 1, wx.EXPAND)
        self.finish_sizer.Add(self.sizer4, 0, wx.EXPAND)
        
################################################################################
        
        self.parent_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.parent_sizer.Add(self.sizer, 0, wx.EXPAND)
        self.parent_sizer.Add(self.finish_sizer, 0, wx.EXPAND)        
        
################################################################################
        
        self.SetSizer(self.parent_sizer)
        self.Show(True)
        
################################################################################
        

    def timeout(self, time, target):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, target, self.timer)
        self.timer.Start(int(time))
    
    def SetDefaultStatus(self, event):
        self.statusbar.SetStatusText("  Welcome to Tris: Have Fun")   
        try:
            self.timer.Stop()
        except:
            pass
    
    def SetTemporaryStatus(self, status, time):
        self.statusbar.SetStatusText(status)
        self.timeout(time, self.SetDefaultStatus)
    
    def SetStatus(self, event, status):
        self.statusbar.SetStatusText(status)    

################################################################################
    
    def winner(self):

        def three_X(self):
            if self.btn1.GetLabel() == self.btn2.GetLabel() == self.btn3.GetLabel() == "X":
                btns = [self.btn1, self.btn2, self.btn3]
                for elem in btns:
                    pass
                return True
            elif self.btn4.GetLabel() == self.btn5.GetLabel() == self.btn6.GetLabel() == "X":
                return True
            elif self.btn7.GetLabel() == self.btn8.GetLabel() == self.btn9.GetLabel() == "X":
                return True
            elif self.btn1.GetLabel() == self.btn4.GetLabel() == self.btn7.GetLabel() == "X":
                return True
            elif self.btn2.GetLabel() == self.btn5.GetLabel() == self.btn8.GetLabel() == "X":
                return True
            elif self.btn3.GetLabel() == self.btn6.GetLabel() == self.btn9.GetLabel() == "X":
                return True
            elif self.btn1.GetLabel() == self.btn5.GetLabel() == self.btn9.GetLabel() == "X":
                return True
            elif self.btn3.GetLabel() == self.btn5.GetLabel() == self.btn7.GetLabel() == "X":
                return True
        
        def three_O(self):
            if self.btn1.GetLabel() == self.btn2.GetLabel() == self.btn3.GetLabel() == "O":
                return True
            elif self.btn4.GetLabel() == self.btn5.GetLabel() == self.btn6.GetLabel() == "O":
                return True
            elif self.btn7.GetLabel() == self.btn8.GetLabel() == self.btn9.GetLabel() == "O":
                return True
            elif self.btn1.GetLabel() == self.btn4.GetLabel() == self.btn7.GetLabel() == "O":
                return True
            elif self.btn2.GetLabel() == self.btn5.GetLabel() == self.btn8.GetLabel() == "O":
                return True
            elif self.btn3.GetLabel() == self.btn6.GetLabel() == self.btn9.GetLabel() == "O":
                return True
            elif self.btn1.GetLabel() == self.btn5.GetLabel() == self.btn9.GetLabel() == "O":
                return True
            elif self.btn3.GetLabel() == self.btn5.GetLabel() == self.btn7.GetLabel() == "O":
                return True
        
        def Tie(self):
            
            if self.btn1.GetLabel() != "" and self.btn2.GetLabel() != "" and self.btn3.GetLabel() != "" and self.btn4.GetLabel() != "" and self.btn5.GetLabel() != "" and self.btn6.GetLabel() != "" and self.btn7.GetLabel() != "" and self.btn8.GetLabel() != "" and self.btn9.GetLabel() != "":
                
                return True
                
            
        
        if three_X(self) == True:
            return "X"
        elif three_O(self) == True:
            return "O"
        elif Tie(self) == True:
            return "Tie"
        else:
            return None
        
    
    
    def terminal(self):        
        winner = self.winner()
        if winner == "X":
            self.finish.SetLabel("X Wins")
            self.sizer.ShowItems(False)
            self.finish_sizer.ShowItems(True)
            self.parent_sizer.Layout()
            self.new = True
        elif winner == "O":
            self.finish.SetLabel("O Wins")
            self.sizer.ShowItems(False)
            self.finish_sizer.ShowItems(True)
            self.parent_sizer.Layout()
            self.new = True            
        elif winner == "Tie":
            self.finish.SetLabel("It's a Tie")
            self.sizer.ShowItems(False)
            self.finish_sizer.ShowItems(True)
            self.parent_sizer.Layout()
            self.new = True            
        else:
            pass

################################################################################
    
    def OnRestart(self, event):
        buttons = [self.btn1, self.btn2, self.btn3,
                   self.btn4, self.btn5, self.btn6,
                   self.btn7, self.btn8, self.btn9]
        for btn in buttons:
            btn.SetLabel("")
        self.turn = 0
        self.sizer.ShowItems(True)
        self.finish_sizer.ShowItems(False)
        self.parent_sizer.Layout()
    
    def OnExit(self, event):
        self.sizer.ShowItems(True)
        self.finish_sizer.ShowItems(False)
        self.parent_sizer.Layout()
    
    def OnAbout(self, event):
        pass
    
    def OnUser(self, event):
        self.user.Check()
        self.mode = "user"
        self.OnRestart(None)  
    
    def OnAI(self, event):
        self.ai.Check()
        self.mode = "ai"
        self.OnRestart(None)
    
    def OnOnline(self, event):
        self.online.Check()
        self.mode = "online"
        self.OnRestart(None) 
        global server
        server = Socket()
    
################################################################################
    
    def Move(self, btn, operator):
        if self.new == True:
            self.OnRestart(None)
            self.new = False
        btn.SetLabel(operator)
        self.parent_sizer.Layout()
        self.turn+=1
        self.terminal()
        if operator == "X" and self.mode == "ai" and self.turn < 9 and self.new == False:
            global ai
            move = ai.play(self, self.level)
            time.sleep(1)
            self.board[move[0]][move[1]].SetLabel("O")
            self.parent_sizer.Layout()            
            self.turn+=1
            self.terminal()
        elif operator == "X" and self.mode == "online":
            server = Socket()
            for elem in self.board:
                if btn in elem:
                    index = elem.index(btn)
            server.send(index)
            data = server.MainLoop()
            self.board[data[0]][data[1]].SetLabel("O")
            self.parent_sizer.Layout()            
            self.turn+=1
            self.terminal()  
        elif operator == "O" and self.mode == "online":
            server = Socket()
            for elem in self.board:
                if btn in elem:
                    index = elem.index(btn)
            server.send(index)
            data = server.MainLoop()
            self.board[data[0]][data[1]].SetLabel("X")
            self.parent_sizer.Layout()            
            self.turn+=1
            self.terminal()            
    
################################################################################
    
    def OnBtn(self, event, btn):
        x = {"1": self.btn1, "2": self.btn2, "3": self.btn3,
             "4": self.btn4, "5": self.btn5, "6": self.btn6,
             "7": self.btn7, "8": self.btn8, "9": self.btn9}[btn]
        
        if x.GetLabel() == "" or self.new == True:
            self.Move(x, self.operator[self.turn])            
    
################################################################################
    
ai = AI()
server = None
app = wx.App(False)
frame = MainWindow("Tris")
app.MainLoop()
