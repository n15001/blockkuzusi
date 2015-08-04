#!/usr/bin/python3

from tkinter import *
import random
import time
import sys


# teisuu
WIDTH			= 500
HEIGHT			= 700
FPS				= 60
BALL_SPEED		= 5
PADDLE_SPEED	= 3
COLORS = ('cyan','green','gold','dark orange','magenta',)

class Ball:
    def __init__(self,canvas,paddle,speed,color):
        self.canvas	= canvas
        self.paddle	= paddle
        self.speed = speed
        self.id	= canvas.create_oval(10,10,25,25,fill=color)
        self.canvas.move(self.id,WIDTH/2,HEIGHT*0.6)
        self.x = 0
        self.y = 0
        self.h_btm = False
        self.canvas.bind_all('<Return>',self.start)

    def h_pdl(self,pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[1] <= paddle_pos[3] and pos[1] >= paddle_pos[1]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id)
        if pos[3] >= HEIGHT:        #bottom_wall (Reflect)
            self.y *= -1
        if pos[3] <= 0:             #top_wall (Gameover!)
            self.h_btm = True
        if self.h_pdl(pos) == True: #HIT_paddle (Reflect)
            self.y *= -1
        if pos[0] <= 0:             #left_wall (Reflect)
            self.x *= -1
        if pos[2] >= WIDTH:         #right_wall (Reflect)
            self.x *= -1

    def start(self,evt):
        self.x = -self.speed
        self.y = self.speed

class Paddle:
    def __init__(self,canvas,speed,color):
        self.canvas = canvas
        self.speed = speed
        self.id = canvas.create_rectangle(0,0,100,10,fill=color)
        self.canvas.move(self.id,WIDTH/2-50,HEIGHT/10)
        self.x = 0

        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>',self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>',self.turn_right)

    def draw(self):
        self.canvas.move(self.id,self.x,0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0
  
    def turn_left(self,evt):
        self.x = -self.speed

    def turn_right(self,evt):
        self.x = self.speed

class Block:
    def __init__(self,canvas,x,y,color):
        self.canvas = canvas
        self.pos_x = x
        self.pos_y = y
        self.id = canvas.create_rectangle(0,0,50,20,fill=color,outline='white')
        self.canvas.move(self.id,25 + self.pos_x * 50											, HEIGHT - 50 + self.pos_y * -20)

    def delete(self):
        self.canvas.delete(self.id)

class Check:
    def __init__(self,block):
        self.block = block

class TextLabel: 
    def __init__(self,canvas,color='green',text='GameOver!',x=250,						y=200,font=('Times',48),state='hidden'):
        self.canvas = canvas
        self.id = canvas.create_text(x,y,text=text,fill=color,												font=font,state=state)

    def show(self):
        self.canvas.itemconfig(self.id,state='normal')

# initarize
tk = Tk()
tk.title("---BreakOut---")
tk.resizable(0,0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk,width=WIDTH,height=HEIGHT,bd=0,highlightthickness=0)
canvas.pack()
tk.update()

image1 = PhotoImage(file = 'image2.gif')
#Label(tk, image = image1).pack()
#tk.mainloop()


hoge = canvas.create_image(0,0,image=image1)
canvas.move(hoge,250,350)
paddle	= Paddle(canvas,PADDLE_SPEED,'blue')
ball	= Ball(canvas,paddle,BALL_SPEED,'red')
blocks  = []
for y in range(5):
    for x in range(9):
        blocks.append(Block(canvas,x,y,random.choice(COLORS)),)
print(blocks)
text	= TextLabel(canvas)

#main
while True:
    if not ball.h_btm:
        ball.draw()
        paddle.draw()
    else:
        text.show()

    tk.update_idletasks()
    tk.update()
    time.sleep(1/FPS)
