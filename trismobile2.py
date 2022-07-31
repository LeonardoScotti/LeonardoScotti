
from copy import deepcopy

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout

class MainApp(App):
    
    def build(self):
        
        self.layout1 = BoxLayout()
        self.layout2 = BoxLayout()
        self.layout3 = BoxLayout()
        self.blayout = BoxLayout()
        self.layout = BoxLayout()
        self.layout.orientation = "vertical"

        
        self.white = [255,255,255,1]
        self.black = [0,0,0,1]
        self.red = [255,0,0,1]
        self.blue = [0,0,255,1]
        self.yellow = [255,255,0,1]
        self.grey = [1,1,1,1]
        
        self.turn = "X"
        self.nturns = 0
        self.finished = False
        self.m = 0
        self.ca = True

        self.info = Button(text="", font_size=75)
        self.restart = Button(text="RESTART", font_size=75)
        self.restart.bind(on_press=self.clear_board)  
        self.mode = Button(text="MODE", font_size=75) 
        self.mode.bind(on_press=self.select_mode)  
        
        self.info.text = "It's X's turn"
        self.info.background_color = self.red
        self.restart.background_color = self.red        
        self.mode.background_color = self.red        

        self.btn1 = Button(text="", background_color=self.white, font_size=100)
        cb1 = lambda x: self.on_board_click([0,0])
        self.btn1.bind(on_press=cb1)       
        self.btn2 = Button(text="", background_color=self.white, font_size=100)
        cb2 = lambda x: self.on_board_click([0,1])
        self.btn2.bind(on_press=cb2)       
        self.btn3 = Button(text="", background_color=self.white, font_size=100)
        cb3 = lambda x: self.on_board_click([0,2])
        self.btn3.bind(on_press=cb3)       
        self.btn4 = Button(text="", background_color=self.white, font_size=100)
        cb4 = lambda x: self.on_board_click([1,0])
        self.btn4.bind(on_press=cb4)       
        self.btn5 = Button(text="", background_color=self.white, font_size=100)
        cb5 = lambda x: self.on_board_click([1,1])
        self.btn5.bind(on_press=cb5)       
        self.btn6 = Button(text="", background_color=self.white, font_size=100)
        cb6 = lambda x: self.on_board_click([1,2])
        self.btn6.bind(on_press=cb6)       
        self.btn7 = Button(text="", background_color=self.white, font_size=100)
        cb7 = lambda x: self.on_board_click([2,0])
        self.btn7.bind(on_press=cb7)       
        self.btn8 = Button(text="", background_color=self.white, font_size=100)
        cb8 = lambda x: self.on_board_click([2,1])
        self.btn8.bind(on_press=cb8)       
        self.btn9 = Button(text="", background_color=self.white, font_size=100)
        cb9 = lambda x: self.on_board_click([2,2])
        self.btn9.bind(on_press=cb9)       

        
        self.board = [[self.btn1, self.btn2, self.btn3],
                      [self.btn4, self.btn5, self.btn6],
                      [self.btn7, self.btn8, self.btn9]]
        

        [self.layout1.add_widget(x) for x in self.board[0]]
        [self.layout2.add_widget(x) for x in self.board[1]]
        [self.layout3.add_widget(x) for x in self.board[2]]
        
        self.blayout.add_widget(self.restart)
        self.blayout.add_widget(self.mode)

        self.layout.add_widget(self.info)
        self.layout.add_widget(self.layout1)
        self.layout.add_widget(self.layout2)
        self.layout.add_widget(self.layout3)
        self.layout.add_widget(self.blayout)

        
        return self.layout
        
        

    def select_mode(self, event):

        def set(mode):
            print(mode)
            if mode == 0:
                self.m = 0
            elif mode == 1:
                self.m = 1
            popup.dismiss()
            self.clear_board(None)

        popup = ModalView(size_hint=(None, None), size=(400, 400)) 
        pop_layout = BoxLayout()
        pop_layout.orientation = "vertical"
        duo = Button(text="1v1", font_size=83)
        l1 = lambda x: set(0)
        duo.bind(on_press=l1)       
        pop_layout.add_widget(duo)
        pc = Button(text="1 v/s PC", font_size=75)
        l2 = lambda x: set(1)
        pc.bind(on_press=l2)       
        pop_layout.add_widget(pc)
        popup.add_widget(pop_layout)
        print(duo.background_color)
        popup.open()
    
    def on_board_click(self, cords, pc=False):
        
        if self.board[cords[0]][cords[1]].text not in ["X", "O"] and not self.finished and (self.ca or pc):    
            self.board[cords[0]][cords[1]].text = self.turn
            self.board[cords[0]][cords[1]].background_color = {"X": self.red, "O": self.blue}[self.turn]
            self.turn = [x for x in ["X", "O"] if x != self.turn][0]
            self.nturns +=1
            if self.terminal() not in ["X", "O", "Tie"]:
                self.info.text = f"It's {self.turn}'s turn"
                self.info.background_color = {"X": self.red, "O": self.blue}[self.turn]
                self.restart.background_color = {"X": self.red, "O": self.blue}[self.turn]
                self.mode.background_color = {"X": self.red, "O": self.blue}[self.turn]
                if self.turn == "O" and self.m == 1:
                    self.ca = False
                    bo = [
                        [self.board[0][0].text, self.board[0][1].text, self.board[0][2].text],
                        [self.board[1][0].text, self.board[1][1].text, self.board[1][2].text],
                        [self.board[2][0].text, self.board[2][1].text, self.board[2][2].text]]
                    self.on_board_click(self.minmax(bo), True)
                else:
                    self.ca = True


    def clear_board(self, z):

        for y in self.board:
            for x in y:
                x.text = ""
                x.background_color = self.white
        self.turn = "X"
        self.nturns = 0
        self.info.text = "It's X's turn"
        self.info.background_color = self.red
        self.restart.background_color = self.red
        self.mode.background_color = self.red
        self.finished = False
        self.ca = True

    def winner(self):
        
        r = [[False, None]]
        r += [[x, [self.btn1, self.btn2, self.btn3]] for x in ["X", "O"] if self.btn1.text == self.btn2.text == self.btn3.text == x]
        r += [[x, [self.btn4, self.btn5, self.btn6]] for x in ["X", "O"] if self.btn4.text == self.btn5.text == self.btn6.text == x]
        r += [[x, [self.btn7, self.btn8, self.btn9]] for x in ["X", "O"] if self.btn7.text == self.btn8.text == self.btn9.text == x]
        r += [[x, [self.btn1, self.btn4, self.btn7]] for x in ["X", "O"] if self.btn1.text == self.btn4.text == self.btn7.text == x]
        r += [[x, [self.btn2, self.btn5, self.btn8]] for x in ["X", "O"] if self.btn2.text == self.btn5.text == self.btn8.text == x]
        r += [[x, [self.btn3, self.btn6, self.btn9]] for x in ["X", "O"] if self.btn3.text == self.btn6.text == self.btn9.text == x]
        r += [[x, [self.btn1, self.btn5, self.btn9]] for x in ["X", "O"] if self.btn1.text == self.btn5.text == self.btn9.text == x]
        r += [[x, [self.btn3, self.btn5, self.btn7]] for x in ["X", "O"] if self.btn3.text == self.btn5.text == self.btn7.text == x]
        
        return r[-1]
        
    
    def terminal(self):   

        winner, btns = self.winner()
        if winner == "X":
            self.info.text = "X Wins"
            self.info.background_color = self.red
            self.restart.background_color = self.red
            self.mode.background_color = self.red
            self.finished = True
            for r in self.board:
                for b in r:
                    if b not in btns and b.background_color != self.white:
                        b.background_color = self.grey
            return "O"
        elif winner == "O":
            self.info.text = "O Wins"
            self.info.background_color = self.blue   
            self.restart.background_color = self.blue
            self.mode.background_color = self.blue
            self.finished = True 
            for r in self.board:
                for b in r:
                    if b not in btns and b.background_color != self.white:
                        b.background_color = self.grey
            return "X"
        elif self.nturns == 9:
            self.info.text = "It's a Tie"
            self.info.background_color = self.yellow  
            self.restart.background_color = self.yellow
            self.mode.background_color = self.yellow
            self.finished = True
            return "Tie"

    

    def actions(self, board):
        
            possible_actions = []
            row = -1
            column = -1
            
            for line in board:
                row +=1
                for elem in line:
                    column +=1
                    if elem == "":
                        cordinate = (row, column)
                        possible_actions.append(cordinate)
                column = -1 
                    
            return possible_actions


  
    def result(self, board, action, operator="O"):
            
        x = deepcopy(board)
        x[action[0]][action[1]] = operator
        
        return x
        
    
    def winner2(self, board):
        
        r = [None]
        r += [x for x in ["X", "O"] if board[0][0] == board[0][1] == board[0][2] == x]
        r += [x for x in ["X", "O"] if board[1][0] == board[1][1] == board[1][2] == x]
        r += [x for x in ["X", "O"] if board[2][0] == board[2][1] == board[2][2] == x]
        r += [x for x in ["X", "O"] if board[0][0] == board[1][0] == board[2][0] == x]
        r += [x for x in ["X", "O"] if board[0][1] == board[1][1] == board[2][1] == x]
        r += [x for x in ["X", "O"] if board[0][2] == board[1][2] == board[2][2] == x]
        r += [x for x in ["X", "O"] if board[0][0] == board[1][1] == board[2][2] == x]
        r += [x for x in ["X", "O"] if board[0][2] == board[1][1] == board[2][0] == x]
        
        return r[-1]
  
    def terminal2(self, board):
        
        win =  self.winner2(board)

        if win != None:
            return True
        else:
            s = []
            [[(s.append(e)) for e in r] for r in board]
            if "" not in s:
                return True
            else:
                return False
      
  
    def utility(self, board):
 
        win =  self.winner2(board)
        
        if win == None:
            return 0
        elif win == "X":
            return -1
        elif win == "O":
            return 1


    def minmax(self, board):
                   
        o_moves = {a: 0 for a in self.actions(board)}
        f_moves = []
        w_moves = []
        iterations = {a: 0 for a in self.actions(board)}

        def godeep(board, move, o_action):
            iterations[o_action]+=1
            b = self.result(board, move, "O") #result of current's move
            if self.terminal2(b):
                u = self.utility(b)
                o_moves[o_action] += u
                if u == 1 and iterations[o_action] == 1:
                    w_moves.append(o_action)
            else:
                moves = self.actions(b) #opponent's possible moves after current's move
                for m in moves:
                    b1 = self.result(b, m, "X") #result of opponent's move
                    if self.terminal2(b1):
                        u = self.utility(b1)
                        o_moves[o_action] += u 
                        if u == -1 and iterations[o_action] == 1:
                            f_moves.append(o_action)
                    else:
                        for m1 in self.actions(b1): #current's possible moves after opponent's move
                            godeep(b1, m1, o_action)
            
                    
        for action in o_moves:
            godeep(board, action, action)

        print(o_moves, f_moves, iterations)
        if len(w_moves) > 0:
            return w_moves[0]
        else:
            r = {m: o_moves[m] for m in o_moves if m not in f_moves}
            return max(r, key=r.get)




if __name__ == '__main__':
    app = MainApp()
    app.run()    
