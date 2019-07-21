import random, time
import numpy as np
import json
from flask import Flask, escape, request,render_template
from tools import encode_state,decode_state, getAllPossibleNextAction, try_action, win_or_loss
import train as T

action = random.choice([ 0, 2, 7, 9 ])
statePlayerB = 0
statePlayerA = 0
done         = False
world = T.oTrain()
world.read_train('hard.txt')

def handle(action, statePlayerB, statePlayerA, world):
   statePlayerB    = int(statePlayerB)
   statePlayerA    = int(statePlayerA)
   state_playerA, IA_win, done = world.Play1(action, statePlayerB,  statePlayerA)
   state_win = [0,0]
   if done == True:
      state_playerB = 0  ## player 1 win
      IA_win[lvl][1]   += 1 
      state_win   = [state_playerA,1] 
   else:   
      state_playerB, done  = world.Play2(2, state_playerA, statePlayerB)
      if done == True:  
         IA_win[0][2]   += 1    ## player 2 win  
         state_playerA = 0 
         state_win   = [state_playerB,2] 
      elif state_playerB == 0 :                   
         IA_win[0][0]   += 1    ##empate
         state_win   = [state_playerA,0] 
         done        = True   
   return done, IA_win, state_playerA, state_playerB      

while not done:   
    done, IA_win, state_playerA, state_playerB = handle(action, statePlayerB, statePlayerA, world)         

print(done, IA_win, state_playerA, state_playerB)    