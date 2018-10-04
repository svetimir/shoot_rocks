# -*- coding: utf-8 -*-

# SHOOTING ROCKS GAME
# AUTHOR: fluxoid, ifi@yandex.ru
# STARTED: 05.07.2017
# VERSION: 0.3
# LATEST FILE REVISION: 05.09.2018

from tkinter import *
from tkinter import messagebox
import random, time

version='0.3'
authors='fluxoid <ifi@yandex.ru>\njazzard <deathwingstwinks@gmail.com>'

# 0.4 - ОЖИДАЕТСЯ
# - уровни сложности EASY MEDIUM HARDCORE

# 0.3.2 - ОЖИДАЕТСЯ
# - моргание корабля при попадании в него камня

# 0.3.1
# - оптимизация, исправление косяков

# 0.3
# - добавлен анимированный бэкграунд
# - оптимизация

# 0.2.8
# - добавлена документация к классам

# 0.2.7
# - новые экстра-прочные камни (с хитпоинтами количеством 3)
# -- вероятность спавна 15%

# 0.2.6
# - ускорение скорости спавна и движения камней со временем

# 0.2.5
# - кораблю добавлены хитпоинты
# -- больше не ваншотается
# - интерфейс с очками и хитпоинтами

# версия 0.2.1
# - графические камушки
# - новый корабль

# при выстреле порождается новый объект Bullet
# пуля движется и существует пока либо не столкнется с камнем
# либо не уйдет за пределы игрового холста

class Vehicle(object):
    """
    Класс корабля
    * создает корабль на холсте
    * задает характеристики корабля
    * содержит массив пуль
    """
    def __init__(self,canvas):
        self.canvas=canvas
        self.bs=list()
        self.x=0
        #pause flag
        self.p=False
        self.img=PhotoImage(file='sp-0.2.1.gif')
        self.id=canvas.create_image(245,425,anchor=NW,image=self.img)
        self.canvas_width=self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-space>',self.shoot)
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right)
        self.canvas.bind_all('<Return>',self.spause)
        # 0.2.5
        self.hitpoints=5

    def draw(self):
        pos = self.canvas.coords(self.id)
        self.canvas.move(self.id,self.x,0)
        if pos[0] <= 0:
            self.x = 0
        elif pos[0] >= self.canvas_width:
            self.x = 0

    def spause(self,event):
        self.p=not self.p

    def shoot(self,event):
        pos=self.canvas.coords(self.id)
        self.bs.append(Bullet(canvas,pos[0]+20,pos[1]))

    def turn_left(self,event):
        self.x=-5

    def turn_right(self,event):
        self.x=5

# функция моргания корабля при попадании в него камня
    def cblink(self):
        pass

class Bullet(object):
    """
    Класс пуль
    * создает пулю при нажатии соответствующей кнопки
    * пока (0.2.7.1) пули не имеют графики а рисуются графическим примитивом
    """
    def __init__(self,canvas,x,y):
        self.d=7
        self.y=-5
        self.canvas=canvas
        self.id=canvas.create_oval(x,y,x-self.d,y-self.d,fill='#ddcc00')
        self.canvas_height=self.canvas.winfo_height()
    
    def draw(self):
        self.canvas.move(self.id,0,self.y)
        
class Rock(object):
    """
    Класс камней
    * создает камень на холсте
    * камень заданного типа (одного из двух), с заданной скоростью падения
    """
    def __init__(self,canvas,velocity,rock_type):
# конструктор версии 0.2.7
        self.rock_type=rock_type
        self.canvas=canvas
        self.hp=0
        if rock_type=='regular':
            self.img=PhotoImage(file='asteroid40x40.gif')
        elif rock_type=='extra':
            self.img=PhotoImage(file='asteroid-extra.gif')
            self.hp=2
        c=random.randint(20,480)
        self.id=canvas.create_image(c,0,anchor=NW,image=self.img)
# стартовая скорость падения камней 1
# каждые N камней скорость падения чучуть увеличивается
        self.y=velocity
        self.canvas_height=self.canvas.winfo_height()
        
    # камень движется строго сверху вниз
    def draw(self):
        self.canvas.move(self.id,0,self.y)

class Stats(object):
    """
    класс игровой статистики
    """
    def __init__(self):
        self.pts=0

# 0.2.5
class InfoHP(object):
    """
    класс учёта хитпоинтов корабля и вывода их количества на экран
    """
    def __init__(self,canvas,hitpoints):
        self.canvas=canvas
        self.hp=hitpoints
        self.id=canvas.create_text((20,20),anchor=NW,text='Hits: '+str(hitpoints),fill='#ffffff')

    def update(self,hitpoints):
        self.canvas.itemconfigure(self.id,text='Hits: '+str(hitpoints))

class InfoScore(object):
    """
    класс учета очков, заработанных игроком
    """
    def __init__(self,canvas,score):
        self.canvas=canvas
        self.sc=score
        self.id=canvas.create_text((20,40),anchor=NW,text='Score: '+str(score),fill='#ffffff')

    def update(self,score):
        self.canvas.itemconfigure(self.id,text='Score: '+str(score))

tk=Tk()
state_str=StringVar()
state_str.set('GAME ON. TO QUIT GAME PRESS \"ESC\", TO PAUSE PRESS \"ENTER\"')
tk.title('SHOOT ROCKS GAME. VERSION '+version)
tk.resizable(0,0)
btn1=Button(tk,text='Exit App',command=tk.destroy)
btn1.pack()
state_label=Label(tk,textvariable=state_str)
state_label.pack()
canvas=Canvas(tk,width=500,height=500,bg='black')
canvas.pack()

#------------------------------
# анимированный бэкграунд
bg_upd_cnt=0
frm_cnt=0
bgif=PhotoImage(file='cosm.gif')
bg_image=canvas.create_image(0,0,anchor=NW,image=bgif)

bg_frames=[PhotoImage(file='cosm.gif',format='gif -index %i'%(i)) for i in range(45)]

def update_bg(ind):
    frame=bg_frames[ind]
    canvas.itemconfigure(bg_image,image=frame)

#------------------------------

v=Vehicle(canvas)
s=Stats()
infohp=InfoHP(canvas,v.hitpoints)
infosc=InfoScore(canvas,s.pts)
gap=0.01
c=0
#tol=0.001
rocks=list()
state=True
# стартовый интервал спавна (сложности EASY)
spawn_interval=1.5
# каждые next_v камней чуть чуть увеличиваем скорость падения
# и скорость спавна каждые next_sp камней
spawn_fact=0.1
# минимальный интервал спавна
spawn_min=0.4
# счетчики камней
rc=0
rs=0
# константа ускорения камней
next_v=10
# константа ускорения спавна
next_sp=20
# скорость падения
fall_v=1
# фактор скорости
v_fact=0.05
# максимальная скорость
max_v=10
# контроль спавна камней
wrock=0

canvas.bind_all('<Escape>',lambda e: tk.destroy())

#основной цикл игры
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
        # селектор спавна камней
        wrock=random.randint(1,100)
        if wrock>=85:
            rocks.append(Rock(canvas,fall_v,'extra'))
        else:
            rocks.append(Rock(canvas,fall_v,'regular'))
        c=0        
        rc+=1
        rs+=1
        # каждые next_v камней чучуть увеличиваем скорость падения
        # и скорость спавна каждые next_sp камней
        if rc==next_v:
            if fall_v<=max_v:
                fall_v+=v_fact
            # debug
            # print('текущая скорость камней: '+str(fall_v))
            # print('текущий промежуток спавна: '+str(spawn_interval))
            # end_debug
            rc=0
        if rs==next_sp:
            if spawn_interval>=spawn_min:
                spawn_interval-=spawn_fact
            rs=0
                
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
            if a[2]>=b[0] and a[0]<=b[0]+40:
                if a[3]>=b[1] and a[3]<=b[1]+40:
                    # пулю удаляем
                    canvas.delete(i.id)
                    v.bs.remove(i)
                    # проверяем хитпоинты камня
                    if j.hp==0:
                        canvas.delete(j.id)
                        rocks.remove(j)
                    else:
                        j.hp-=1
                    s.pts+=10
                    # обновляем текст информации об очках
                    infosc.update(s.pts)
            #B. камень уходит за холст
            if b[1]>=j.canvas_height:
                canvas.delete(j.id)
                rocks.remove(j)
    #2. корабль сталкивается с камнем
    for i in rocks:
        a=v.canvas.coords(v.id)
        b=i.canvas.coords(i.id)
        if a[0]+40>=b[0] and a[0]<=b[0]+40:
            if a[1]>=b[1] and a[1]<=b[1]+40:
                # столкновение произошло
                # во первых удаляем камень (так или иначе камень всё)
                canvas.delete(i.id)
                rocks.remove(i)
                # если хиты еще есть - живем и декремент их
                if v.hitpoints>1:
                    v.hitpoints-=1
                    # обновляем текст хитпоинтов
                    infohp.update(v.hitpoints)
                    # а тут моргаем кораблем изза столкновения
                    v.cblink()
                # если же хитпоинт оставался последний - геймовер
                else:
                    state=False
                    state_str.set('GAME OVER')
                break

    # анимируем бэкграундный гиф
    bg_upd_cnt+=1
    if bg_upd_cnt>2:
        bg_upd_cnt=0
        if frm_cnt>44:
            frm_cnt=0
        update_bg(frm_cnt)
        frm_cnt+=1

    tk.update_idletasks()
    tk.update()
    time.sleep(gap)
    c+=gap

messagebox.showinfo('SHOOT ROCKS VERSION '+version,'GAME IS OVER\nTHANKS FOR PLAYING!\nYOUR SCORE IS: '+str(s.pts)+'\nSHOOT ROCKS IS BROUGHT TO YOU BY:\n'+authors)
