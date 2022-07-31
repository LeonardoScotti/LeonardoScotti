
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView

class MainApp(App):
    
    def build(self):
        
        self.layout1 = BoxLayout()
        self.layout2 = BoxLayout()
        self.layout3 = BoxLayout()
        self.layout4 = BoxLayout()
        self.layout = BoxLayout()
        self.layout.orientation = "vertical"
        
        self.white = [255,255,255,1]
        self.black = [0,0,0,1]
        self.red = [255,0,0,1]
        self.yellow = [255,255,0,1]
        
        self.cards = {"yellow": 0, "red": 0, "black": 0,
                      "pyellow": 0, "pred": 0, "pblack": 0}
        
        self.timecount = 180
        self.fighting = False        
        
        self.score = Button(text="0 : 0", font_size=75*3, size_hint=(1, 2))
        self.time = Button(text="03:00", font_size=75*3, size_hint=(1, 2))
        self.startstop = Button(text="START", font_size=75*2, size_hint=(1, 2))
        self.startstop.background_color = [0, 255, 0, 1]   
        self.startstop.bind(on_press=self.start_stop)
        
        self.plus_dx = Button(text="+", font_size=50*2)
        self.plus_dx.color = [0,1,0,1]
        o1 = lambda x: self.plus(1, 0)
        self.plus_dx.bind(on_press=o1)
        self.minus_dx = Button(text="-", font_size=90*2)
        self.minus_dx.color = [1,0,0,1]
        o2 = lambda x: self.plus(-1, 0)
        self.minus_dx.bind(on_press=o2)
        self.double =  Button(text="doppio", font_size=30)
        o5 = lambda x: self.plus(1, 1)
        self.double.bind(on_press=o5)
        self.plus_sx = Button(text="+", font_size=50*2)
        self.plus_sx.color = [0,1,0,1]
        o3 = lambda x: self.plus(0, 1)
        self.plus_sx.bind(on_press=o3)
        self.minus_sx = Button(text="-", font_size=90*2)
        self.minus_sx.color = [1,0,0,1]
        o4 = lambda x: self.plus(0, -1)
        self.minus_sx.bind(on_press=o4)
        
        self.onemin = Button(text="1 min", font_size=25)
        t1 = lambda x: self.ctime("01")
        self.onemin.bind(on_press=t1)
        self.twomin = Button(text="2 min", font_size=25)
        t2 = lambda x: self.ctime("02")
        self.twomin.bind(on_press=t2)
        self.threemin = Button(text="3 min", font_size=25)
        t3 = lambda x: self.ctime("03")
        self.threemin.bind(on_press=t3)
        
        self.reset = Button(text="reset", font_size=25)
        self.reset.bind(on_press=self.total_reset)
        self.zero = Button(text="0:0", font_size=25)
        self.zero.bind(on_press=self.to_zero)
        self.priority = Button(text="priority", font_size=25)
        self.priority.bind(on_press=self.rpriority)
        
        self.yellow = Button(text="", font_size=60)
        self.yellow.background_color = [255,255,0,1]
        c1 = lambda x: self.card("yellow")
        self.yellow.bind(on_press=c1)
        self.red = Button(text="", font_size=60)
        self.red.background_color = [255,0,0,1]
        c2 = lambda x: self.card("red")
        self.red.bind(on_press=c2)
        self.black = Button(text="", font_size=60)
        self.black.background_color = [0,0,0,1]
        c3 = lambda x: self.card("black")
        self.black.bind(on_press=c3)
        self.pyellow = Button(text="P", font_size=60)
        self.pyellow.background_color = [255,255,0,1]
        c4 = lambda x: self.card("pyellow")
        self.pyellow.bind(on_press=c4)
        self.pred = Button(text="P", font_size=60)
        self.pred.background_color = [255,0,0,1]
        c5 = lambda x: self.card("pred")
        self.pred.bind(on_press=c5)
        self.pblack = Button(text="P", font_size=60)
        self.pblack.background_color = [0,0,0,1]
        c6 = lambda x: self.card("pblack")
        self.pblack.bind(on_press=c6)
        
        
        [self.layout1.add_widget(x) for x in [self.plus_dx, self.minus_dx, self.double, self.plus_sx, self.minus_sx]]
        [self.layout2.add_widget(x) for x in [self.threemin, self.twomin, self.onemin, self.reset, self.zero, self.priority]]
        [self.layout3.add_widget(x) for x in [self.yellow, self.red, self.black]]
        [self.layout4.add_widget(x) for x in [self.pyellow, self.pred, self.pblack]]
        
        self.layout.add_widget(self.score)
        self.layout.add_widget(self.time)
        self.layout.add_widget(self.layout1)
        self.layout.add_widget(self.startstop)
        self.layout.add_widget(self.layout2)
        self.layout.add_widget(self.layout3)
        self.layout.add_widget(self.layout4)
        
        #self.layout.background_color = [240/255, 240/255, 240/255, 1]
       
        return self.layout
        
        
    
    def on_start(self):
        Clock.schedule_interval(self.timer, 1)
        
    
    def timer(self, event):
        if self.fighting and self.timecount > 0:
            self.timecount-=1
            x = self.timecount//60
            y = str(self.timecount - x*60)
            if len(y) < 2:
                Y = "0" + y
            self.time.text = "0" + str(x) + ":" + y
    
    def start_stop(self, event):
        if self.fighting:
            self.startstop.text = "START"
            self.startstop.background_color = [0, 255, 0, 1]
            self.fighting = False
        else:
            self.startstop.text = "STOP"
            self.startstop.background_color = [255,0,0,1]            
            self.fighting = True
    
    def plus(self, sx, dx):
        x = self.score.text.split(" : ")
        s = int(x[0]) + sx
        d = int(x[1]) + dx
        if s < 0:
            s = 0
        if d < 0:
            d = 0
        n = str(s) + " : " + str(d)
        self.score.text = n

    def ctime(self, mins):
        self.timecount = int(mins) * 60
        self.time.text = mins + ":00"
    
    def total_reset(self, event):
        self.score.text = "0 : 0"
        self.time.text = "03:00"
        self.cards = {"yellow": 0, "red": 0, "black": 0,
                      "pyellow": 0, "pred": 0, "pblack": 0}

    
    def to_zero(self, event):
        self.score.text = "0 : 0"

    
    def rpriority(self, event):
        x = ["LEFT", "RIGHT"][random.randint(0,1)]
        popup = ModalView(size_hint=(None, None), size=(400, 400))
        pop_layout = BoxLayout()
        pop_layout.orientation = "vertical"
        label = Label(text=x, font_size=90, size_hint=(1, .85))
        pop_layout.add_widget(label)
        button =  Button(text="close", font_size=25, size_hint=(1, .25))
        button.bind(on_press=popup.dismiss)
        pop_layout.add_widget(button)
        popup.add_widget(pop_layout)
        popup.open()
    
    def card(self, colour):
        label = Button(text="", font_size=150*5)
        if "p" in colour:
            label.text = "P"
        card = ModalView(size_hint=(1, 1))
        c= {"yellow": [255,255,0,1],
            "red": [255,0,0,1],
            "black": [0,0,0,1]}[colour.strip("p")]
        label.background_color = c
        label.bind(on_press=card.dismiss)
        card.add_widget(label)
        card.open()
    

if __name__ == '__main__':
    app = MainApp()
    app.run()    
