import random, time
import numpy as np
import json
from flask import Flask, escape, request,render_template
from tools import encode_state,decode_state, getAllPossibleNextAction, try_action, win_or_loss

import train as T

app = Flask(__name__, static_url_path='/static')
                     
world = T.oTrain()
world.try_train(20000)
world.play()

##
##
## WEB CLIENT
##
##
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train/<number>')
def train(number):
    number = int(number)
    world.try_train(number)
    return render_template('index.html')  

@app.route('/clear')
def clean():
    world.q_table = np.zeros([world.width, world.states])
    return render_template('index.html')   

@app.route('/update/<state>', methods=['POST','GET'])
def update(state):  
   state = int(state)
   row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
   ret = { "rows": {
               "row1": row1,"row2": row2,"row3": row3,"row4": row4,"row5": row5,"row6": row6,"row7": row7,"row8": row8,"row9": row9
         }, 
         "state_playerB":T.state_playerB,
         "state_playerA":T.state_playerA,
         "IA_win":T.IA_win,
         "done":False
   }
   return json.dumps(ret)

@app.route('/handle/<action>/<statePlayerB>/<statePlayerA>', methods=['POST','GET'])
def handle(action, statePlayerB, statePlayerA):
   state_playerA, IA_win, done = world.Play1(action, statePlayerB,  statePlayerA)
   state_win = [0,0]
   if done == True:
      state_playerB = 0  ## player 1 win
      IA_win[1]   += 1 
      state_win   = [state_playerA,1] 
   else:   
      state_playerB, done  = world.Play2(2, state_playerA, statePlayerB)
      if done == True:  
         IA_win[2]   += 1    ## player 2 win  
         state_playerA = 0 
         state_win   = [state_playerB,2] 
      elif state_playerB == 0 :                   
         IA_win[0]   += 1    ##empate
         state_win   = [state_playerA,0] 
         done        = True     
    
   if done == True: 
      row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state_win[0])
   else:   
      row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state_playerB)
   ret = { "rows": {
               "row1": row1,"re1":world.q_table[state_playerA][0],"pe1":world.q_table[state_playerB][0],
               "row2": row2,"re2":world.q_table[state_playerA][1],"pe2":world.q_table[state_playerB][1],
               "row3": row3,"re3":world.q_table[state_playerA][2],"pe3":world.q_table[state_playerB][2],
               "row4": row4,"re4":world.q_table[state_playerA][3],"pe4":world.q_table[state_playerB][3],
               "row5": row5,"re5":world.q_table[state_playerA][4],"pe5":world.q_table[state_playerB][4],
               "row6": row6,"re6":world.q_table[state_playerA][5],"pe6":world.q_table[state_playerB][5],
               "row7": row7,"re7":world.q_table[state_playerA][6],"pe7":world.q_table[state_playerB][6],
               "row8": row8,"re8":world.q_table[state_playerA][7],"pe8":world.q_table[state_playerB][7],
               "row9": row9,"re9":world.q_table[state_playerA][8],"pe9":world.q_table[state_playerB][8]
         }, 
         "state_playerB":state_playerB,
         "state_playerA":state_playerA,
         "IA_win":IA_win,
         "done":done,
         "win":state_win[1]
   }
   return json.dumps(ret)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9800)    

