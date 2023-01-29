 
from board import *



def isLegalPit(app,pit):
    if app.isGameOver == True:
        return False
    # is this pit legal for the current player
    if (pit.number in app.currentPlayer.pits):
        return True 
    else:
        return False

def getExtraTurn(app,lastPlaceAdded):
    if isinstance(lastPlaceAdded,Mancala):
        return True
    else:
        return False


def getBonusSeeds(app,lastPlaceAdded):
    if (isinstance(lastPlaceAdded,Pit)and lastPlaceAdded.seedCount ==1 and 
        lastPlaceAdded.number in app.currentPlayer.pits):
        oppositeSidePitNumber = app.pitCount+1 - lastPlaceAdded.number
        for pit in app.pitList:
            if pit.number == oppositeSidePitNumber and pit.seedCount>0:
                return pit



'''
This function handles the situation when the last seed lands in an empty 
pit on the current players side
'''
def updateBonusSeeds(app,pit,oppositePit):
    seedCount = pit.seedCount
    pit.emptyPit()
    seedCount+= oppositePit.seedCount 
    oppositePit.emptyPit

    for mancala in app.mancalaList:
        if mancala.number == app.currentPlayerNumber:
            currentMancala = mancala
            mancala.seedCount+=seedCount

    for seed in app.seedList:
        if seed.pit == pit.number or seed.pit == oppositePit.number:
            seed.pit = currentMancala


def isGameOver(app):
    # Case1: Player 1 runs out of seeds
    sum = 0
    for pit in app.pitList:
        if pit.number in app.playerList[0].pits:
            sum = sum+ pit.seedCount
    print("Sum = ", sum)
    if sum==0:
        print("returning True")
        return True
    else:
        sum =0
        for pit in app.pitList:
            if pit.number in app.playerList[1].pits:
                sum = sum+ pit.seedCount
        print("Sum = ", sum)
        if sum==0:  
            #print("returning True")
            return True
    #print("returning False")
    return False

    



                
            

    
