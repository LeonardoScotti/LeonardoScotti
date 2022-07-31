
import wx
import re
import sys
import smtplib

class MainWindow(wx.Frame):   
    
    def __init__(self, title, appid, icon):
        
        
        print(sys.argv)
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title=title + ": Contact Us", size=(460,550), style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))    
        
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)          
        
        self.SetIcon(wx.Icon(icon))
        
        self.prog = title
        self.content = False
        self.choice = wx.SingleChoiceDialog(self, f"Which type of message do you want to send to the \n{title}'s developers?", f"{title}: Contact Us", ["Bug Report", "Suggestion", "Proposal", "Question", "Something Else"]) 
        
        if self.choice.ShowModal() == wx.ID_CANCEL:
            self.Destroy()
            exit()
        else:
            if self.choice.GetStringSelection() == "Something Else":
                self.choice = wx.TextEntryDialog(self, f"Please specify which type of message do you want to send to the \n{title}'s developers", f"{title}: Contact Us",)
                if self.choice.ShowModal() == wx.ID_CANCEL:
                    self.Destroy()
                    exit()
                else:
                    self.content = self.choice.GetValue()                    
            else:
                self.content = self.choice.GetStringSelection()
        self.name = wx.StaticText(self, wx.ID_ANY, label="\nName:", size=(100, 45))      
        self.namevalue = wx.TextCtrl(self, wx.ID_ANY, size=(200, 23), style=wx.TE_PROCESS_ENTER)
        self.namevalue.Bind(wx.EVT_TEXT_ENTER, lambda event, control=0: self.OnNext(event, control))
        self.surname = wx.StaticText(self, wx.ID_ANY, label="\nSurname:", size=(100, 45))
        self.surnamevalue = wx.TextCtrl(self, wx.ID_ANY, size=(200, 23), style=wx.TE_PROCESS_ENTER)
        self.surnamevalue.Bind(wx.EVT_TEXT_ENTER, lambda event, control=1: self.OnNext(event, control))
        self.mail = wx.StaticText(self, wx.ID_ANY, label="\nE-Mail:", size=(100, 45))
        self.mailvalue = wx.TextCtrl(self, wx.ID_ANY, size=(300, 23), style=wx.TE_PROCESS_ENTER)
        self.mailvalue.Bind(wx.EVT_TEXT_ENTER, lambda event, control=2: self.OnNext(event, control))
        self.message = wx.StaticText(self, wx.ID_ANY, label="\nMessage:", size=(100, 45))
        self.messagevalue = wx.TextCtrl(self, wx.ID_ANY, size=(400, 200), style=wx.TE_MULTILINE | wx.TE_RICH | wx.TE_PROCESS_ENTER)
        self.send = wx.Button(self, wx.ID_ANY, label="Send", size=(100, 25))
        self.send.Bind(wx.EVT_BUTTON, self.OnSend)
        self.cancel = wx.Button(self, wx.ID_ANY, label="Cancel", size=(100, 25))
        self.cancel.Bind(wx.EVT_BUTTON, self.OnExit)        
        self.footer = wx.StaticText(self, wx.ID_ANY, label="\n", size=(100, 20))

        self.placers = [self.name, self.surname, self.mail, self.message, self.send, self.cancel, self.footer]        
        self.controls = [self.namevalue, self.surnamevalue, self.mailvalue, self.messagevalue, self.send]
        
        self.SetBackgroundColour((240, 240, 240, 455))                
        for elem in self.placers:
            elem.SetBackgroundColour((240, 240, 240, 455)) 
        
        self.bottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bottomsizer.Add(self.send, 0, wx.LEFT, 200)
        self.bottomsizer.Add(self.cancel, 0, wx.LEFT, 20)        
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.name, 0, wx.LEFT, 20)
        self.sizer.Add(self.namevalue, 0, wx.LEFT, 20)
        self.sizer.Add(self.surname, 0, wx.LEFT, 20)
        self.sizer.Add(self.surnamevalue, 0, wx.LEFT, 20)
        self.sizer.Add(self.mail, 0, wx.LEFT, 20)
        self.sizer.Add(self.mailvalue, 0, wx.LEFT, 20)
        self.sizer.Add(self.message, 0, wx.LEFT, 20)
        self.sizer.Add(self.messagevalue, 0, wx.LEFT, 20)
        self.sizer.Add(self.bottomsizer, 0, wx.TOP, 20,)
        self.sizer.Add(self.footer, 0)
        
        self.SetSizer(self.sizer)
        self.Show(True)
        

    def OnNext(self, event, control):

        try:
            self.controls[control+1].SetFocus()
        except IndexError:
            self.OnSubmit(None)
        
    
    def OnSend(self, event):

        title = self.prog
        content = self.content
        name = self.namevalue.GetValue()
        surname = self.surnamevalue.GetValue()
        mail = self.mailvalue.GetValue()
        content = self.content
        txt = self.messagevalue.GetValue()        
        
        if len(name) > 0 and len(surname) > 0 and len(mail) > 0 and re.match('^[a-zA-Z0-9_]*@[a-z]*\.[a-z]*$', mail) and len(txt) > 0:
        
            prog = wx.ProgressDialog("Sending", f"We are sending your {content}, please wait...", 18)            
        
            subject = f"Subject: {title} {content}\n"
            prog.Update(1)
            
            text = f"""
Content: {content}
About: {title}
From: 
      Name: {name}
      Surname: {surname}
      Email: {mail}

Message:

{txt}
    
    """
            prog.Update(2)
            
            message = subject + text
            prog.Update(3)            
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            prog.Update(4)
            server.ehlo()
            prog.Update(5)
            server.starttls()
            prog.Update(6)
            server.login("servicescottiltd@gmail.com", "Operatorpassword25")
            prog.Update(7)
            server.sendmail("servicescottiltd@gmail.com", "officialscottiltd@gmail.com", message)
            prog.Update(8)
            server.quit()
            prog.Update(9)
            
            subject = f"Subject: Re: {content}  about {title}\n"
            prog.Update(10)

            text = f"""
Hi {name} {surname},
thanks for your {content}, 
we have just recived it, and we will took it seriously,
one of our operators wil look at it as soon as possible and we will re-contact you back if necessary.
For any other comunication of any sort don't forget to write us again.

Leonardo Scotti

{title}'s Head Developer."""
            prog.Update(11)
            
            message = subject + text
            prog.Update(12)
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            prog.Update(13)
            server.ehlo()
            prog.Update(14)
            server.starttls()
            prog.Update(15)
            server.login("officialscottiltd@gmail.com", "Scottiltd25")
            prog.Update(16)
            server.sendmail("officialscottiltd@gmail.com", mail, message)
            prog.Update(17)
            server.quit()            
            prog.Update(18)
            
            exit()
            
        else:
            
            wx.MessageDialog(self, message=" SOMETHING WENT WRONG \n\n One of this requirements wasn't respected \n\n - All fields have to be compiled \n\n - E-Mail field has to be in the username@provider.domain format", caption="ATTENTION", style=wx.OK|wx.ICON_ERROR).ShowModal()
            
        
    
    def OnExit(self, event):
        exit()
    

args = sys.argv
args.pop(0)


args = ["Tabata Timer for Windows", "tabata.scottiltd", "C:/Users/Barbara/Desktop/python/tabata/files/favicon.ico"]


app = wx.App(False)
frame = MainWindow(args[0], args[1], args[2])
app.MainLoop()
