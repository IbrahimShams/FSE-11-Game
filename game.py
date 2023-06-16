#TO DO
#make robot_platforms and robot_actual_hitbox in robot hitboxes
#dont do robot health bars yet, do level transitions
#block count collisions with map degenerator, shooter, and bomber
#finish the levelling system
#player block count display
#player health (blocks, health, and lava)

from pygame import *
from math import *
from random import *

font.init()

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
lava_counter,robot_counter=0,0
block=image.load("block2.png").convert()
rect_list=[Rect(0,500,50,50)]
omx,omy=0,0
lavaImgs=[image.load("lava/lava00"+f"{i}"+".png").convert() for i in range(6)]
lava_background=Rect(0,597,1150,100)
no_spawn_region=Rect(0,325,200,175)
jumpPower=-7
move_list=["no jump","right",0.07,False]
dJump,facing,img_speed,atckHitbox=0,1,2,3
gravity=0.3
X,Y,W,H=0,1,2,3
start_timer,start_timer1,start_timer2=time.get_ticks(),time.get_ticks(),time.get_ticks()
SPEED=15
begin_timer=False
begin=True
comicFont=font.SysFont("Comic Sans MS",40)

v=[0,0,697]
p=Rect(0,300,40,75)
p_list=[0,0]
objects=[lava_background,p]
bullets=[]

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
robot_pics.append(addPics("robots","tile",168,175)) #floater robot pics right
robot_pics.append(flipPics(robot_pics[6])) #floater robot pics left
robot_pics.append(addPics("robots","tile",176,183)) #laser robot pics right
robot_pics.append(flipPics(robot_pics[8])) #laser robot pics left

possibleRobots=["shooter","bomber","map degenerator"] #laser, floater
robots=[choice(possibleRobots)]
level=1
blocks=[20,20]
robot_timers=[time.get_ticks()]

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
        b[0]+=b[2]
        b[1]+=b[3]
        if b[0]>1150 or b[0]<0 or b[1]<0 or b[1]>697:
            bullets.remove(b)

def robotDeath(hitboxes,robots,timers):
    global level,begin_timer,begin
    if move_list[atckHitbox]:
        index=move_list[atckHitbox].collidelist(robot_hitboxes)
        if index!=-1:
            objects.remove(hitboxes[index])
            del hitboxes[index]
            del robots[index]
            del timers[index]
            blocks[1]+=20
            blocks[0]=blocks[1]-len(rect_list)
    if not robots:
        if begin:
            begin_timer=time.get_ticks()
            begin=False
        current=time.get_ticks()
        if (current-begin_timer)/1000>=60:
            p[X]=0
            p[Y]=425
            level=newLevel(level)

def robots_function(robot_counter):
    robot_counter=(robot_counter+0.2)%7
    for i in range(len(robots)):
        if robots[i]=="shooter":
            shooterRobot(i,3000,robot_hitboxes[i][0]+25,robot_hitboxes[i][1]+25,p[0]+20,p[1]+37)
            if (p[0]+12)>robot_hitboxes[i][0]+30:
                screen.blit(robot_pics[0][int(robot_counter)],(robot_hitboxes[i][0]-20,robot_hitboxes[i][1]-20))
            else:
                screen.blit(robot_pics[1][int(robot_counter)],(robot_hitboxes[i][0]-10,robot_hitboxes[i][1]-20))
        elif robots[i]=="map degenerator":
            mapDestroyRobot(i,5000)
            if (p[0]+12)>robot_hitboxes[i][0]+30:
                screen.blit(robot_pics[4][int(robot_counter)],(robot_hitboxes[i][0]-10,robot_hitboxes[i][1]-20))
            else:
                screen.blit(robot_pics[5][int(robot_counter)],(robot_hitboxes[i][0]-10,robot_hitboxes[i][1]-20))
        elif robots[i]=="bomber":
            if (p[0]+12)>robot_hitboxes[i][0]+30:
                screen.blit(robot_pics[2][int(robot_counter)],(robot_hitboxes[i][0]-10,robot_hitboxes[i][1]-20))
            else:
                screen.blit(robot_pics[3][int(robot_counter)],(robot_hitboxes[i][0]-10,robot_hitboxes[i][1]-20))
    return robot_counter

def drawScene():
    screen.fill(BLUE)
    for plat in rect_list:
        screen.blit(block,plat)
    for b in bullets:
        draw.circle(screen,GREEN,(int(b[0]),int(b[1])),4)
    if move_list[atckHitbox]:
        draw.rect(screen,RED,move_list[atckHitbox],1)
    row=p_list[0]
    col=int(p_list[1])
    pic=player_pics[row][col]
    screen.blit(pic,(p[0]-17,p[1]))

def hitWalls(x,y,walls):
    playerRect=Rect(x,y,40,75)
    return playerRect.collidelist(walls)!=-1

def newLevel(level):
    global begin
    begin=True
    level+=1
    robots.clear()
    robot_hitboxes.clear()
    rect_list.clear()
    rect_list.append(Rect(0,500,50,50))
    robot_timers.clear()
    for i in range(level):
        robots.append(choice(possibleRobots))
        generatePlatform()
        robot_timers.append(time.get_ticks())
    return level

def movePlayer(p,move_list):
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
        move_list[img_speed]=0.2
        if move_list[facing]=="right":
            if p_list[1]>=4:
                move_list[atckHitbox]=Rect(p[0]+30,p[1],30,75)
            p_list[0]=6
        else:
            if p_list[1]>=4:
                move_list[atckHitbox]=Rect(p[0]-25,p[1],30,75)
            p_list[0]=7

    p_list[1]=(p_list[1]+move_list[img_speed])%len(player_pics[p_list[0]])

    p[X]+=v[X]
    if v[Y]<=100:
        v[Y]+=gravity
    
    #phasing through the sides
    if p[0]+p[W]<0:
        p[0]=1150+p[0]+p[W]
    elif p[0]>1150:
        if not robots:
            level=newLevel(level)
        else:
            p[0]=0-p[W]+p[0]-1150          
    
def check(p):
    current=time.get_ticks()
    for plat in rect_list:
        if p[X]+p[W]>plat[X] and p[X]<plat[X]+plat[W] and p[Y]+p[H]<=plat[Y] and p[Y]+p[H]+v[Y]>=plat[Y]:
            v[Y]=0
            v[2]=plat[Y]
            p[Y]=plat[Y]-p[H]
    p[Y]+=int(v[Y])

for img in lavaImgs:
    img.set_colorkey(BLACK)

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
                blocks[0]=blocks[1]-len(rect_list)
                map.append(block)
                new_blocks_drawn.append(block)
    else:
        drawRect=Rect(x2,y2,50,50)
        if drawRect not in map and blocks[0]>0:
            map.append(drawRect)
            new_blocks_drawn.append(drawRect)
            blocks[0]=blocks[1]-len(rect_list)
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
    block_count=comicFont.render(str(blocks[0]),True,BLACK)
    screen.blit(block_count,(50,550))
    movePlayer(p,move_list)
    check(p)
    robot_counter=robots_function(robot_counter)
    robotDeath(robot_hitboxes,robots,robot_timers)
    print(blocks[0])
    myClock.tick(60)
    print(robots)
    display.update()
    omx,omy=mx,my
quit()
