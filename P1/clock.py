import tkinter as tk
import math
import time
from P1.Logger import Log


class Ceas(tk.Frame):

    def __init__(self, master=None):
        self.w = 500
        self.h = 500
        self.states = []
        tk.Frame.__init__(self, master)
        self.master = master
        self.ceas = tk.Canvas(self, width=self.w, height=self.h)
        self.ceas.place(x=0, y=0)
        self.init_window()

    def init_window(self):
        self.master.title("Analogical clock")
        self.pack(fil=tk.BOTH, expand=1)

        # Set h/m/s
        setClock=tk.Button(self, text="Set clock", command=self.client_set_clock).place(x=645,y=53)
        restore=tk.Button(self, text="Restore clock", command=self.client_restore).place(x=645,y=90)

        self.hourSet=tk.Spinbox(self, cnf={"from":0, "to":11, "width":3, "font":"Consolas"})
        self.hourSet.place(x=510,y=55)
        self.minuteSet=tk.Spinbox(self, cnf={"from":0, "to":60, "width":3, "font":"Consolas"})
        self.minuteSet.place(x=555,y=55)
        self.secundeSet=tk.Spinbox(self, cnf={"from":0, "to":60, "width":3, "font":"Consolas"})
        self.secundeSet.place(x=600,y=55)


        self.hour=time.localtime().tm_hour
        self.min=time.localtime().tm_min
        self.sec=time.localtime().tm_sec
        self.states.append((self.hour, self.min, self.sec))
        self.after(1000,self.UpdateClock)

    def UpdateClock(self):
        self.ceas.create_rectangle(0, 0, self.w, self.h, fill="grey")

        self.sec += 1
        Log.get_instanta().write('a trecut o sec')
        if self.sec >= 60:
            self.sec=0
            self.min+=1
        if self.min >= 60:
            self.min=0
            self.hour+=1
        if self.hour >=12:
            self.hour-=12


        self.DrawClock(self.w, self.h, self.hour, self.min, self.sec)
        self.after(1000, self.UpdateClock)

    def DrawClock(self, w, h, hh, mm, ss):

        self.ceas.create_oval(10, 10, w-10, h-10)
        XCentru=w/2
        YCentru=h/2
        Raza=(w+h)/4-50
        cifre = (3, 4, 5, 6, 7,  8,  9, 10, 11, 12,  1,  2)
        #punctele rosii aferente minutelor principale + numerele in format text
        for i in range(12):
            #construim coordonatele punctelor rosii care indica minutele divizibile cu 5, respectiv textul aferent acestor grupuri
            xNr = XCentru + Raza * math.cos(self.ToRadiani(30 * i))
            yNr = YCentru + Raza * math.sin(self.ToRadiani(30 * i))
            xPt = XCentru + (Raza + 30) * math.cos(self.ToRadiani(30 * i))
            yPt = YCentru + (Raza + 30) * math.sin(self.ToRadiani(30 * i))
            #culoarea este un string hex similar cu valorile HTML, "#FF0000" = red   culorile sunt hex RGB -> RRGGBB
            self.ceas.create_text(xNr, yNr, fill="#800080", text=str(cifre[i]), font = 'Consolas 18 bold')
            self.ceas.create_oval(xPt - 5, yPt - 5, xPt + 5, yPt + 5, fill = "#FF0000")

        #liniile care indica minutele
        grad_minut = 360 / ( 5 * 12)
        Rinterior = (w+h) / 4 - 30
        Rexterior = (w+h) / 4 - 20
        # construim coordonatele liniilor care indica minutele (orientarea trebuie sa fie cerc_interior -> cerc_exterior), altfel ar arata ciudat
        for i in range(60):
            if i>0 and i % 5 != 0:
                x1 = XCentru + Rinterior * math.cos(self.ToRadiani(grad_minut * i))
                y1 = YCentru + Rinterior * math.sin(self.ToRadiani(grad_minut * i))
                x2 = XCentru + Rexterior * math.cos(self.ToRadiani(grad_minut * i))
                y2 = YCentru + Rexterior * math.sin(self.ToRadiani(grad_minut * i))
                self.ceas.create_line(x1,y1,x2,y2, fill="#0000FF", width = 3)

        # centrul ceasului
        self.ceas.create_oval(w / 2 - 10, h / 2 - 10, w / 2 + 10, h / 2 + 10, fill="#FFFF00")

        self.ceas.create_text(self.w / 2, self.h / 2 + 30, fill = "#FF8000", text="Clock Application", font = "Times 20 italic bold")

        #desenam acele care indica ora
        self.DeseneazaAc(1, hh, mm)
        self.DeseneazaAc(2, mm, ss)
        self.DeseneazaAc(3, ss)

    def DeseneazaAc(self, tip, indicator, indicator2 = 0):
        grad_minut = 360 / (5 * 12)
        x1 = self.w / 2
        y1 = self.h / 2
        if tip == 1:
            #unghiul acului care indica ora, trebuie pozitionat si in functie de minut, indicator2 este minutul, iar pentru 60 minute, orarul face maxim 30 grade
            unghi = self.ToRadiani(((indicator % 12) * 5 * grad_minut + indicator2 * (30 / 60) + 270) % 360)
            scale = 8
            x2 = self.w / 2 + ((self.w + self.h) / scale) * math.cos(unghi)
            y2 = self.h / 2 + ((self.w + self.h) / scale) * math.sin(unghi)
            self.ceas.create_line(x1, y1, x2, y2, fill="#000000", width = 7)
        elif tip == 2:
            #unghiul acului care indica minutul, trebuie pozitionat si in functie de secunda, indicator2 este secunda, iar pentru 60 secunde, minutarul face maxim 6 grade
            #adica distanta intre 2 minute pe cerc
            unghi = self.ToRadiani(((indicator % 60) * grad_minut + indicator2 * (6 / 60) + 270) % 360)
            scale = 6
            x2 = self.w / 2 + ((self.w + self.h) / scale) * math.cos(unghi)
            y2 = self.h / 2 + ((self.w + self.h) / scale) * math.sin(unghi)
            self.ceas.create_line(x1, y1, x2, y2, fill="#008000", width = 3)
        elif tip == 3:
            #secundarul se misca doar intre liniutele care arata minutele/secundele
            unghi = self.ToRadiani(((indicator % 60) * grad_minut + 270) % 360)
            scale = 5.5
            x2 = self.w / 2 + ((self.w + self.h) / scale) * math.cos(unghi)
            y2 = self.h / 2 + ((self.w + self.h) / scale) * math.sin(unghi)
            self.ceas.create_line(x1, y1, x2, y2, fill="#FF0000")


    def ToRadiani(self, unghi):
        return unghi*math.pi/180

    def client_set_clock(self):
        Log.get_instanta().write('Set Clock')
        self.states.append((self.hour, self.min, self.sec))
        self.hour=aproximare(int(self.hourSet.get()), 0, 11)
        self.min=aproximare(int(self.minuteSet.get()), 0, 60)
        self.sec=aproximare(int(self.secundeSet.get()), 0, 60)
        self.ceas.create_rectangle(0,0,self.w, self.h, fill="grey")
        self.DrawClock(self.w, self.h, self.hour, self.min, self.sec)

    def client_restore(self):
        Log.get_instanta().write('Restore clock')
        if len(self.states) > 0:
            last_states = self.states.pop()
            self.hour = last_states[0]
            self.min = last_states[1]
            self.sec = last_states[2]

def aproximare(value, _min, _max):
    return max(_min, min(value, _max))

#=== Main ===

Log = Log('spy.txt')
root = tk.Tk()
root.geometry("800x500")
clockApp = Ceas(root)
root.mainloop()