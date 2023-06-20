from pygame import * #importing modules
from math import *
from random import *

font.init() #font intitialization

#general setup variables
width,height=1150,697
screen=display.set_mode((width,height))
display.set_caption("Vicioux Robotix")
RED=(255,0,0)
GREY=(200,200,200)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
myClock=time.Clock()
running=True
bg_colour=(randint(50,205),randint(50,205),randint(50,205)) #bg colour random
omx,omy=0,0 #old mouse x mouse y
rect_list=[Rect(0,500,50,50)] #list of all the blocks (rects) player places

#Image paths, counters, and image variables
lava_counter,robot_counter=0,0
block=image.load("block2.png").convert()
block_count_icon=image.load("block_count_icon.png")
block_count_icon=transform.scale(block_count_icon,(60,60)).convert_alpha()
robot_platform=image.load("robot_platform.png").convert_alpha()
lavaImgs=[image.load("lava/lava00"+f"{i}"+".png").convert() for i in range(6)]
lava_background=Rect(0,597,1150,100)
for img in lavaImgs:
    img.set_colorkey(BLACK)

#player and move variables
jumpPower=-7
move_list=["no jump","right",0.07,False]
dJump,facing,img_speed,atckHitbox=0,1,2,3 #double jump, facing direction for player, image speed for animation, and attack hitbox variables
gravity=0.3 #gravity
X,Y,W,H=0,1,2,3 #for player
v=[0,0,697] #X,Y velocity for player
p=Rect(0,300,40,75) #player hitbox rect
p_list=[0,0] #player animation list (row, column for 2d list of animations. row for action, column for frame)

#robot variables
SPEED=15 #speed of bullet
begin_timer=False #timing robot
begin=True #a variable to control timer, when to start and when to finish
no_spawn_region=Rect(0,325,200,175) #robots cant spawn in this rect
objects=[lava_background,p] #the objects you cant draw on
bullets=[] #bullets 2d list. includes a list for each bullet with x,y,vx,vy

#level and block variables
level=10
blocks=[15,15] #the 2nd one is your maximum amount of blocks you can place and your first one is the amount of blocks you have with you minus the ones you have placed.
blockFont=font.SysFont("Comic Sans MS",40) #fonts for block and level
levelFont=font.SysFont("Arial",250)

def flipPics(lst):
    return [transform.flip(image,True,False) for image in lst]

def addPics(source,name,start,end):
    mypics=[]
    for i in range(start,end+1):
        img=image.load(f"{source}/{name}{i:03}.png").convert_alpha()
        img=transform.scale(img,(75,75))
        mypics.append(img)
    return mypics

player_pics=[]
player_pics.append(addPics("player","tile",0,4)) #idle right
player_pics.append(flipPics(player_pics[0])) #idle left
player_pics.append(addPics("player","tile",24,31)) #walking right
player_pics.append(flipPics(player_pics[2])) #walking left
player_pics.append(addPics("player","tile",40,47)) #jumping right
player_pics.append(flipPics(player_pics[4])) #jumping left
player_pics.append(addPics("player","tile",64,71)) #attack right
player_pics.append(flipPics(player_pics[6])) #attack left

robot_pics=[]
robot_pics.append(addPics("robots","tile",88,95)) #shooter robot pics right
robot_pics.append(flipPics(robot_pics[0])) #shooter robot pics left
robot_pics.append(addPics("robots","tile",104,111)) #bomber robot pics right
robot_pics.append(flipPics(robot_pics[2])) #bomber robot pics left
robot_pics.append(addPics("robots","tile",48,55)) #map degenerator robot pics right
robot_pics.append(flipPics(robot_pics[4])) #map degenerator robot pics left
robot_pics.append(addPics("robots","tile",176,183)) #laser robot pics right
robot_pics.append(flipPics(robot_pics[6])) #laser robot pics left

possibleRobots=["shooter","bomber","map degenerator","laser"]
robots=[choice(possibleRobots)]
robot_timers=[time.get_ticks()]

poof_pics=addPics("poof","tile",0,7)
poof_list=[]

def checkDeath():
    global running
    if p[Y]>=600 or blocks[1]==0:
        running=False

def roundIt(num,round_num):
    n=0
    for i in range(0,num+1,round_num):
        if i+round_num>num:
            n=i
    return n

robot_hitboxes=[Rect(roundIt(randint(0,1100),50),roundIt(randint(0,500),50),50,50)]
while robot_hitboxes[0].colliderect(no_spawn_region):
    robot_hitboxes=[Rect(roundIt(randint(0,1100),50),roundIt(randint(0,500),50),50,50)]
objects.append(robot_hitboxes[0])

def generatePlatform():
    while True:
        robotHitbox=Rect(roundIt(randint(0,1100),50),roundIt(randint(0,500),50),50,50)
        if not robotHitbox.colliderect(no_spawn_region) and robotHitbox.collidelist(robot_hitboxes)==-1:
            robot_hitboxes.append(robotHitbox)
            objects.append(robotHitbox)
            break

def destroyMap(map):
    if len(map)>0:
        block=choice(map)
        map.remove(block)
        if blocks[1]>0:
            blocks[1]-=1
    blocks[0]=blocks[1]-len(map)

def mapDestroyRobot(start,waiting):
    current=time.get_ticks()
    if current-robot_timers[start]>=waiting:
        destroyMap(rect_list)
        robot_timers[start]=current

def shoot(x1,y1,x2,y2):
    ang=atan2(y2-y1,x2-x1)
    vx=cos(ang)*SPEED
    vy=sin(ang)*SPEED
    bullets.append([x1,y1,vx,vy])

def shooterRobot(start,waiting,x1,y1,x2,y2):
    current=time.get_ticks()
    if current-robot_timers[start]>=waiting:
        shoot(x1,y1,x2,y2)
        robot_timers[start]=current
    for b in bullets[:]:
        b[X]+=b[2]
        b[Y]+=b[3]
        if b[X]>1150 or b[X]<0 or b[Y]<0 or b[Y]>697:
            bullets.remove(b)

def robotDeath(hitboxes,robots,timers,poof):
    global level,begin_timer,begin
    if move_list[atckHitbox]:
        index=move_list[atckHitbox].collidelist(hitboxes)
        if index!=-1:
            poof.append([hitboxes[index][X],hitboxes[index][Y],0])
            objects.remove(hitboxes[index])
            del hitboxes[index]
            del robots[index]
            del timers[index]
            blocks[1]+=15
            blocks[0]=blocks[1]-len(rect_list)
    if not robots:
        bullets.clear()
        if begin:
            begin_timer=time.get_ticks()
            begin=False
        current=time.get_ticks()
        if (current-begin_timer)/1000>=60:
            p[X]=0
            p[Y]=425
            level=newLevel(level)

    for i in range(len(poof)):
        if poof[i]:
            if poof[i][2]<7:
                poof[i][2]+=0.3
                screen.blit(poof_pics[int(poof[i][2])],(poof[i][X],poof[i][Y]))
        else:
            del poof[i]
            if len(poof)==0:
                break

def robotsFunction(robot_counter):
    robot_counter=(robot_counter+0.2)%7
    for i in range(len(robots)):
        screen.blit(robot_platform,(robot_hitboxes[i][X]-25,robot_hitboxes[i][Y]+50))
        if robots[i]=="shooter":
            shooterRobot(i,randint(1500,5000),robot_hitboxes[i][X]+25,robot_hitboxes[i][Y]+25,p[X]+20,p[Y]+37)
            if (p[X]+12)>robot_hitboxes[i][X]+30:
                screen.blit(robot_pics[0][int(robot_counter)],(robot_hitboxes[i][X]-20,robot_hitboxes[i][Y]-20))
            else:
                screen.blit(robot_pics[1][int(robot_counter)],(robot_hitboxes[i][X]-10,robot_hitboxes[i][Y]-20))
        elif robots[i]=="map degenerator":
            mapDestroyRobot(i,randint(3000,6000))
            if (p[X]+12)>robot_hitboxes[i][X]+30:
                screen.blit(robot_pics[4][int(robot_counter)],(robot_hitboxes[i][X]-10,robot_hitboxes[i][Y]-20))
            else:
                screen.blit(robot_pics[5][int(robot_counter)],(robot_hitboxes[i][X]-10,robot_hitboxes[i][Y]-20))
        elif robots[i]=="bomber":
            if (p[X]+12)>robot_hitboxes[i][X]+30:
                screen.blit(robot_pics[2][int(robot_counter)],(robot_hitboxes[i][X]-10,robot_hitboxes[i][Y]-20))
            else:
                screen.blit(robot_pics[3][int(robot_counter)],(robot_hitboxes[i][X]-10,robot_hitboxes[i][Y]-20))
        elif robots[i]=="laser":
            if (p[X]+12)>robot_hitboxes[i][X]+30:
                screen.blit(robot_pics[6][int(robot_counter)],(robot_hitboxes[i][X]-10,robot_hitboxes[i][Y]-20))
            else:
                screen.blit(robot_pics[7][int(robot_counter)],(robot_hitboxes[i][X]-10,robot_hitboxes[i][Y]-20))
    return robot_counter

def drawScene():
    screen.fill(bg_colour)
    if level<20:
        level_surface=levelFont.render(str(level),True,(200,200,200))
    else:
        level_surface=levelFont.render("∞",True,(200,200,200))
    screen.blit(level_surface,(575-level_surface.get_width()//2,350-level_surface.get_height()//2))
    for plat in rect_list:
        screen.blit(block,plat)
    for b in bullets:
        draw.circle(screen,GREEN,(int(b[0]),int(b[1])),4)
    row=p_list[0]
    col=int(p_list[1])
    pic=player_pics[row][col]
    screen.blit(pic,(p[X]-17,p[Y]))

def hitWalls(x,y,walls): #this function credited to Mr Macanovik
    playerRect=Rect(x,y,40,75)
    return playerRect.collidelist(walls)!=-1

def newLevel(level):
    global begin,bg_colour
    begin=True
    if level<20:
        level+=1
    robots.clear()
    robot_hitboxes.clear()
    rect_list.clear()
    rect_list.append(Rect(0,500,50,50))
    blocks[0]=blocks[1]-len(rect_list)
    robot_timers.clear()
    bg_colour=(randint(50,205),randint(50,205),randint(50,205))
    for i in range(level):
        robots.append(choice(possibleRobots))
        generatePlatform()
        robot_timers.append(time.get_ticks())
    return level

def movePlayer(p,move_list): #this function credited to Mr Macanovik
    global level
    keys=key.get_pressed()
    v[X]=0
    move_list[img_speed]=0.07
    move_list[atckHitbox]=False
    if move_list[facing]=="right":
        p_list[0]=0
    else:
        p_list[0]=1
    if keys[K_a] and not hitWalls(p[X]-5,p[Y],rect_list):
        v[X]=-5
        move_list[facing]="left"
        if v[Y]==0:
            p_list[0]=3
            move_list[img_speed]=0.15
    if keys[K_d] and not hitWalls(p[X]+5,p[Y],rect_list):
        v[X]=5
        move_list[facing]="right"
        if v[Y]==0:
            p_list[0]=2
            move_list[img_speed]=0.15
    if p[Y]+p[H]==v[2] and v[Y]==0:
        move_list[dJump]="first jump"
    if keys[K_w] and p[Y]+p[H]==v[2] and v[Y]==0:
        v[Y]=jumpPower
    if not keys[K_w] and move_list[dJump]=="first jump":
        move_list[dJump]="double jump available"
    if move_list[dJump]=="double jump available" and keys[K_w]:
        v[Y]=jumpPower
        move_list[dJump]="no jump"
    if v[Y]<0:
        move_list[img_speed]=0.33
        if hitWalls(p[X],p[Y]+v[Y],rect_list) or p[Y]+v[Y]<=0:
            v[Y]=-gravity
        if move_list[facing]=="right":
            p_list[0]=4
        else:
            p_list[0]=5
    if keys[K_LSHIFT]:
        move_list[img_speed]=0.4
        if move_list[facing]=="right":
            if p_list[1]>=4:
                move_list[atckHitbox]=Rect(p[X]+30,p[Y],30,75)
            p_list[0]=6
        else:
            if p_list[1]>=4:
                move_list[atckHitbox]=Rect(p[X]-25,p[Y],30,75)
            p_list[0]=7

    p_list[1]=(p_list[1]+move_list[img_speed])%len(player_pics[p_list[0]])

    p[X]+=v[X]
    if v[Y]<=100:
        v[Y]+=gravity
    
    #phasing through the sides
    if p[X]+p[W]<0:
        p[X]=1150+p[X]+p[W]
    elif p[X]>1150:
        if not robots:
            level=newLevel(level)
        else:
            p[X]=0-p[W]+p[X]-1150

def check(p): #this function credited to Mr Macanovik
    for plat in rect_list:
        if p[X]+p[W]>plat[X] and p[X]<plat[X]+plat[W] and p[Y]+p[H]<=plat[Y] and p[Y]+p[H]+v[Y]>=plat[Y]:
            v[Y]=0
            v[2]=plat[Y]
            p[Y]=plat[Y]-p[H]
    p[Y]+=int(v[Y])

def gaps(x1,y1,x2,y2,map,action):
    gap=[]
    dst=sqrt((x2-x1)**2+(y2-y1)**2)
    dx,dy=x2-x1,y2-y1
    if abs(dx)>=abs(dy):
        side=dy/dx*50
    elif abs(dx)<abs(dy):
        side=dx/dy*50
    hypot=sqrt(50**2+side**2)
    num_squares=int(dst/hypot)
    dx_increase,dy_increase=dx/num_squares,dy/num_squares
    dotX,dotY=omx,omy
    if action=="fill":
        for i in range(num_squares):
            dotX+=dx_increase
            dotY+=dy_increase
            gapfillRect=Rect(roundIt(int(dotX),50),roundIt(int(dotY),50),50,50)
            if gapfillRect not in map:
                gap.append(gapfillRect)
        return gap
    elif action=="erase":
        for i in range(num_squares):
            dotX=omx+dx_increase*i
            dotY=omy+dy_increase*i
            gaperaseRect=Rect(roundIt(int(dotX),50),roundIt(int(dotY),50),50,50)
            if gaperaseRect in map:
                map.remove(gaperaseRect)
        return map

def cleanMap(new_blocks_drawn,map):
    for block in new_blocks_drawn:
        if block.collidelist(objects)!=-1:
            map.remove(block)

def drawMap(x1,y1,x2,y2,map,blocks):
    new_blocks_drawn=[]
    if abs(x1-x2)>50 or abs(y1-y2)>50:
        for block in gaps(x1,y1,x2,y2,map,"fill"):
            if blocks[0]>0:
                blocks[0]=blocks[1]-len(map)
                map.append(block)
                new_blocks_drawn.append(block)
    else:
        drawRect=Rect(x2,y2,50,50)
        if drawRect not in map and blocks[0]>0:
            map.append(drawRect)
            new_blocks_drawn.append(drawRect)
            blocks[0]=blocks[1]-len(map)
    cleanMap(new_blocks_drawn,map)

def eraseMap(x1,y1,x2,y2,map,blocks):
    if abs(x1-x2)>50 or abs(y1-y2)>50:
        map=gaps(x1,y1,x2,y2,map,"erase")
    else:
        eraseRect=Rect(x2,y2,50,50)
        if eraseRect in map:
            map.remove(eraseRect)
    blocks[0]=blocks[1]-len(map)

def animate(lst,counter,speed,x,y):
    screen.blit(lst[int(counter)],(x,y))
    return (counter+speed)%len(lst)

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key==K_w or evt.key==K_LSHIFT:
                p_list[1]=0

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    
    if mb[0]:
        drawMap(roundIt(omx,50),roundIt(omy,50),roundIt(mx,50),roundIt(my,50),rect_list,blocks)
    
    elif mb[2]:
        eraseMap(roundIt(omx,50),roundIt(omy,50),roundIt(mx,50),roundIt(my,50),rect_list,blocks)

    drawScene()
    draw.rect(screen,(220,70,40),lava_background)
    lava_counter=animate(lavaImgs,lava_counter,0.1,0,580)
    robot_counter=robotsFunction(robot_counter)
    robotDeath(robot_hitboxes,robots,robot_timers,poof_list)
    movePlayer(p,move_list)
    screen.blit(block_count_icon,(20,610))
    block_count=blockFont.render(str(blocks[0]),True,BLUE)
    screen.blit(block_count,(100,610))
    check(p)
    checkDeath()
    myClock.tick(60)
    display.update()
    omx,omy=mx,my
quit()
