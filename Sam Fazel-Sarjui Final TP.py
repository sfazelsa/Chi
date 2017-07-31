# Sam Fazel-Sarjui 
# sfazelsa
# 15-112 term project

from pykinect2 import PyKinectV2, PyKinectRuntime 
from pykinect2.PyKinectV2 import * 
import ctypes 
import _ctypes 
import pygame 
import sys 
import math 
import random
import os

#TO KEEP TRACK OF HIGH SCORES
highScoreList=[]


class GameRuntime(pygame.sprite.Sprite): 

    #This code with the following pass statements are derived from Lucas from CMU Spring 15-112
    def init(self):
        pass
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        return self._keys.get(key, False)


    def __init__(self): 
        pygame.init() 
        self.screen_width = 960 
        self.screen_height = 540 
        self.bird_height = self.screen_height/2 
        self.prev_right_hand_height = 0 
        self.prev_left_hand_height = 0 
        self.cur_right_hand_height = 0 
        self.cur_left_hand_height = 0
        self.prev_right_hand_width=0
        self.prev_left_hand_width=0
        self.cur_right_hand_width=0
        self.cur_left_hand_width=0
        self.radius=1 
        self.hoopX=200
        self.hoopY=self.screen_height//2
        self.obsX=400
        self.obsY=self.screen_height//2
        self.margin=75
        #degree of how much the person is tilting
        self.tilt=0
        self.score=0
        #which way the person is leaning
        self.lean=None
        #Margin for dtermining if the hoop is centered
        self.scoringMargin=100
        #increments score by 2
        self.level=1
        # Used to manage how fast the screen updates 
        self._clock = pygame.time.Clock() 
        # Set the width and height of the window [width/2, height/2] 
        self._screen = pygame.display.set_mode((960,540)) 
        # Loop until the user clicks the close button. 
        self._done = False
        # Kinect runtime object, we want color and body frames  
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body) 

        # here we will store skeleton data  
        self._bodies = None 
        #saves background image
        self.plane = pygame.image.load('plane.png').convert_alpha()
        self.ada= pygame.image.load('anil.gif').convert_alpha()
        #self.ada = pygame.transform.scale(self.ada, (200, 200))
        self.adaX=300
        self.adaY=self.screen_height
        self.adaHeight=250
        self.adaWidth=250
        self.image = pygame.image.load('sky.JPG').convert_alpha()
        self.image = pygame.transform.scale(self.image, (960, 540))
        self.back= pygame.image.load('back.JPG').convert_alpha()
        self.back = pygame.transform.scale(self.back, (960, 540))
        self.gravity=2
        self.flap=0
        self.hoopList=[1]
        self.completedList=[]
        self.lives=3
        self.mode=1
        self.obstacleRad=1
        #checks if there is an obstacle on the board
        self.liveBool=False
        self.hitObstacles=False
        self.gameCounter=0
        #determines whne to display missed screen
        self.missed=None
        #Sound
        self.losingSound=pygame.mixer.Sound("sound.wav")
        #level up sound
        self.levelUp=pygame.mixer.Sound("level.wav")
        #extra life sound
        self.cash= pygame.mixer.Sound("cash.wav")
        #tracks hand state
        self.handState=False
        self.clap=False
        #used for the extra life feature
        self.prevCounter=0
        
        
        
    #defines each button click
    def buttonClick(self,click,mousePos):
        if mousePos[0]>300 and mousePos[0]<400 and mousePos[1]>350 and mousePos[1]<400:
            if click[0] == 1:
                self.mode=1
                #if start is clicked...run the actual game
                game = GameRuntime() 
                game.run()

        #changes mode when each button is clicked
        if self.mode==1 or self.mode==2:
            if mousePos[0]>600 and mousePos[0]<710 and mousePos[1]>350 and mousePos[1]<400:
                if click[0] == 1:
                    self.mode=2

        #back button
        if self.mode==2 or self.mode==3 or self.mode==4:
            if mousePos[0]>450 and mousePos[0]<550 and mousePos[1]>350 and mousePos[1]<400:
                if click[0] == 1:
                    self.mode=1
        # if the user lost in the game    
        if self.mode==3:
            if mousePos[0]>600 and mousePos[0]<750 and mousePos[1]>350 and mousePos[1]<400:
                if click[0] == 1:
                    self.mode=4

    #intro screen
    def gameIntro(self):

        intro=True
        while intro:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if self.mode==1:
                self._screen.fill((0,0,0))
                self._screen.blit(self.back,(0,0))
                text = pygame.font.Font('freesansbold.ttf',60)
                TextSurf=text.render("Wormhole Racing",True,(255,255,255))
                txtCenter = ((self.screen_width//4),(self.screen_height//3))
                self._screen.blit(TextSurf, txtCenter)

                pygame.draw.rect(self._screen,(0,0,0),(600,350,100,50))

                mousePos=pygame.mouse.get_pos()

                if mousePos[0]>300 and mousePos[0]<400 and mousePos[1]>350 and mousePos[1]<400:
                    pygame.draw.rect(self._screen,(128,128,128),(300,350,100,50))
                else:
                    pygame.draw.rect(self._screen,(0,0,0),(300,350,100,50))

                if mousePos[0]>600 and mousePos[0]<710 and mousePos[1]>350 and mousePos[1]<400:
                    pygame.draw.rect(self._screen,(128,128,128),(600,350,110,50))
                else:
                    pygame.draw.rect(self._screen,(0,0,0),(600,350,110,50))

                #BUTTON 1 text
                text = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=text.render("Start",True,(255,255,255))
                txtCenter = ((325),(370))
                self._screen.blit(TextSurf, txtCenter)

                #BUTTON 2 text
                text = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=text.render("Directions",True,(255,255,255))
                txtCenter = ((605),(370))
                self._screen.blit(TextSurf, txtCenter)

                click= pygame.mouse.get_pressed()

                self.buttonClick(click,mousePos)

            #differetn modes for the different buttons
            if self.mode==2:
                self._screen.fill((255,255,255))
                self._screen.blit(self.back,(0,0))

                mousePos=pygame.mouse.get_pos()
                click= pygame.mouse.get_pressed()

                #back button
                if mousePos[0]>450 and mousePos[0]<550 and mousePos[1]>350 and mousePos[1]<400:
                    pygame.draw.rect(self._screen,(128,128,128),(450,350,100,50))
                else:
                    pygame.draw.rect(self._screen,(0,0,0),(450,350,100,50))



                #BUTTON to Main Menu
                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Back",True,(255,255,255))
                txtCenter = ((475),(370))
                self._screen.blit(TextSurf, txtCenter)

                #title
                txt = pygame.font.Font('freesansbold.ttf',40)
                TextSurf=txt.render("DIRECTIONS",True,(255,255,255))
                txtCenter = ((350),(25))
                self._screen.blit(TextSurf, txtCenter)

                #game directions
                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("To play flap your wings to fight gravity!",True,(255,255,255))
                txtCenter = ((200),(80))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Fly through the wormhole (black circle) by tilting your arms",True,(255,255,255))
                txtCenter = ((200),(100))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("This game is interactive",True,(255,255,255))
                txtCenter = ((200),(120))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("You have 3 lives",True,(255,255,255))
                txtCenter = ((200),(140))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Avoid the blue obstacles",True,(255,255,255))
                txtCenter = ((200),(160))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Blue obstacles dissapear quicker",True,(255,255,255))
                txtCenter = ((200),(180))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Level up every 5 successful flights",True,(255,255,255))
                txtCenter = ((200),(200))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("You can get an extra life by clapping your hands when Prof. Ada is on the screen!",True,(255,255,255))
                txtCenter = ((200),(220))

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("To pause the game...",True,(255,255,255))
                txtCenter = ((200),(240))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("You need to bring both of your hands together at your hip",True,(255,255,255))
                txtCenter = ((200),(260))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("While holding this position, the game is paused...",True,(255,255,255))
                txtCenter = ((200),(280))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("To resume go back to wing position",True,(255,255,255))
                txtCenter = ((200),(300))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Good Luck!",True,(255,255,255))
                txtCenter = ((200),(320))
                self._screen.blit(TextSurf, txtCenter)


                self._screen.blit(TextSurf, txtCenter)
                self.buttonClick(click,mousePos)

            if self.mode==3:

                self._screen.fill((255,255,255))
                self._screen.blit(self.back,(0,0))

                mousePos=pygame.mouse.get_pos()
                click= pygame.mouse.get_pressed()

               #back button
                if mousePos[0]>450 and mousePos[0]<550 and mousePos[1]>350 and mousePos[1]<400:
                    pygame.draw.rect(self._screen,(128,128,128),(450,350,100,50))
                else:
                    pygame.draw.rect(self._screen,(0,0,0),(450,350,100,50))

                #High Score button
                if mousePos[0]>600 and mousePos[0]<700 and mousePos[1]>350 and mousePos[1]<400:
                    pygame.draw.rect(self._screen,(128,128,128),(600,350,100,50))
                else:
                    pygame.draw.rect(self._screen,(0,0,0),(600,350,100,50))

                #BUTTON to Main Menu
                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Back",True,(255,255,255))
                txtCenter = ((475),(370))
                self._screen.blit(TextSurf, txtCenter)

                #button to leaderboard
                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Leaders",True,(255,255,255))
                txtCenter = ((620),(370))
                self._screen.blit(TextSurf, txtCenter)

                #displays the score

                txt = pygame.font.Font('freesansbold.ttf',100)
                TextSurf=txt.render(str(self.score) + " points!",True,(255,255,255))
                txtCenter = ((300),(50))
                self._screen.blit(TextSurf, txtCenter)


                self.buttonClick(click,mousePos)

            #High Score screen
            if self.mode==4:

                self._screen.fill((255,255,255))
                self._screen.blit(self.back,(0,0))

                mousePos=pygame.mouse.get_pos()
                click= pygame.mouse.get_pressed()

                if mousePos[0]>450 and mousePos[0]<550 and mousePos[1]>350 and mousePos[1]<400:
                    pygame.draw.rect(self._screen,(128,128,128),(450,350,100,50))
                else:
                    pygame.draw.rect(self._screen,(0,0,0),(450,350,100,50))

                #BUTTON to Main Menu
                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render("Back",True,(255,255,255))
                txtCenter = ((475),(370))
                self._screen.blit(TextSurf, txtCenter)

                #calculates high score
                global highScoreList
                highScore=max(highScoreList)
                highScoreList=sorted(highScoreList)

                #Calculates if the user got a high score
                if highScoreList[-1]==highScore:
                    txt = pygame.font.Font('freesansbold.ttf',70)
                    TextSurf=txt.render("New High Score: " + str(highScore),True,(255,255,255))
                    txtCenter = ((100),(50))
                    self._screen.blit(TextSurf, txtCenter)

                else:    
                    txt = pygame.font.Font('freesansbold.ttf',70)
                    TextSurf=txt.render("High Score: " + str(highScore),True,(255,255,255))
                    txtCenter = ((100),(50))
                    self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',30)
                TextSurf=txt.render("1: " + str(highScore) + " points",True,(255,255,255))
                txtCenter = ((250),(150))
                self._screen.blit(TextSurf, txtCenter)

                if len(highScoreList)>=2:
                    txt = pygame.font.Font('freesansbold.ttf',30)
                    TextSurf=txt.render("2: " + str(highScoreList[-2]) + " points",True,(255,255,255))
                    txtCenter = ((250),(180))
                    self._screen.blit(TextSurf, txtCenter)

                else:
                    txt = pygame.font.Font('freesansbold.ttf',30)
                    TextSurf=txt.render("2: ",True,(255,255,255))
                    txtCenter = ((250),(180))
                    self._screen.blit(TextSurf, txtCenter)

                if len(highScoreList)>=3:
                    txt = pygame.font.Font('freesansbold.ttf',30)
                    TextSurf=txt.render("3: " + str(highScoreList[-3]) + " points",True,(255,255,255))
                    txtCenter = ((250),(210))
                    self._screen.blit(TextSurf, txtCenter)

                else:
                    txt = pygame.font.Font('freesansbold.ttf',30)
                    TextSurf=txt.render("3: ",True,(255,255,255))
                    txtCenter = ((250),(210))
                    self._screen.blit(TextSurf, txtCenter)

                self.buttonClick(click,mousePos)

            pygame.display.update()
            self._clock.tick(60)

    
    def extraLife(self):

       
        if len(self.hoopList)%3==0 and len(self.hoopList)!=0 :    
            self.ada = pygame.transform.scale(self.ada, (self.adaWidth, self.adaHeight))
            self._screen.blit(self.ada,(self.adaX, self.adaY))
            self.adaY-=7

            
            # if Ada is still on the screen award an extra life if you clap
            #the third part of the and statements makes sure the player can at max get one life per 4 rounds
            if self.adaY>-45 and self.clap==True and ((abs(self.gameCounter-self.prevCounter)>200) or self.prevCounter==0) :
                #incorpotrates sound
                pygame.mixer.Sound.play(self.cash)
                pygame.mixer.music.stop()
                self.lives+=1
                self.prevCounter=self.gameCounter

        #make Ada's position at the bottom of the screen 
        else: 
            self.adaY=self.screen_height
            self.adaX=random.randint(0,600)                       


    def createObstacles(self):
        #creates the case for when the user wants to pause the game 
        if abs(self.cur_right_hand_height)<.1 and abs(self.cur_left_hand_height)<.1 and abs(self.cur_right_hand_width)<.1 and abs(self.cur_left_hand_width)<.1:
            pass

        else:       

            #draws the obstacle until it reaches the optimasl size
            if self.obstacleRad< self.screen_height//4:
                pygame.draw.circle(self._screen,(0,0,150),(self.obsX,self.obsY),self.obstacleRad)
                #increases radius
                self.obstacleRad+=self.level
                self.liveBool=True

            #randomizes newe obstacle position
            elif self.radius>= self.screen_height//2:
                self.obsX=random.randint(self.margin,self.screen_width-self.margin)
                self.obstacleRad=1
                self.obsY= self.screen_height//2
                self.liveBool=False

            #if an obstacle is not on board, no lives can be lost
            else:
                self.liveBool=False

    #if an obstacle is hit
    def hitObstacle(self):
        if  self.obstacleRad >= self.screen_height//4 and self.liveBool:
            #checks to see if the x boundary of the obstacle is hitting the plane
            if self.obsX+self.obstacleRad> 340 and self.obsX-self.obstacleRad<490:
                #checks to see if the y boundary of the obstacle is hitting the plane
                if self.obsY+self.obstacleRad> 200 and self.obsY-self.obstacleRad<300:
                    #you lose a life if you hit the obstacle
                    self.lives-=1

                    #incorpotrates sound
                    pygame.mixer.Sound.play(self.losingSound)
                    pygame.mixer.music.stop()

                    #creates text for hitting obstacle
                    txt = pygame.font.Font('freesansbold.ttf',100)
                    TextSurf=txt.render(("HIT!"),True,(255,0,0))
                    txtCenter = ((350),(50))
                    self._screen.blit(TextSurf, txtCenter)

                    #checks if out of lives
                    if self.lives==0:
                    #calls helper function
                        highScoreList.append(self.score)
                        self.gameOver()


    def createHoops(self):
        #cretaes the case for when the user wants to pause the game 
        if abs(self.cur_right_hand_height)<.1 and abs(self.cur_left_hand_height)<.1 and abs(self.cur_right_hand_width)<.1 and abs(self.cur_left_hand_width)<.1:
            pass

        else: 
            #draws the obstacle until it reaches the optimasl size
            if self.radius< self.screen_height//2:
                pygame.draw.circle(self._screen,(0,0,0),(self.hoopX,self.hoopY),self.radius)
                #increases radius
                self.radius+=self.level
            #randomizes newe obstacle position
            else:
                self.hoopX=random.randint(self.margin,self.screen_width-self.margin)
                self.radius=1
                self.hoopY= self.screen_height//2
                self.hoopList.append(self.level)


    def handMovement(self):
        #cretaes the case for when the user wants to pause the game 
        if abs(self.cur_right_hand_height)<.1 and abs(self.cur_left_hand_height)<.1 and abs(self.cur_right_hand_width)<.1 and abs(self.cur_left_hand_width)<.1:
            pass

        else:
            if self.lean=="left":
                    #for the hoop
                    self.hoopX+=self.tilt*2
                    #for the obstacle
                    self.obsX+=self.tilt*2
                    
            if self.lean=="right":
                    #for the hoop
                    self.hoopX-=self.tilt*2
                    #for the obstacle
                    self.obsX-=self.tilt*2
               


   #when the game is over
    def gameOver(self):
        self.mode=3
        self.gameIntro()        

    def scoring(self):
        #cheks to see if the hoop is to the full size
        if self.radius >=self.screen_height//2:
        
             #checks to make sure the hoop is centered
            if self.hoopX<self.screen_width//2+ self.scoringMargin and self.hoopX>self.screen_width//2 - self.scoringMargin and self.hoopY<self.screen_height//2+ self.scoringMargin and self.hoopY>self.screen_height//2 - self.scoringMargin:
                self.score+=1
                self.completedList.append(self.level)
                self.missed=False

            #when the user doesnt go through the hoop
            else:
                self.lives-=1
                #incorpotrates sound
                pygame.mixer.Sound.play(self.losingSound)
                pygame.mixer.music.stop()

                txt = pygame.font.Font('freesansbold.ttf',100)
                TextSurf=txt.render(("MISSED"),True,(255,0,0))
                txtCenter = ((250),(50))
                self._screen.blit(TextSurf, txtCenter)
                self.missed=True
                #checks if out of lives
                if self.lives==0:
                    #calls helper function
                    highScoreList.append(self.score)
                    
                    self.gameOver()
                    

    def levels(self):
        #increments the level every 7 successful trials
        #increases speed
        if len(self.hoopList)%5==0 and len(self.hoopList)!=0:
            if self.radius>=self.screen_height//2:  
                #incorpotrates sound
                pygame.mixer.Sound.play(self.levelUp)
                pygame.mixer.music.stop()
                self.level+=1

   
    #This code structure is from the 2016 Microsoft Kinect Workshop
    def run(self): 
        # -------- Main Program Loop ----------- 
        while not self._done:
            self._screen.fill((0,0,0))
            self._screen.blit(self.image,(0,0))
            
            # --- Main event loop 
            for event in pygame.event.get(): # User did something 
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT: # If user clicked close 
                    self._done = True # Flag that we are done so we exit this loop 
                self.redrawAll(self._screen)
           
            # We have a body frame, so can get skeletons 
            if self._kinect.has_new_body_frame():  
                self._bodies = self._kinect.get_last_body_frame() 
                if self._bodies is not None:  
                    for i in range(0, self._kinect.max_body_count): 
                        body = self._bodies.bodies[i] 
                        if not body.is_tracked:  
                            continue  
                        joints = body.joints


                        # save the hand positions  

                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked: 
                            self.cur_right_hand_height = joints[PyKinectV2.JointType_HandRight].Position.y 
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked: 
                            self.cur_left_hand_height = joints[PyKinectV2.JointType_HandLeft].Position.y 

                       
                        #saves x positionsc
                        if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked: 
                            self.cur_right_hand_width = joints[PyKinectV2.JointType_HandRight].Position.x 
                        if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked: 
                            self.cur_left_hand_width = joints[PyKinectV2.JointType_HandLeft].Position.x 

                          
                        # calculate the tilt which controls to degree to which how fast obstacles move
                        self.tilt = int(abs(self.cur_left_hand_height- self.cur_right_hand_height)*10)
                        #checks which way the tilt is leaning
                        if self.cur_right_hand_height> self.cur_left_hand_height:
                            self.lean="left" 
                        else:
                            self.lean="right" 

                        #calculates how far apart hand positions are
                        if abs(abs(self.cur_left_hand_width)-abs(self.cur_right_hand_width))<.06:
                            self.clap=True
                        else:
                            self.clap=False

                        #code the wing flap
                        #Code derived from CMU 2016 Microsoft Kinect Workshop
                        # calculate wing flap

                        self.flap = (self.prev_left_hand_height - self.cur_left_hand_height) + (self.prev_right_hand_height - self.cur_right_hand_height)
                        if math.isnan(self.flap) or self.flap < 0:
                            self.flap = 0

                        self.prev_left_hand_height = self.cur_left_hand_height 
                        self.prev_right_hand_height = self.cur_right_hand_height
                        self.prev_left_hand_width = self.cur_left_hand_width
                        self.prev_right_hand_width = self.cur_right_hand_width

            # --- Game logic 

            
            #creates hoops
            self.createObstacles()
            #creates obstacles
            self.createHoops()
            #calculates hand positions
            self.handMovement()
            
            #if obsacles were hit
            self.hitObstacle()
            #Calculates scoring count
            self.scoring()
            self.levels()
               
            #cretaes the case for when the user wants to pause the game 
            if abs(self.cur_right_hand_height)<.1 and abs(self.cur_left_hand_height)<.1 and abs(self.cur_right_hand_width)<.1 and abs(self.cur_left_hand_width)<.1:
                #writesd Paused
                txt = pygame.font.Font('freesansbold.ttf',100)
                TextSurf=txt.render(("Paused"),True,(0,0,0))
                txtCenter = ((300),(45))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render(("To hold this pause, step out of the frame or keep your hands together at hip height"),True,(0,0,0))
                txtCenter = ((100),(140))
                self._screen.blit(TextSurf, txtCenter)

                txt = pygame.font.Font('freesansbold.ttf',20)
                TextSurf=txt.render(("To exit this pause, bring your hands into a plane position"),True,(0,0,0))
                txtCenter = ((100),(170))
                self._screen.blit(TextSurf, txtCenter)
                
            else:
                
                self.hoopY-=self.gravity
                self.hoopY+=int(self.flap*100)

            #ExtraLife
            self.extraLife()
            #keeps track of time
            self.gameCounter+=1

            #draw the score on the screen
            txt = pygame.font.Font('freesansbold.ttf',60)
            TextSurf=txt.render(str(self.score),True,(0,0,0))
            txtCenter = ((25),(25))
            self._screen.blit(TextSurf, txtCenter)

             #draw the lives on he screen
            txt = pygame.font.Font('freesansbold.ttf',30)
            TextSurf=txt.render(str(self.lives) + "lives",True,(0,0,0))
            txtCenter = ((800),(45))
            self._screen.blit(TextSurf, txtCenter)

            
            self._screen.blit(self.plane,(340,200))
                

            surface_to_draw = None 
            pygame.display.update() 

            # --- Limit to 60 frames per second 
            self._clock.tick(60) 
                
            # Close our Kinect sensor, close the window and quit. 
        self._kinect.close() 
        pygame.quit() 
        
game = GameRuntime(); 
game.gameIntro();


