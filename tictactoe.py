import random, time
import numpy as np
import json
from flask import Flask, escape, request,render_template
from tools import encode_state,decode_state, getAllPossibleNextAction, try_action, win_or_loss
import train as T

app = Flask(__name__, static_url_path='/static')

state_playerB= 0
state_playerA= 0
IA_win       = [[0,0,0],[0,0,0],[0,0,0]]  

world = T.oTrain()
world.read_train('easy.txt')

world1 = T.oTrain()
world1.read_train('medium.txt')

world2 = T.oTrain()
world2.read_train('hard.txt')
#world2.try_train(150000)

lvls = [world, world1, world2]

##
##
## WEB CLIENT
##
##
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save')
def save():
    lvls[0].save_train('easy.txt')
    lvls[1].save_train('medium.txt')
    lvls[2].save_train('hard.txt')
    return render_template('index.html') 

@app.route('/reload')
def reload():
    lvls[0].read_train('easy.txt')
    lvls[1].read_train('medium.txt')
    lvls[2].read_train('hard.txt')
    return render_template('index.html') 

@app.route('/train/<lvl>/<number>')
def train(lvl, number):
    lvl    = int(lvl)
    number = int(number)
    lvls[lvl].try_train(number)
    return render_template('index.html')  

@app.route('/clear/<lvl>')
def clean(lvl):
    lvl    = int(lvl)
    lvls[lvl].q_table = np.zeros([lvls[lvl].width, lvls[lvl].states])
    return render_template('index.html')   

@app.route('/update/<state>', methods=['POST','GET'])
def update(state):  
   state = int(state)
   row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
   ret = { "rows": {
               "row1": row1,"row2": row2,"row3": row3,"row4": row4,"row5": row5,"row6": row6,"row7": row7,"row8": row8,"row9": row9
         }, 
         "state_playerB":state_playerB,
         "state_playerA":state_playerA,
         "IA_win":IA_win,
         "done":False
   }
   return json.dumps(ret)

@app.route('/handle/<action>/<statePlayerB>/<statePlayerA>/<lvl>', methods=['POST','GET'])
def handle(action, statePlayerB, statePlayerA, lvl):
   state_playerB    = int(statePlayerB)
   state_playerA    = int(statePlayerA)
   lvl             = int(lvl)
   action          = int(action)
   done, draw      = False, False
   state_win       = [0,0]
   if action != 99 : #only play Player 2
      state_playerA, done, draw = lvls[lvl].Play1(action, state_playerB,  state_playerA)  
   else :
      state_playerA = 0

   if done == True:
      state_playerB   = 0    ## player 1 win
      IA_win[lvl][1]  += 1 
      state_win       = [state_playerA,1] 
   elif draw :
      IA_win[0][0]   += 1    ##empate
      state_win      = [state_playerA,0] 
      done           = True           
   else:   
      state_playerB, done, draw  = lvls[lvl].Play2(2, state_playerA, state_playerB)
      if done == True:  
         IA_win[0][2]   += 1    ## player 2 win  
         state_playerA  = 0 
         state_win      = [state_playerB,2] 
      elif draw :                   
         IA_win[0][0]   += 1    ##empate
         state_win      = [state_playerB,0] 
         done           = True     
    
   if done == True: 
      row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state_win[0])
   else:   
      row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state_playerB)

   ret = { "rows": {
               "row1": row1,
               "row2": row2,
               "row3": row3,
               "row4": row4,
               "row5": row5,
               "row6": row6,
               "row7": row7,
               "row8": row8,
               "row9": row9
         }, 
         "state_playerB":state_playerB,
         "state_playerA":state_playerA,
         "IA_win":IA_win,
         "done":done,
         "win":state_win,
         "Play1_current":lvls[lvl].q_table[state_playerA].tolist(),
         "Play2_current":lvls[lvl].q_table[state_playerB].tolist()
   }
   return json.dumps(ret)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9800)    

