
class Pit(object):
    def __init__(self,cx,cy,seedCount,number,sequence):
        self.number = number
        self.xPos = cx
        self.yPos = cy
        self.seedCount = seedCount
        self.color = "white"
        self.sequence = sequence
        
        
    def emptyPit(self):
        self.seedCount = 0
        
    def removeSeed(self):
        self.seedCount-=1
    
    def addSeed(self):
        self.seedCount+=1

    def isEmpty(self):
        if self.seedCount ==0:
            return True 
        else:
            return False
    def __repr__(self):
        return "Pit"+str(self.number)+" Sequence"+str(self.sequence)
class Mancala(object):

    def __init__(self,x0,y0,x1,y1,seedCount,number,sequence):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.seedCount = seedCount 
        self.number = number
        self.sequence = sequence
        

    def getSeedCount(self):
        return self.seedCount
    
    def addSeed(self):
        self.seedCount+=1

    def addSeed(self,numOfSeeds):
        self.seedCount+=numOfSeeds

    def __repr__(self):
        return "Mancala"+str(self.number)+" Sequence"+str(self.sequence)

class Seed(object):

    def __init__(self,color, initialPit,xPos,yPos):
        self.color = color
        self.pit = initialPit # store reference of pit/mancala class here
        self.x = xPos
        self.y = yPos
        self.dy = 0
        self.dx = 0
        self.finalX = xPos
        self.finalY = yPos

    def changePosition(self, newPit):
        self.pit = newPit
    
    def __repr__(self):
        return self.color+"  Pit: "+str(self.pit)



class Player(object):

    def __init__(self,app,number,name):       
        self.name = name 
        if number==1:
            print("Player 1 Pits",)
            self.pits = [i for i in range(app.pitCount//2+1,app.pitCount+1)]
            print("Player 1 Pits",self.pits)
        else:
            self.pits = [i for i in range(1,app.pitCount//2+1)]
            print("Player 2 Pits",self.pits)
        self.number = number




def convertBoardToDictionary(app):
    board = dict()
    for pit in app.pitList:
        board[pit.number] = pit.seedCount
    board["M1"] = app.mancalaList[0].seedCount
    board["M2"] = app.mancalaList[0].seedCount
    
        

    

    









