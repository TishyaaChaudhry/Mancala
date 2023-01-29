
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
    while state[move]!=0:
        location  = app.allLocations[sequence]
        if isinstance(location,Pit):
            state[location.number]+=1
            state[move]-=1
            lastPlaceAdded= location.number
        elif isinstance(location,Mancala):
            if location.number == player:
                state["M"+str(location.number)]+=1
                state[move]-=1
                lastPlaceAdded= "M"+str(location.number)
        sequence = (sequence+1)%(app.pitCount+2)

    if isinstance(lastPlaceAdded, int):
        oppositeSide= app.pitCount+1 - lastPlaceAdded
        if state[lastPlaceAdded]==1 and state[oppositeSide]!=0 and lastPlaceAdded in pitsForPlayer(app,player):
            state["M"+str(player)] = state[oppositeSide]+ state[lastPlaceAdded]
            state[oppositeSide] = 0
            state[lastPlaceAdded] =0
    if not isinstance(lastPlaceAdded,str) and state[lastPlaceAdded] not in (0,1):
        return applyMove(app,state,lastPlaceAdded,player)
    else:
        if isinstance(lastPlaceAdded,str):
            return state, True
        else:
            return state, False
            


def max_value(app,state,player,depth):
    print(depth)
    if gameOver(app,state) or depth ==0:
        return eval(state,player), None
    maxV = -math.inf
    movetomake = None
    for move in possibleMoves(app,state,player):
        #print(state, "apply", move, player)
        newState, extraMove =  applyMove(app,state,move,player)
        if extraMove==True:
            result = max_value(app,newState,player,depth-1)[0]
            
        result = min_value(app,newState, abs(player-1),depth-1)[0]

        if result>maxV:
            movetomake = move
            maxV = result
    #print("returning", maxV,movetomake)
    return maxV,movetomake

def min_value(app,state,player, depth): 
    #print(depth)
    if gameOver(app,state) or depth ==0: 
        return eval(state,player), None
    minV =math.inf
    movetomake = "Nothing"
    for move in possibleMoves(app,state,player):
        #print(state, "apply", move,player)
        newState, extraMove =  applyMove(app,state,move,player)
        if extraMove==True:
            result = min_value(app,newState,player,depth-1)[0]
            
        result = max_value(app,newState, abs(player-1),depth-1)[0]
        if minV>result:
                movetomake = move
                minV= result
    #print("returning", minV,movetomake)
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
  


    


    


