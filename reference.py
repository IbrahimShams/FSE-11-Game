#gameMenu.py

from pygame import *

def menu():
    running=True
    #myClock=time.Clock()
    buttons=[Rect(100+x*150,300,80,40) for x in range(4)]
    while running:
        print("main menu")
        for evt in event.get():
            if evt.type==QUIT:
                return "exit"
        screen.fill((0,0,0))
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        for b in buttons:
            draw.rect(screen,(0,255,0),b)

        if mb[0]:
            if buttons[0].collidepoint(mx,my):
                return "lev1"
##            if buttons[1].collidepoint(mx,my):
##                return "lev2"
            if buttons[2].collidepoint(mx,my):
                return "instructions"
            if buttons[3].collidepoint(mx,my):
                return "story"

        display.flip()
        
def story():
    running=True
    #load the picture here
    while running:
        print("story")
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        screen.fill((255,0,0))
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        ##here you can blit a picture with the "game story"
        ###also add "back to main menu" button
        display.flip()
    return "menu"

def instructions():
    running=True
    #load the picture here
    while running:
        print("instructions")
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        screen.fill((0,0,255))
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        ##here you can blit a picture with the "instructions"
        ###also add "back to main menu" button
        display.flip()
    return "menu"

def level1():
    running=True
    c=0 #counting the frames
    #load the picture here
    myClock=time.Clock()
    while running:
        #print("level 1")
        for evt in event.get():
            if evt.type==QUIT:
                running=False
        
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        c+=1
        if c%120==0:
            bullets.append([enemy[0],enemy[1],v[0],v[1]])

        print(bullets)

        
##'''
##        all the code for level1 goes here (break it down into functions)
##        movePlayer()  function calls
##        moveBullets()
##        drawScene()
##        checkHits()
##        .....
##'''
        drawScene(enemy,bullets)
        moveBullets(bullets)
        myClock.tick(60)
    
    return "menu"

def drawScene(en,bull):
    screen.fill((255,255,0))
    draw.circle(screen,(255,0,0),(en[0],en[1]),20)
    for b in bull:
        brect=Rect(b[0],b[1],10,10)
        draw.rect(screen,(0,0,255),brect)
    display.flip()

def moveBullets(bull):
    for b in bull:
        b[0]+=b[2]
        b[1]+=b[3]
        if b[0]<0:
            bull.remove(b)
    

screen=display.set_mode((800,600))
bullets=[]
v=[-2,0]#horizontal and vertical velocity
enemy=[700,300]#coordinates of the enemy


'''
This is the IMPORTANT part of this example
The idea is we have a variable (page) that keeps
track of which page we are on. We give control
of the program to the function until it is done and
the program returns the new page it should be on.
'''
page="menu"
while page!="exit":
    if page=="menu":
        page=menu()
    if page=="lev1":
        page=level1()
##    if page=="lev2":
##        page=level2()
    if page=="instructions":
        page=instructions()
    if page=="story":
        page=story()

quit()