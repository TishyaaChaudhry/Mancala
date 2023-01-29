
from board import *

import copy,math

from ai import convertBoardToDictionary, pitsForPlayer, gameOver, eval


def possibleMoves(app,state,player):
    moves = set()
    if player ==1:
        for i in range(1,app.pitCount//2+1):
            if state[i]!=0:
                moves.add(i)
    else:
        for i in range(app.pitCount//2,app.pitCount+1):
            if state[i]!=0:
                moves.add(i)
    return moves
    


def applyMove(app,s,move,player):
    state = copy.copy(s)
    print(state)
    sequence = (app.pitList[move-1].sequence+1)%(app.pitCount+2)
    print("state[move]",state[move])
    while state[move]!=0:
        location  = app.allLocations[sequence]
        print("location",location)
        print(state)
        print(type(location))
        if isinstance(location,Pit):
            state[location.number]+=1
            print("STATE", state)
            print("added to", location.number)
            state[move]-=1
            lastPlaceAdded= location.number
       
        print("sequence",sequence)
        sequence = (sequence+1)%(app.pitCount+2)

    # account for bonus seeds
    while(isinstance(lastPlaceAdded, int) and state[lastPlaceAdded] in (2,4,6)):
        print("CURR PLAYER PITS",app.currentPlayer.pits)
        print("got bonus seeds")
        state["M"+str(player)] = state[lastPlaceAdded]
        state[lastPlaceAdded] =0
        lastPlaceAdded-=1
    print("returning", state)
    return state
            


def max_value(app,state,player,depth):
    print(depth)
    if gameOver(app,state) or depth ==0:
        return eval(state,player), None
    maxV = -math.inf
    movetomake = None
    for move in possibleMoves(app,state,player):
        print(state, "apply", move, player)
        newState =  applyMove(app,state,move,player)
            
        result = min_value(app,newState, abs(player-1),depth-1)[0]

        if result>maxV:
            movetomake = move
            maxV = result
    print("returning", maxV,movetomake)
    return maxV,movetomake

def min_value(app,state,player, depth): 
    #print(depth)
    if gameOver(app,state) or depth ==0: 
        return eval(state,player), None
    minV =math.inf
    movetomake = "Nothing"
    for move in possibleMoves(app,state,player):
        print(state, "apply", move,player)
        newState =  applyMove(app,state,move,player)      
        result = max_value(app,newState, abs(player-1),depth-1)[0]
        if minV>result:
                movetomake = move
                minV= result
    print("returning", minV,movetomake)
    return minV,movetomake



def minimax(app,player,depth):
    if player==2:
        return max_value(app,convertBoardToDictionary(app),player, depth)[1]
    else:
        return min_value(app,convertBoardToDictionary(app),player, depth)[1]

    
    


# lets test the applyMove function

def testApplyMove(app):
    
    state ={1: 7, 2: 2, 3: 1, 4: 6, 5: 6, 6: 0, 7: 0, 8: 4, 9: 4, 10: 6, 11: 6, 12: 6, 'M1': 0, 'M2': 0}  
    #print(applyMove(app,state,1,1))
  


    


    


