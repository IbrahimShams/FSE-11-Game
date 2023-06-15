"""from pygame import *

width,height=800,600
screen=display.set_mode((width,height))
RED=(255,0,0)
GREY=(127,127,127)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
myClock=time.Clock()
running=True
start=time.get_ticks()
draw1=False
x,y,h,k,a=0,0,0,0,0

def parabola():
    return a*(x-h)**2+k

def draw_parabola(start):
    global draw1,x,y,h,k,a
    current=time.get_ticks()
    if current-start>=3000:
        start=current
        x=400
        y=-300
        h=(400+250)//2
        k=-(min(300,200)-100)
        a=(y-k)/(x-h)**2
        draw1=True
    return start

while running:
    screen.fill(WHITE)
    for evt in event.get():
        if evt.type==QUIT:
            running=False
    draw.circle(screen,RED,(400,300),5)
    draw.circle(screen,BLUE,(250,400),5)
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    start=draw_parabola(start)
    myClock.tick(60)
    if draw1:
        x-=2
        y=parabola()
        draw.circle(screen,GREEN,(x,-y),5)
    display.flip()
quit()
"""
