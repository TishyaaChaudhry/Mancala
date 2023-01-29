from Legal import isLegalPit
from board import *
from cmu_112_graphics import *;
import math 
import random
from Mancala import getBoardRegion, getPitRegion, calculatePitLocation, drawPits,createSeeds,sizeChanged, findWinner, getSeedCoordinates, createMancalas, drawMancalas, drawPits, drawSeeds, moveBonusSeeds, calculateMancalaLocations, drawGameOver,findWinner
from aiBohnenspiel import minimax


#https://www.cs.cmu.edu/~112/notes/notes-data-and-operations.html
def almostEqual(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

def appStarted(app):
    app.pitCount = 12
    app.gameMessage = "Player1"
    app.initialSeedCount = 2
    app.margin = (app.height)*0.1
    app.pitList = []  # change to set if does not serve too many purposes
    # and write hash function for the object
    app.seedList=[]
    app.seedColorOptions =  ["SeaGreen1","orchid1","turquoise1","salmon", "pink", "yellow","orange"]
    app.isGameOver = False
    app.timerDelay = 1000//60
    app.mancalaList =  []
    app.playerList = [Player(app,1,"Player 1"),Player(app,2,"Player 2")]
    app.currentPlayer = app.playerList[0]
    app.startedMovement = False
    app.clickedPit = None
    createPits(app)
    createMancalas(app)
    createSeeds(app)
    # pitList and mancalaList are initialised
    app.allLocations = app.pitList+ app.mancalaList
    #print(app.allLocations)
    app.movingSeedQueue = []

'''
Unique
'''
def createPits(app):
    
    for i in range(1,app.pitCount+1):
        sequence = app.pitCount-i
        pit = Pit(0,0,app.initialSeedCount,i,sequence)
        calculatePitLocation(app,pit)
        app.pitList.append(pit)


def createMancalas(app):
    sequence = -1
    mancala1 = Mancala(0,0,0,0,0,1,sequence)
    calculateMancalaLocations(app,mancala1)
    mancala2 = Mancala(0,0,0,0,0,2,sequence)
    calculateMancalaLocations(app,mancala2)
    app.mancalaList = [mancala1,mancala2]

'''
Unique
'''
def mousePressed(app, event):
    for pit in app.pitList:
        if ((pit.xPos-event.x)**(2)+(pit.yPos-event.y)**(2))**(1/2)<= app.pitRadius:
            app.clickedPit = pit
            print(app.clickedPit.sequence)
            
    onClick(app)
    if isGameOver(app):
        # print appropriate message
        pass

    
def onClick(app):
    app.Message = "Player "+str(app.currentPlayer.number)
    if app.clickedPit == None or app.clickedPit.isEmpty():
        return None
    else:
        #print("Enter Else")
        if isLegalPit(app,app.clickedPit):
            
            position = app.clickedPit.sequence+1
            app.clickedPit.emptyPit()

            for seed in app.seedList:
                if seed.pit.number == app.clickedPit.number and isinstance(seed.pit,Pit):
                    
                    lastPlaceAdded = assignNewPitToSeed(app,seed,position)
                    print("last place added ",lastPlaceAdded.number)
                    seed.finalX,seed.finalY = getSeedCoordinates(app,seed.pit)
                    app.movingSeedQueue.append(seed)
                    position+=1
            if getBonusSeeds(app,lastPlaceAdded)!=[]:
                app.gameMessage = "Player " + str(app.currentPlayer.number) + " gets seeds"
                pitList = getBonusSeeds(app,lastPlaceAdded)
                for pit in pitList:
                    moveBonusSeeds(app,pit)
            
            if app.currentPlayer.number ==1:
                app.currentPlayer = app.playerList[1]
                minimaxResult = minimax(app,1, 2)
                for pit in app.pitList:
                    if pit.number == minimaxResult:
                        app.clickedPit = pit
                        print(app.clickedPit)
                        onClick(app)
                app.gameMessage = "Player2"
            else:
                app.currentPlayer = app.playerList[0]
                app.gameMessage = "Player1"
            # clicked pit becomes none in either case
                app.clickedPit = None
            






def moveRequiredSeed(app,seed):
    if seed.y==seed.finalY:
            seed.dy = 0
    if seed.x==seed.finalX:
            seed.dx = 0
    else:
        seed.dx = (seed.finalX- seed.x)/10
        seed.dy = (seed.finalY-seed.y)/10



def timerFired(app):
    if len(app.movingSeedQueue)!=0:
        seed = app.movingSeedQueue[0]
        if almostEqual(seed.y,seed.finalY):
            seed.dy = 0
        if almostEqual(seed.x,seed.finalX):
            seed.dx = 0
        elif app.startedMovement ==False:
            app.startedMovement = not app.startedMovement
            seed.dx = (seed.finalX- seed.x)/10
            seed.dy = (seed.finalY-seed.y)/10
        seed.x+=seed.dx
        seed.y+=seed.dy
        if seed.dx==0 and seed.dy ==0:
            app.movingSeedQueue.pop(0)
            app.startedMovement = False

def isGameOver(app):
    for pit in app.pitList:
        if not pit.isEmpty():
            return False
    return True

def getBonusSeeds(app,lastPlaceAdded):
    returnList = []
    if (lastPlaceAdded.seedCount in (3,2,4,6)):
        returnList = [lastPlaceAdded]
        pos = app.pitList.index(lastPlaceAdded)
        while app.pitList[pos].seedCount in (3,2,4,6):
            returnList.append(app.pitList[pos])
            pos=(pos+1)%app.pitCount
    return returnList

'''
Assigns a new pit to the seed and return the lastPlaceAdded
'''
def assignNewPitToSeed(app,seed,position):
    print("position ", position)
    for place in app.allLocations:
        if place.sequence == position%(app.pitCount):
            print("move seed from ",seed.pit.number,place.number)
            seed.pit = place
            place.seedCount+=1
            return place

def redrawAll(app,canvas):
    font = 'Arial 12 bold'
    canvas.create_text(app.width/2, app.margin/2,text=f'{app.gameMessage}',font=font)
    drawPits(app,canvas)
    drawMancalas(app,canvas)
    drawSeeds(app,canvas)
    if isGameOver(app):
        drawGameOver(app,canvas)
    
runApp(width=1200, height=450)

        
    
        
        
        

















