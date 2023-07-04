#block count problem, score resetting problem
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
PURPLE=(102,0,255)
myClock=time.Clock()
score1=[0,0] #first one is the score, second one is the number of robot kills. every robot you kill, your score gets added by your level number. ex. level1: each robot is 1 point. level 17: each robot is worth 17 points. It maxes out at level 20, which is considered the "infinite level", because the maximum number of everything happens in level 20 and after level 20.

def gameOver():
    """this is a page that you get after dying. it shows 2 buttons: main menu and play again. You can click any two of the buttons and it will either go to main menu or restart the game. It will also display your final score and total kills."""
    running=True
    buttons=[Rect(450,400+y*100,250,75) for y in range(2)]
    endFont=font.SysFont("Comic Sans MS",40)
    while running:
        screen.fill((0,247,255))
        for evt in event.get():
            if evt.type==QUIT:
                return "exit"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    if buttons[0].collidepoint(mx,my):
                        return "play"
                    if buttons[1].collidepoint(mx,my):
                        return "menu"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        for b in buttons:
            draw.rect(screen,BLUE,b)
            if b.collidepoint(mx,my):
                draw.rect(screen,WHITE,b,5)
        deathSurf=endFont.render(f"You Died!",True,RED)
        scoreSurf=endFont.render(f"Final Score: {score1[0]}",True,RED)
        killsSurf=endFont.render(f"Total Kills: {score1[1]}",True,RED)
        screen.blit(deathSurf,(485,100))
        screen.blit(scoreSurf,(450,140))
        screen.blit(killsSurf,(450,180))
        playSurf=endFont.render("Play",True,RED)
        menuSurf=endFont.render("Menu",True,RED)
        screen.blit(playSurf,(buttons[0][0]+60,buttons[0][1]))
        screen.blit(menuSurf,(buttons[1][0]+60,buttons[1][1]))
        display.flip()

def menu():
    """this is the menu which shows the thumbnail of the game and shows three buttons: play, instructions, and recent scores. you can click any and go to that page."""
    running=True
    menu_img=image.load("menu_img.png")
    menu_img=transform.scale(menu_img,(1150,697)).convert()
    buttons=[Rect(37,315+y*127,363,96) for y in range(3)]
    while running:
        screen.blit(menu_img,(0,0))
        for evt in event.get():
            if evt.type==QUIT:
                return "exit"
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1:
                    if buttons[0].collidepoint(mx,my):
                        return "play"
                    if buttons[1].collidepoint(mx,my):
                        return "instructions"
                    if buttons[2].collidepoint(mx,my):
                        return "recent scores"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        for b in buttons:
            if b.collidepoint(mx,my):
                draw.rect(screen,PURPLE,b,5)
        display.flip()

def instructions():
    """this is the instructions page you get to after clicking instructions. it has a back button going to main menu, and it blits an image of instructions that i made."""
    running=True
    instructions_img=image.load("instructions.png").convert()
    backButton=Rect(1070,620,50,50)
    back_img=image.load("back_button.png")
    back_img=transform.scale(back_img,(50,50)).convert_alpha()
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                return "exit"
        screen.fill((0,247,255))
        screen.blit(instructions_img,(125,50))
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        screen.blit(back_img,backButton)
        if backButton.collidepoint(mx,my):
            draw.rect(screen,PURPLE,backButton,2)
            if mb[0]:
                return "menu"
        display.flip()

def recentScores():
    """this is a page that you get after you click the button on main menu. it shows the last 5 recent scores on a blue background and has a back button. it returns to menu if you click back button"""
    running=True
    backButton=Rect(1070,620,50,50)
    back_img=image.load("back_button.png")
    back_img=transform.scale(back_img,(50,50)).convert_alpha()
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                return "exit"
        screen.fill((0,247,255))
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        screen.blit(back_img,backButton)
        if backButton.collidepoint(mx,my):
            draw.rect(screen,PURPLE,backButton,2)
            if mb[0]:
                return "menu"
        display.flip()

def play(score):
    global level,begin_timer,begin,bg_colour,running
    #general variables
    running=True
    bg_colour=(randint(50,205),randint(50,205),randint(50,205)) #bg colour random
    omx,omy=0,0 #old mouse x mouse y
    rect_list=[Rect(0,500,50,50)] #list of all the blocks (rects) player places

    #Image paths, counters, and image variables
    lava_counter,robot_counter=0,0
    block=image.load("block2.png").convert()
    block_count_icon=image.load("block_count_icon.png")
    block_count_icon=transform.scale(block_count_icon,(60,60)).convert_alpha()
    robot_kills_icon=image.load("robot.png")
    robot_kills_icon=transform.scale(robot_kills_icon,(60,60)).convert_alpha()
    robot_platform=image.load("robot_platform.png").convert_alpha()
    menu_icon=image.load("menu_icon.png").convert()
    spike=image.load("spike.png").convert()
    spike.set_colorkey(WHITE)
    menuButton=Rect(1050,620,48,33)
    lavaImgs=[image.load("lava/lava00"+f"{i}"+".png").convert() for i in range(6)]
    lava_background=Rect(0,625,1150,72)
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
    SPEED=8 #speed of bullet
    begin_timer=False #timing robot
    begin=True #a variable to control timer, when to start and when to finish
    no_spawn_region=Rect(0,325,200,175) #robots cant spawn in this rect
    objects=[lava_background,p] #the objects you cant draw on
    bullets=[] #bullets 2d list. includes a list for each bullet with x,y,vx,vy
    bulletRects=[]

    #game system variables (level and blocks)
    level=1
    blocks=[15,15] #the 2nd one is your maximum amount of blocks you can place and your first one is the amount of blocks you have with you minus the ones you have placed.
    blockFont=font.SysFont("Comic Sans MS",40) #fonts for block, level, and scores
    levelFont=font.SysFont("Arial",250)
    scoresFont=font.SysFont("Arial",25)

    def flipPics(lst):
        """this funcion takes in a list of imgs and flips them horizontally"""
        return [transform.flip(image,True,False) for image in lst]

    def addPics(source,name,start,end):
        """this funcion takes in a folder name, the consistent names of images in the folder, and a start and end index. it appends images from that folder with the index and returns a list"""
        mypics=[]
        for i in range(start,end+1):
            img=image.load(f"{source}/{name}{i:03}.png").convert_alpha()
            img=transform.scale(img,(75,75))
            mypics.append(img)
        return mypics
    
    #player pics different actions facing left and right 2d list
    player_pics=[]
    player_pics.append(addPics("player","tile",0,4)) #idle right
    player_pics.append(flipPics(player_pics[0])) #idle left
    player_pics.append(addPics("player","tile",24,31)) #walking right
    player_pics.append(flipPics(player_pics[2])) #walking left
    player_pics.append(addPics("player","tile",40,47)) #jumping right
    player_pics.append(flipPics(player_pics[4])) #jumping left
    player_pics.append(addPics("player","tile",64,71)) #attack right
    player_pics.append(flipPics(player_pics[6])) #attack left

    #robot pics 2d list of different robots
    robot_pics=[]
    robot_pics.append(addPics("robots","tile",88,95)) #shooter robot pics right
    robot_pics.append(flipPics(robot_pics[0])) #shooter robot pics left
    robot_pics.append(addPics("robots","tile",104,111)) #bomber robot pics right
    robot_pics.append(flipPics(robot_pics[2])) #bomber robot pics left
    robot_pics.append(addPics("robots","tile",48,55)) #map degenerator robot pics right
    robot_pics.append(flipPics(robot_pics[4])) #map degenerator robot pics left
    robot_pics.append(addPics("robots","tile",176,183)) #laser robot pics right
    robot_pics.append(flipPics(robot_pics[6])) #laser robot pics left
    
    #more robot variables (list of types, related list of delays for each type)
    possibleRobots=["shooter","map degenerator","laser"]
    possibleDelays=[(1500,4000),(2000,5000),(5000,8000)]
    robots=[choice(possibleRobots)] #the robots in each level (string list)
    robot_timers=[time.get_ticks()] #the timers for each robot action in each level
    robotDelays=[randint(possibleDelays[possibleRobots.index(robots[0])][0],possibleDelays[possibleRobots.index(robots[0])][1])] #the robot delays for each robot. (they are randomized every time the robot does something)
    #the above lists are all related

    #pictures of poof animation
    poof_pics=addPics("poof","tile",0,7)
    poof_list=[]

    def patchBlocks():
        if len(rect_list)>blocks[1]:
            blocks[0]=0

    def checkDeath():
        global running
        if p[Y]>=600 or blocks[1]<=0:
            running=False

    def roundIt(num,round_num):
        """this function takes in a number and a round number and then rounds that number down to the nearest round number (ex roundIt(127,20) -> 120). This is for the square grid of the game"""
        n=0
        for i in range(0,num+1,round_num):
            if i+round_num>num:
                n=i
        return n

    #the robot hitboxes
    robot_hitboxes=[Rect(roundIt(randint(0,1100),50),roundIt(randint(0,500),50),50,50)]
    while robot_hitboxes[0].colliderect(no_spawn_region):
        robot_hitboxes=[Rect(roundIt(randint(0,1100),50),roundIt(randint(0,500),50),50,50)]
    objects.append(robot_hitboxes[0])

    def generateHitbox():
        """this function generates a robot hitbox that doesnt collide with the no spawn region and doesnt collide with any other robot hitbox"""
        while True:
            robotHitbox=Rect(roundIt(randint(0,1100),50),roundIt(randint(0,500),50),50,50)
            if not robotHitbox.colliderect(no_spawn_region) and robotHitbox.collidelist(robot_hitboxes)==-1:
                robot_hitboxes.append(robotHitbox)
                objects.append(robotHitbox)
                break

    def destroyMap(map):
        """this function is called whenever the map destroyer robots need to destroy the map. it simply removes a rectangle from the list that is the map"""
        if len(map)>0:
            block=choice(map)
            map.remove(block)
            if blocks[1]>0:
                blocks[1]-=1
        blocks[0]=blocks[1]-len(map)

    def mapDestroyRobot(start,waiting_lst,pos):
        """this is the map destroyer robot function. it is identical to all the other robot functions in structure. there is a timer system (with a randomized waiting time which was mentioned above) and the destoryMap function is called when the timer goes off"""
        current=time.get_ticks()
        if current-robot_timers[start]>=waiting_lst[pos]:
            destroyMap(rect_list)
            robot_timers[start]=current
            waiting_lst[pos]=randint(possibleDelays[possibleRobots.index(robots[pos])][0],possibleDelays[possibleRobots.index(robots[pos])][1])

    def shoot(x1,y1,x2,y2):
        """this function is called when the shooter robot shoots. it calculates the angle using trig to aim at the player and then append the x,y,vx,vy to the bullets list. there is a bulletRects list that is simply a copy paste of the bullets list but with rectangles to check if the bullet hit the player"""
        ang=atan2(y2-y1+38,x2-x1+12)
        vx=cos(ang)*SPEED
        vy=sin(ang)*SPEED
        bullets.append([x1,y1,vx,vy])
        bulletRects.append(Rect(x1,y1,2,2))

    def shooterRobot(start,waiting_lst,pos,x1,y1,x2,y2):
        """this function is similar in structure to all the othe robot functions. it has a timer system, when timer goes off, it takes the fixed x,y of the player and called shoot(). Then, it makes each bullet in the bullet list move by adding vx and vy to the x and y. it checks if the bullet hit the player or went off the screen and removes the bullet in that case"""
        current=time.get_ticks()
        if current-robot_timers[start]>=waiting_lst[pos]:
            shoot(x1,y1,x2,y2)
            robot_timers[start]=current
            waiting_lst[pos]=randint(possibleDelays[possibleRobots.index(robots[pos])][0],possibleDelays[possibleRobots.index(robots[pos])][1])
        for b in bullets[:]:
            b[X]+=b[2]
            b[Y]+=b[3]
            bullet_idx=bullets.index(b)
            bulletRects[bullet_idx][X]+=b[2]
            bulletRects[bullet_idx][Y]+=b[3]
            if bulletRects[bullet_idx].collidelist(rect_list)!=-1:
                del bulletRects[bullet_idx]
                bullets.remove(b)
            elif b[X]>1150 or b[X]+2<0 or b[Y]+2<0 or b[Y]>697:
                del bulletRects[bullets.index(b)]
                bullets.remove(b)
            elif p.collidelist(bulletRects)!=-1:
                blocks[1]-=5
                blocks[0]=blocks[1]-len(rect_list)
                idx=p.collidelist(bulletRects)
                del bulletRects[idx]
                del bullets[idx]

    def robotDeath(hitboxes,robots,timers,poof,game_score):
        """this function deals with when robots are killed. it checks if the player colllided with the robot hitbox list. if so, it deletes the robot from all the related lists. you also get blocks."""
        global level,begin_timer,begin
        if move_list[atckHitbox]:
            index=move_list[atckHitbox].collidelist(hitboxes)
            if index!=-1:
                poof.append([hitboxes[index][X],hitboxes[index][Y],0])
                objects.remove(hitboxes[index])
                del hitboxes[index]
                del robots[index]
                del timers[index]
                del robotDelays[index]
                blocks[1]+=5
                blocks[0]=blocks[1]-len(rect_list)
                game_score[0]+=level
                game_score[1]+=1

        if not robots: #if all robots are dead, there is a timer that goes for 60 seconds which automatically spawns you to the next level after 60 seconds.
            bullets.clear()
            if begin:
                begin_timer=time.get_ticks()
                begin=False
            current=time.get_ticks()
            if (current-begin_timer)/1000>=60:
                p[X]=0
                p[Y]=425
                level=newLevel(level)

        for i in range(len(poof)): #this is the poof animation for each killed robot
            if poof[i]:
                if poof[i][2]<7:
                    poof[i][2]+=0.3
                    screen.blit(poof_pics[int(poof[i][2])],(poof[i][X],poof[i][Y]))
            else:
                del poof[i]
                if len(poof)==0:
                    break
        
    def robotsFunction(robot_counter):
        """this function is the main robots function. it blits a different animation image for each robot in robots list (there is a facing left and right) and calls each functions for each robot in robots list."""
        robot_counter=(robot_counter+0.2)%7
        for i in range(len(robots)):
            screen.blit(robot_platform,(robot_hitboxes[i][X]-25,robot_hitboxes[i][Y]+50))
            if robots[i]=="shooter":
                shooterRobot(i,robotDelays,i,robot_hitboxes[i][X]+25,robot_hitboxes[i][Y]+25,p[X]+20,p[Y]+37)
                if (p[X]+12)>robot_hitboxes[i][X]+30:
                    screen.blit(robot_pics[0][int(robot_counter)],(robot_hitboxes[i][X]-20,robot_hitboxes[i][Y]-20))
                else:
                    screen.blit(robot_pics[1][int(robot_counter)],(robot_hitboxes[i][X]-10,robot_hitboxes[i][Y]-20))
            elif robots[i]=="map degenerator":
                mapDestroyRobot(i,robotDelays,i)
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
        """this function draws the scene of the game. it draws the level number, the screen fill, the map, the player animations, and the bullets."""
        screen.fill(bg_colour)
        if level<20:
            level_surface=levelFont.render(str(level),True,(200,200,200))
        else:
            level_surface=levelFont.render("∞",True,(200,200,200))
        screen.blit(level_surface,(575-level_surface.get_width()//2,350-level_surface.get_height()//2))
        for plat in rect_list:
            screen.blit(block,plat)
        for b in bulletRects:
            screen.blit(spike,(b[0]-12,b[1]-12))
        row=p_list[0]
        col=int(p_list[1])
        pic=player_pics[row][col]
        screen.blit(pic,(p[X]-17,p[Y]))

    def hitWalls(x,y,walls):
        """this function  checks if the player hit the map so the player doesnt phase through the map."""
        playerRect=Rect(x,y,40,75)
        return playerRect.collidelist(walls)!=-1

    def newLevel(level):
        """this function is called when a new level needs to be created. all the robot related lists are cleared, the map is cleared (so your blocks can be transferred to the next level), and new robots are generated based no the number of the level."""
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
        robotDelays.clear()
        bullets.clear()
        bulletRects.clear()
        bg_colour=(randint(50,205),randint(50,205),randint(50,205))
        for i in range(level):
            robots.append(choice(possibleRobots))
            robotDelays.append(randint(possibleDelays[possibleRobots.index(robots[-1])][0],possibleDelays[possibleRobots.index(robots[-1])][1]))
            generateHitbox()
            robot_timers.append(time.get_ticks())
        return level

    def movePlayer(p,move_list):
        """this function moves the player and deals with a variable (list) that controls player animation. the player can move left and right (without phasing through the map) and can jump in this function. Also, the player attacking mechanicsm is in this function. (If player clicks shift, an attack hitbox shows up beside the player)."""
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
        if p[Y]+p[H]==v[2] and v[Y]==0: #jumping mechanism. (double jump also present)
            move_list[dJump]="first jump"
        if keys[K_SPACE] and p[Y]+p[H]==v[2] and v[Y]==0:
            v[Y]=jumpPower
        if not keys[K_SPACE] and move_list[dJump]=="first jump":
            move_list[dJump]="double jump available"
        if move_list[dJump]=="double jump available" and keys[K_SPACE]:
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
        if keys[K_r]: #attacking
            move_list[img_speed]=0.4
            if move_list[facing]=="right":
                if p_list[1]>=4:
                    move_list[atckHitbox]=Rect(p[X]+30,p[Y],30,75)
                p_list[0]=6
            else:
                if p_list[1]>=4:
                    move_list[atckHitbox]=Rect(p[X]-25,p[Y],30,75)
                p_list[0]=7
        
        #player animations
        p_list[1]=(p_list[1]+move_list[img_speed])%len(player_pics[p_list[0]])
        
        #movement velocity
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

    def check(p):
        """this function checks if a player landed on the map. if they did, it stops the player from going straight through the map by stopping their velocity"""
        for plat in rect_list:
            if p[X]+p[W]>plat[X] and p[X]<plat[X]+plat[W] and p[Y]+p[H]<=plat[Y] and p[Y]+p[H]+v[Y]>=plat[Y]:
                v[Y]=0
                v[2]=plat[Y]
                p[Y]=plat[Y]-p[H]
        p[Y]+=int(v[Y])

    def gaps(x1,y1,x2,y2,map,action):
        """this function fills the gaps when the player draws rectangles using slops and pythagorean theorem. there is an action parameter that determines whether the player will be drawing or erasing, but the gaps works for both actions."""
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
        """this function makes sure the player doesnt draw on certain objects like itself, the robots, and the lava. if there are blocks on these objects, they are removed from the list."""
        for block in new_blocks_drawn:
            if block.collidelist(objects)!=-1:
                map.remove(block)

    def drawMap(x1,y1,x2,y2,map,blocks):
        """this is the function where the player draws the map. either they draw it slowly and a rect is appended to the map for where their mouse is at, or they draw it fast which requires the gap fill function."""
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
        """this function is for erasing the map, which also includes drawing quickly and slowly just like the drawMap function."""
        if abs(x1-x2)>50 or abs(y1-y2)>50:
            map=gaps(x1,y1,x2,y2,map,"erase")
        else:
            eraseRect=Rect(x2,y2,50,50)
            if eraseRect in map:
                map.remove(eraseRect)
        blocks[0]=blocks[1]-len(map)

    def animate(lst,counter,speed,x,y):
        """this is an animation function that takes in a list of images and blits the image at the counter. It added a certain amount to the counter every time (speed parameter) and returns the counter to be updated."""
        screen.blit(lst[int(counter)],(x,y))
        return (counter+speed)%len(lst)

    while running: #this is the while running loop where all the functions are called
        for evt in event.get():
            if evt.type==QUIT:
                return "exit"
            if evt.type==KEYDOWN:
                if evt.key==K_SPACE or evt.key==K_r:
                    p_list[1]=0
            if evt.type==MOUSEBUTTONDOWN:
                if evt.button==1 and menuButton.collidepoint(mx,my):
                    return "menu"
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
        if mb[2]:
            drawMap(roundIt(omx,50),roundIt(omy,50),roundIt(mx,50),roundIt(my,50),rect_list,blocks)
            
        elif mb[0]:
            eraseMap(roundIt(omx,50),roundIt(omy,50),roundIt(mx,50),roundIt(my,50),rect_list,blocks)

        drawScene()
        draw.rect(screen,(220,70,40),lava_background)
        lava_counter=animate(lavaImgs,lava_counter,0.1,0,580)
        robot_counter=robotsFunction(robot_counter)
        robotDeath(robot_hitboxes,robots,robot_timers,poof_list,score)
        movePlayer(p,move_list)
        screen.blit(block_count_icon,(20,610))
        block_count=blockFont.render(str(blocks[0]),True,BLUE)
        screen.blit(block_count,(100,610))
        scoreSurf=scoresFont.render(f"Score: {score[0]}",True,BLACK)
        killsSurf=scoresFont.render(f"Kills: {score[1]}",True,BLACK)
        screen.blit(menu_icon,menuButton)
        screen.blit(scoreSurf,(5,5))
        screen.blit(killsSurf,(1075,5))
        check(p)
        checkDeath()
        patchBlocks()
        myClock.tick(60)
        display.update()
        omx,omy=mx,my
    return "game over"

#This is the menu system. There is a page variable that controls where we are at the menu and calls a different function based on what it is. (if page = play, the play function is called which is the game.)
page="menu"
while page!="exit":
    if page=="menu":
        page=menu()
    if page=="play":
        page=play(score1)
    if page=="instructions":
        page=instructions()
    if page=="recent scores":
        page=recentScores()
    if page=="game over":
        page=gameOver()
quit()
