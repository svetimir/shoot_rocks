# SHOOTING ROCKS GAME
# AUTHOR: fluxoid, ifi@yandex.ru
# STARTED: 05.07.2017
# VERSION: 0.1.2
# FILE LATEST REVISION: 06.07.2017

from tkinter import *
from tkinter import messagebox
import random
import math
import time

version='0.1.2'
authors='fluxoid <ifi@yandex.ru>\njazzard <deathwingstwinks@gmail.com>'

# при выстреле порождается новый объект Bullet
# пуля движется и существует пока либо не столкнется с камнем
# либо не уйдет за пределы игрового холста

class Vehicle():
    def __init__(self,canvas,color):
        self.canvas=canvas
        self.bs=list()
        self.x=0
        #pause flag
        self.p=False
        #self.id=canvas.create_polygon(225,450,245,450,235,425,fill=color)
        self.img=PhotoImage(file='sp.gif')
        self.id=canvas.create_image(245,425,anchor=NW,image=self.img)
        self.canvas_width=self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-space>',self.shoot)
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right)
        self.canvas.bind_all('<Return>',self.spause)

    def draw(self):
        self.canvas.move(self.id,self.x,0)
        pos=self.canvas.coords(self.id)
        if pos[0]<=0:
            self.x=0
        elif pos[1]>=self.canvas_width:
            self.x=0

    def spause(self,event):
        if self.p==False:
            self.p=True
        else:
            self.p=False

    def shoot(self,event):
        pos=self.canvas.coords(self.id)
        self.bs.append(Bullet(canvas,pos[0]+20,pos[1]))

    def turn_left(self,event):
        self.x=-5

    def turn_right(self,event):
        self.x=5

class Bullet():
    def __init__(self,canvas,x,y):
        self.d=7
        self.y=-3
        self.canvas=canvas
        self.id=canvas.create_oval(x,y,x-self.d,y-self.d,fill='#ddcc00')
        self.canvas_height=self.canvas.winfo_height() 

    def hit_rock():
        pass
    
    def draw(self):
        self.canvas.move(self.id,0,self.y)
        
class Rock():
    def __init__(self,canvas):
        self.canvas=canvas
        c=random.randint(20,480)
        d=random.randint(10,20)
        self.id=canvas.create_rectangle(c,0,c+d,d,fill='#eeeeee')
        self.y=1
        self.canvas_height=self.canvas.winfo_height()

    # камень движется строго сверху вниз
    def draw(self):
        self.canvas.move(self.id,0,self.y)
        
class Stats():
    def __init__(self):
        self.pts=0

tk=Tk()
score=StringVar()
score.set('SCORE: ')
state_str=StringVar()
state_str.set('GAME ON. TO QUIT GAME PRESS \"ESC\", TO PAUSE PRESS \"ENTER\"')
tk.title('SHOOT ROCKS GAME. VERSION '+version)
tk.resizable(0,0)
btn1=Button(tk,text='Exit App',command=tk.destroy)
btn1.pack()
score_label=Label(tk,textvariable=score)
score_label.pack()
state_label=Label(tk,textvariable=state_str)
state_label.pack()
canvas=Canvas(tk,width=500,height=500,bg='#000000')
canvas.pack()

v=Vehicle(canvas,'red')
s=Stats()
gap=0.01
c=0
tol=0.001
rocks=list()
state=True
spawn_interval=1.5

canvas.bind_all('<Escape>',lambda e: tk.destroy())

while state:
    #if game paused
    if v.p:
        state_str.set('GAME PAUSED. TO QUIT GAME PRESS \"ESC\", TO RESUME PRESS \"ENTER\"')
        tk.update_idletasks()
        tk.update()
        time.sleep(0.05)
        continue
    state_str.set('GAME ON. TO QUIT GAME PRESS \"ESC\", TO PAUSE PRESS \"ENTER\"')
    v.draw()
    if v.bs:
        for i in v.bs:
            i.draw()
    if rocks:
        for i in rocks:
            i.draw()
    # создаем камень
    if c>=spawn_interval:
        rocks.append(Rock(canvas))
        c=0
    # защита от переполнения
    if len(rocks)>=500:
        rocks.clear()
    if len(v.bs)>=500:
        v.bs.clear()
    # проверка на столкновение
    for i in v.bs:
        a=i.canvas.coords(i.id)
        #A. пуля уходит за холст
        if a[1]<=0:
            canvas.delete(i.id)
            v.bs.remove(i)
        for j in rocks:
            b=j.canvas.coords(j.id)
            #1. пуля сталкивается с камнем
            if a[2]>=b[0] and a[0]<=b[2]:
                if a[3]>=b[1] and a[3]<=b[3]:
                    # print('boom!')
                    canvas.delete(i.id)
                    canvas.delete(j.id)
                    v.bs.remove(i)
                    rocks.remove(j)
                    s.pts+=10
                    score.set(('SCORE: ')+str(s.pts))
            #B. камень уходит за холст
            if b[3]>=j.canvas_height:
                canvas.delete(j.id)
                rocks.remove(j)
    #2. корабль сталкивается с камнем
    for i in rocks:
        a=v.canvas.coords(v.id)
        b=i.canvas.coords(i.id)
        if a[0]+40>=b[0] and a[0]<=b[2]:
            if a[1]>=b[1] and a[1]<=b[3]:
                state=False
                state_str.set('GAME OVER')
                break
    tk.update_idletasks()
    tk.update()
    time.sleep(gap)
    c+=gap

messagebox.showinfo('SHOOT ROCKS VERSION '+version,'GAME IS OVER\nTHANKS FOR PLAYING!\nYOUR SCORE IS: '+str(s.pts)+'\nSHOOT ROCKS IS BROUGHT TO YOU BY:\n'+authors)
