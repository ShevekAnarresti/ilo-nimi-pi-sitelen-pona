import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import messagebox
import pyautogui as pa
import fpdf, os

class Keyboard(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.buttons=[[
            ['!','60','52','36','32','28','26','30','34','50','58','BKSP'],
            ['TAB','56','44','24','16','12','10','14','22','42','54','"'],
            ['?','48','40','20','8','4','2','6','18','38','46','ENT'],
            ['[','47','39','19','7','3','1','5','17','37','45',','],
            [']','55','43','23','15','11','9','13','21','41','53','.'],
            ['ALT','59','51','35','31','27','25','29','33','49','57',':']
            ],[
            ['!','120','112','96','92','88','86','90','94','110','118','BKSP'],
            ['TAB','116','104','84','76','72','70','74','82','102','114','"'],
            ['?','108','100','80','68','64','62','66','78','98','106','ENT'],
            ['(','107','99','79','67','63','61','65','77','97','105',','],
            [')','115','103','83','75','71','69','73','81','101','113','.'],
            ['ALT','119','111','95','91','87','85','89','93','109','117',':']]]
        self.buttontounicode=[
            57383,101,57397,57410,57361,57453,57428,57421,57377,57450,57388,57346,57439,57414,57405,57452,57442,57366,57464,57393,
            57384,57368,111,57411,57449,57422,57448,97,57357,57417,57363,57454,57390,57369,57348,57444,57434,57441,57455,57351,
            57433,57420,57430,57404,57445,57408,57460,57356,57354,57375,57451,57380,57424,57386,57443,57399,57437,57389,57406,57396,
            57358,57352,57436,57365,57407,57400,57462,57416,57367,57463,57394,57353,57373,57426,57458,57398,57413,57423,57378,57359,
            57350,57371,57431,57395,57461,57376,57385,57381,57435,57427,57403,57447,57345,57425,57415,57382,57418,57387,57370,57372,
            57459,57446,57374,57440,57364,57457,57409,57412,57401,57392,57402,57456,57360,57355,57362,57379,57419,57432,57429,57347]
        self.buttontoname=[
            'li','e','mi','ni','jan','toki','pona','pi','la','tawa','lon','ala','sina','ona','mute','tenpo','sona','kama','wile','ma',
            'lili','ken','o','nimi','taso','pilin','tan','a','ike','pali','jo','tomo','lukin','kepeken','ali','suli','sewi','sitelen','tu','ante','seme',
            'pana','sama','musi','suno','nasin','wan','ijo','en','kulupu','telo','lawa','pini','lipu','soweli','moku','sin','luka','nanpa','meli',
            'ilo','anu','sike','kalama','nasa','moli','wawa','pakala','kasi','weka','mama','awen','kon','poka','utala','mije','olin','pimeja','lape','insa',
            'anpa','kiwen','seli','mani','waso','kute','linja','len','sijelo','poki','mun','suwi','akesi','pipi','open','lete','palisa','loje','kili','ko',
            'walo','supa','kule','sinpin','kala','uta','nena','noka','monsi','lupa','mu','unpa','jaki','esun','jelo','laso','pan','selo','pu','alasa']
        rightbuttons=[
            ['INS','HOME','PAGEUP'],
            ['DEL','END','PAGEDOWN'],
            [None,None,None],
            [None,None,None],
            [None,'UP',None],
            ['LEFT','DOWN','RIGHT']]
        self.words=[]
        self.tkbuttons=[None]*(12*6)
        for i in range(6):
            frame=tk.Frame(self)
            frame.grid(row=i)
            for j in range(12):
                self.tkbuttons[i*12+j]=tk.Button(frame,
                            width=2+
                            ((i%2)*1 if j==0 else 0)+
                            (((i+1)%2)*1 if j==11 else 0),
                            repeatdelay=500,repeatinterval=100)
                self.tkbuttons[i*12+j].configure(font=("sitelen luka tu tu",14))
                self.tkbuttons[i*12+j].grid(row=0,column=j,sticky=tk.W+tk.E+tk.N+tk.S)
                self.tkbuttons[i*12+j].tip=CreateToolTip(self.tkbuttons[i*12+j],'')
            f=tk.Frame(frame,width=20).grid(row=0,column=12)
            for j in range(3):
                if rightbuttons[i][j]:
                    b=tk.Button(frame,width=2,
                                font=("sitelen luka tu tu",14),
                                text=self.getchar(rightbuttons[i][j]),
                                command=lambda x=
                                rightbuttons[i][j]:self.getcomm(x),
                                repeatdelay=500,repeatinterval=100
                                ).grid(row=0,column=13+j)
                else:
                    f=tk.Frame(frame,width=44).grid(row=0,column=13+j)
        self.page=0
        self.updateButtons()
    def updateButtons(self):
        for i in range(6):
            for j in range(12):
                button=str(self.buttons[self.page][i][j])
                command=lambda x=button:self.getcomm(x)
                self.tkbuttons[i*12+j].configure(
                    text=self.getchar(button),
                    command=command)
                self.tkbuttons[i*12+j].tip.setText(
                    self.buttontoname[int(button)-1] if button.isdigit() else '')
    def getcomm(self,code):
        if code.isdigit():
            comm=chr(self.buttontounicode[int(code)-1])
        else:
            comm=code
        if comm=='ALT':
            self.page=abs(1-self.page)
            self.updateButtons()
            return
        self.words.append(comm)
    def getchar(self,code):
        if code.isdigit():
            return chr(self.buttontounicode[int(code)-1])
        return {'BKSP':'\u27F5','TAB':'\u21E5','ENT':'\u21B5','ALT':'\u21E7',
                '':'','?':'?','!':'!','[':'[',']':']','(':'(',')':')',
                '.':'.',',':',',':':':','"':'"',
                'INS':'\uE007\uE043','HOME':'\uE029\uE047','PAGEUP':'\uE02A\uE05A',
                'DEL':'o\uE077','END':'\uE029\uE050','PAGEDOWN':'\uE02A\uE006',
                'UP':'\u2191','DOWN':'\u2193','LEFT':'\u2190','RIGHT':'\u2192'}[code]
    def getWords(self):
        toret=self.words
        self.words=[]
        return toret

class Toki(tk.Tk):
    def __init__(self,file=None):
        super().__init__()
        self.actions={'ENT':'\n','BKSP':'backspace','TAB':'tab',
            'HOME':'home','PAGEUP':'pgup','DEL':'del','END':'end',
            'PAGEDOWN':'pgdn','UP':'up','LEFT':'left','DOWN':'down','RIGHT':'right'}
        self.insert=False
        self.file=file
        self.title('ilo nimi pi sitelen pona')
        self.menu=tk.Frame(self)
        self.filemenu=tk.Menubutton(self.menu,font=("sitelen luka tu tu",14),
                                text='\uE02A') #file
        self.filemenud=tk.Menu(self.filemenu,tearoff=0)
        self.filemenud.add_checkbutton(label="\uE02A\uE05D", #new
                                       font=("sitelen luka tu tu",14),
                                       command=lambda:Toki().mainloop())
        self.filemenud.add_checkbutton(label="o\uE047e\uE02A", #open
                                       font=("sitelen luka tu tu",14),
                                       command=self.opennew)
        self.filemenud.add_separator()
        self.filemenud.add_checkbutton(label="o\uE009e\uE02A", #save
                                       font=("sitelen luka tu tu",14),
                                       command=lambda:self.save(False))
        self.filemenud.add_checkbutton(label="o\uE009e\uE02A\uE05D", #save as
                                       font=("sitelen luka tu tu",14),
                                       command=lambda:self.save(True))
        self.filemenud.add_checkbutton(label="o\uE049e\uE02APDF", #export
                                       font=("sitelen luka tu tu",14),
                                       command=self.export)
        self.filemenud.add_separator()
        self.filemenud.add_checkbutton(label="o\uE050", #close
                                       font=("sitelen luka tu tu",14),
                                       command=self.destroy)
        self.filemenu["menu"]=self.filemenud
        self.text=ScrolledText(self,width=40)
        self.text.configure(font=('sitelen luka tu tu', 20))
        self.keyboardFrame=tk.Frame(self,padx=5,pady=5)
        self.keyboard=Keyboard(self.keyboardFrame)
        self.menu.pack(expand=tk.YES,fill=tk.X)
        self.filemenu.grid(row=0)
        self.keyboardFrame.pack()
        self.keyboard.grid(row=0)
        self.text.pack(expand=tk.YES,fill=tk.BOTH)
        if self.file:
            self.open(self.file)
        self.after(0,self.getWord)
    def getWord(self):
        words=self.keyboard.getWords()
        if words:
            self.text.focus()
            for w in words:
                if w in self.actions:
                    pa.press(self.actions[w])
                elif w=='INS':
                    self.insert=not self.insert
                else:
                    if self.insert:
                        pa.press('del')
                    self.text.insert(tk.INSERT,w)
        self.after(10,self.getWord)
    def save(self,new):
        if new:
            filename=filedialog.askopenfilename(title="lipu awen li seme?",
                parent=self,defaultextension='.toki',
                filetypes=(("lipu Toki","*.toki"),("lipu ali","*.*")))
        else:
            filename=filedialog.asksaveasfilename(title="lipu awen li seme?",
                parent=self,defaultextension='.toki',
                filetypes=(("lipu .toki","*.toki"),("lipu ali","*.*")))
        if filename:
            try:
                with open(filename,'wb') as f:
                    f.write(self.text.get('1.0', 'end').encode())
                    self.title('ilo nimi pi sitelen pona: '+filename)
                    self.file=filename
            except IOError as e:
                messagebox.showerror('pakala!','ni li ike:\nI/O error ({0}): {1}'.format(e.errno, e.strerror))
            else:
                messagebox.showinfo('pona!', 'lipu li awen!')
    def open(self,filename):
        try:
            with open(filename,'rb') as f:
                self.text.insert('1.0',f.read().decode())
            self.title('ilo nimi pi sitelen pona: '+filename)
            self.file=filename
        except IOError as e:
            messagebox.showerror('pakala!','ni li ike:\nI/O error ({0}): {1}'.format(e.errno, e.strerror))
    def opennew(self):
        filename=filedialog.askopenfilename(title="lipu open li seme?",
                parent=self,defaultextension='.toki',
                filetypes=(("lipu Toki","*.toki"),("lipu ali","*.*")))
        if filename:
            if self.file:
                Toki(filename).mainloop()
            else:
                self.open(filename)
    def export(self):
        filename=filedialog.asksaveasfilename(title="lipu pana li seme?",
                parent=self,defaultextension='.pdf',
                filetypes=(("lipu .pdf","*.pdf"),("lipu ali","*.*")))
        try:
            pdf=fpdf.FPDF()
            pdf.add_page()
            try:
                pdf.add_font('sitelen luka tu tu','',
                         (r'C:\Windows\Fonts\sitelen_luka_tu_tu.ttf' if os.name=='nt'
                          else '/usr/share/fonts/sitelen_luka_tu_tu.ttf'),
                         uni=True)
            except RuntimeError:
                pdf.add_font('sitelen luka tu tu','',
                         (r'C:\Windows\Fonts\sitelen_luka_tu_tu.ttf_' if os.name=='nt'
                          else '/usr/share/fonts/sitelen_luka_tu_tu_.ttf'),
                         uni=True)
            pdf.set_font('sitelen luka tu tu',size=20)
            for t in self.text.get('1.0',tk.END).split('\n'):
                pdf.cell(200,10,txt=t,ln=1,align='L')
            pdf.output(filename)
        except Exception as e:
            messagebox.showerror('pakala!','ni li ike:\n'+str(e))
        else:
            messagebox.showinfo('pona!', 'lipu li pana!')

class ToolTip(object):
    def __init__(self,widget):
        self.widget=widget
        self.tipwindow=None
        self.x=self.y=0
    def setText(self,text):
        self.text=text
    def showtip(self):
        if self.tipwindow or not self.text:
            return
        x,y,cx,cy=self.widget.bbox("insert")
        x=x+self.widget.winfo_rootx()+57
        y=y+cy+self.widget.winfo_rooty()+27
        self.tipwindow=tw=tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d"%(x,y))
        label=tk.Label(tw,text=self.text,justify=tk.LEFT,
                    background="#ffffe0",relief=tk.SOLID,borderwidth=1,
                    font=("tahoma","8","normal"))
        label.pack(ipadx=1)
        tw.attributes("-topmost",True)
    def hidetip(self):
        tw=self.tipwindow
        self.tipwindow=None
        if tw:
            tw.destroy()

def CreateToolTip(widget,text):
    toolTip=ToolTip(widget)
    def enter(event):
        toolTip.showtip()
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>',enter)
    widget.bind('<Leave>',leave)
    return toolTip

Toki().mainloop()
