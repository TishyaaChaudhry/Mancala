from Legal import  getBonusSeeds, getExtraTurn, isGameOver, isLegalPit
from board import *
from cmu_112_graphics import *;
import math 
import random
from Mancala import getBoardRegion, calculatePitLocation, createPits, createSeeds, drawPits,drawSeeds, getSeedCoordinates, doOnGameOver
from aiCongklak import minimax

def appStarted(app):
    app.pitCount = 14
    app.gameMessage = "Player1"
    app.initialSeedCount = 3
    app.margin = (app.height)*0.1
    app.pitList = []  # change to set if does not serve too many purposes
    # and write hash function for the object
    app.seedList=[]
    app.seedColorOptions =  ["SeaGreen1","orchid1","turquoise1","salmon", "pink", "yellow","orange"]
    app.isGameOver = False
   
    app.mancalaList =  []
    app.playerList = [Player(app,1,"Player 1"),Player(app,2,"Player 2")]
    app.currentPlayer = app.playerList[0]
    app.startedMovement = False
    app.clickedPit = None
    createPits(app)
    createMancalas(app)
    createSeeds(app)
    # pitList and mancalaList are initialised
    app.allLocations = [app.mancalaList[1]]+app.pitList[:app.pitCount//2]+[app.mancalaList[0]]+app.pitList[app.pitCount//2:]

    app.allLocations = app.allLocations[::-1]
    
    #print(app.allLocations)
    app.movingSeedQueue = []

def createMancalas(app):

    sequence = app.pitCount//2
    mancala1 = Mancala(0,0,0,0,0,1,7)
    calculateMancalaLocations(app,mancala1)
    sequence = app.pitCount+1
    mancala2 = Mancala(0,0,0,0,0,2,15)
    calculateMancalaLocations(app,mancala2)
    app.mancalaList = [mancala1,mancala2]
    

def getPitRegion(app):
        pitWidth = app.width - 4*app.margin
        pitHeight = app.height - 2*app.margin
        app.pitRadius = pitWidth/(25)
        app.seedRadius = app.pitRadius/10
        xb0,yb0,xb1,yb1 = getBoardRegion(app)
        x0 = app.margin+0.2*pitWidth
        y0 = app.margin*2
        x1 = xb1-0.2*pitWidth
        y1 = yb1-app.margin*2
        return x0,y0,x1,y1


'''
initializes the mancala objects and stores them in 
an app variable
'''
def calculateMancalaLocations(app,mancala):
    xb0,yb0,xb1,yb1 = getBoardRegion(app)
    xp0,yp0,xp1,yp1 = getPitRegion(app)
    if mancala.number ==2:
        
        mancala.x0 = xb0
        mancala.y0 = yp0
        mancala.x1 =xp0
        mancala.y1 = yp1
    if mancala.number ==1:
        
        mancala.x0 = xp1
        mancala.y0 = yp0
        mancala.x1 =xb1
        mancala.y1 = yp1
   
def createMancalas(app):

    sequence = app.pitCount//2
    mancala1 = Mancala(0,0,0,0,0,1,sequence)
    calculateMancalaLocations(app,mancala1)
    sequence = app.pitCount+1
    mancala2 = Mancala(0,0,0,0,0,2,sequence)
    calculateMancalaLocations(app,mancala2)
    app.mancalaList = [mancala1,mancala2]
    
def drawMancalas(app,canvas):
    for m in app.mancalaList:
        canvas.create_rectangle(m.x0,m.y0,m.x1,m.y1)

def mousePressed(app, event):
    for pit in app.pitList:
        if ((pit.xPos-event.x)**(2)+(pit.yPos-event.y)**(2))**(1/2)<= app.pitRadius and isLegalPit(app,pit):
            app.clickedPit = pit
            #print("Sequence        ",app.clickedPit.sequence)
    # testing code
    #if  app.mancalaList[0].x0<=event.x<=app.mancalaList[0].x1:
        #print("@@@@",app.mancalaList[0].sequence)
    #if app.mancalaList[1].x0<=event.x<=app.mancalaList[1].x1:
        #print("@@@@",app.mancalaList[1].sequence)
            onClick(app, False)
    
    #if isGameOver(app):
        #doOnGameOver(app)



'''
Assigns a new pit to the seed and return the lastPlaceAdded
'''
def assignNewPitToSeed(app,seed,position):
        print("assigning to ", position%(16))
        place = app.allLocations[position%(16)]
        
        print("move seed from ",seed.pit,place)
        seed.pit = place
        place.seedCount+=1
        return place


def onClick(app, redistribute):

    app.Message = "Player "+str(app.currentPlayer.number)
    if app.clickedPit == None or app.clickedPit.isEmpty():
        return None
    else:
        #print("Enter Else")
        print(isLegalPit(app,app.clickedPit), redistribute)
        if isLegalPit(app,app.clickedPit) or redistribute:
            
            position = app.clickedPit.sequence+1
            #print("Start with ", position)
            app.clickedPit.emptyPit()

            for seed in app.seedList:
                #print("Pos",position)
                if seed.pit.number == app.clickedPit.number and isinstance(seed.pit,Pit):
                    #print("SEED",position)
                    if position%(app.pitCount+2) == app.pitCount//2  and app.currentPlayer.number==2:
                        #print("Came Here")
                        position+=1
                    elif position%(app.pitCount+2) == app.pitCount+1 and app.currentPlayer.number==1:
                        #print("Came Here")
                        position+=1
                    #print("assignNewPitToSeed(app,seed", position, ")")
                    lastPlaceAdded = assignNewPitToSeed(app,seed,position)
                    print(lastPlaceAdded)
                    seed.finalX,seed.finalY = getSeedCoordinates(app,seed.pit)
                    #print("**********************",seed)
                    app.movingSeedQueue.append(seed)
                    position+=1
            if getBonusSeeds(app,lastPlaceAdded)!=None:
                app.gameMessage = "Player " + str(app.currentPlayer.number) + " gets bonus seeds"
                #print("added to empty place ")
                oponenetsPit = getBonusSeeds(app,lastPlaceAdded)
                moveBonusSeeds(app,oponenetsPit)
                moveBonusSeeds(app,lastPlaceAdded)
            if getExtraTurn(app,lastPlaceAdded):
                app.gameMessage = "Player " + str(app.currentPlayer.number) + " gets extra turn"
            else:
                if lastPlaceAdded.seedCount not in (0,1) and not isinstance(lastPlaceAdded,Mancala) and not lastPlaceAdded.seedCount==0:
                    
                    app.clickedPit = lastPlaceAdded
                    print("new clicked pit", lastPlaceAdded)
                  
                else:
                    if app.currentPlayer.number ==1:
                        app.currentPlayer = app.playerList[1]
                        app.gameMessage = "Player2"
                        print("minimax",minimax(app,1, 2))
                    else:
                        app.currentPlayer = app.playerList[0]
                        app.gameMessage = "Player1"
                    # clicked pit becomes none in either case
                    app.clickedPit = None
            



def findWinner(app):
    if app.mancalaList[0].seedCount > app.mancalaList[1].seedCount:
        return app.playerList[0]
    else:
        return app.playerList[1]
    
    


def moveBonusSeeds(app,oponenetsPit):
    for seed in app.seedList:
        if seed.pit.number ==oponenetsPit.number and isinstance(seed.pit,Pit):
            if app.currentPlayer.number ==1:
                seed.pit.emptyPit()
                seed.pit = app.mancalaList[0]
                app.mancalaList[0].seedCount+=1
                seed.finalX,seed.finalY = getSeedCoordinates(app,seed.pit)
                app.movingSeedQueue.append(seed)
            else:
                seed.pit.emptyPit()
                seed.pit = app.mancalaList[1]
                app.mancalaList[1].seedCount+=1
                seed.finalX,seed.finalY = getSeedCoordinates(app,seed.pit)
                app.movingSeedQueue.append(seed)
    #print("***Seed Counts",app.mancalaList[0].seedCount, app.mancalaList[1].seedCount)


def moveRequiredSeed(app,seed):
    if seed.y==seed.finalY:
            seed.dy = 0
    if seed.x==seed.finalX:
            seed.dx = 0
    else:
        seed.dx = (seed.finalX- seed.x)/2
        seed.dy = (seed.finalY-seed.y)/2
#https://www.cs.cmu.edu/~112/notes/notes-data-and-operations.html
def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

def timerFired(app):
    if len(app.movingSeedQueue)!=0:
        seed = app.movingSeedQueue[0]
        if almostEqual(seed.y,seed.finalY):
            seed.dy = 0
        if almostEqual(seed.x,seed.finalX):
            seed.dx = 0
        elif app.startedMovement ==False:
            app.startedMovement = not app.startedMovement
            seed.dx = (seed.finalX- seed.x)/2
            seed.dy = (seed.finalY-seed.y)/2
        seed.x+=seed.dx
        seed.y+=seed.dy
        if seed.dx==0 and seed.dy ==0:
            app.movingSeedQueue.pop(0)
            app.startedMovement = False
        #print(app.movingSeedQueue[0:4])
    else:
        if app.clickedPit!= None: #buggy
            onClick(app, True)

def sizeChanged(app):
    app.pitRadius = (app.height-(2*app.margin))/(5)
    for pit in app.pitList:
        calculatePitLocation(app,pit)
    for m in app.mancalaList:
        calculateMancalaLocations(app,m)
    for seed in app.seedList:
        a,b= getSeedCoordinates(app,seed.pit)
        seed.finalX = a
        seed.finalY = b
        seed.x = a
        seed.y = b
        
def redrawAll(app,canvas):
    font = 'Arial 12 bold'
    canvas.create_text(app.width/2, app.margin/2,text=f'{app.gameMessage}',font=font)
    drawPits(app,canvas)
    drawMancalas(app,canvas)
    drawSeeds(app,canvas)
    
runApp(width=1200, height=450)

        
    
        
        
        

















