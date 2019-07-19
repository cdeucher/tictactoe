import random, time
import numpy as np
import json
from flask import Flask, escape, request,render_template
from tools import encode_state,decode_state

app = Flask(__name__)

class World_base:
      def __init__(self): 
         self.width = 500000 
         self.states= 9
         self.q_table = np.zeros([self.width, self.states])
         self.current = 0
         self.action  = 0
         self.oldPlayer2 = 0

      def win_or_loss(self, state, player, base_reward): 
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
         if row1 == player and row2 == player and row3 == player:
            return base_reward[player][player], True
         if row4 == player and row5 == player and row6 == player:
            return base_reward[player][player], True
         if row7 == player and row8 == player and row9 == player:
            return base_reward[player][player], True

         if row1 == player and row4 == player and row7 == player:
            return base_reward[player][player], True
         if row2 == player and row5 == player and row8 == player:
            return base_reward[player][player], True
         if row3 == player and row6 == player and row9 == player:
            return base_reward[player][player], True                                    

         if row1 == player and row5 == player and row9 == player:
            return base_reward[player][player], True
         if row7 == player and row5 == player and row3 == player:
            return base_reward[player][player], True   

         return base_reward[0][0], False
      #end win_or_loss   

      def try_action(self, action, player, state):
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state) 
         if action == 0 :
            return encode_state( player,row2,row3,row4,row5,row6,row7,row8,row9 ) 
         elif action == 1 :   
            return encode_state( row1,player,row3,row4,row5,row6,row7,row8,row9 ) 
         elif action == 2 :   
            return encode_state( row1,row2,player,row4,row5,row6,row7,row8,row9 )  
         elif action == 3 :   
            return encode_state( row1,row2,row3,player,row5,row6,row7,row8,row9 )  
         elif action == 4 :   
            return encode_state( row1,row2,row3,row4,player,row6,row7,row8,row9 )  
         elif action == 5 :   
            return encode_state( row1,row2,row3,row4,row5,player,row7,row8,row9 ) 
         elif action == 6 :   
            return encode_state( row1,row2,row3,row4,row5,row6,player,row8,row9 )  
         elif action == 7 :   
            return encode_state( row1,row2,row3,row4,row5,row6,row7,player,row9 ) 
         elif action == 8 :   
            return encode_state( row1,row2,row3,row4,row5,row6,row7,row8,player )  
                                                       
      def getAllPossibleNextAction(self, state):
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
         #print('decode:',state,'  ::  ',row1,row2,row3,row4,row5,row6,row7,row8,row9)
         action = []
         if(row1 == 0):
            action.append(0)    
         if(row2 == 0):
            action.append(1)     
         if(row3 == 0):
            action.append(2)    
         if(row4 == 0):
            action.append(3)  
         if(row5 == 0):
            action.append(4)  
         if(row6 == 0):
            action.append(5)  
         if(row7 == 0):
            action.append(6)  
         if(row8 == 0):
            action.append(7)  
         if(row9 == 0):
            action.append(8)                                                                                 
         return(action)

      def win(self, win, state, next_state):
         self.debug(state)
         self.debug(next_state)
         win += 1
         print('win',win)
         return win

      def try_train(self):         
         discount      = 0.9
         learning_rate = 0.1                 
         #print(base_reward[0][0],base_reward[0])
         alpha = 0.1
         gamma = 0.6
         win   = 0
         for epocks in range(20000):
            state   = 0
            done    = False  
            player  = 1              
            oldA    = 0
            oldB    = 0
            while not done:   
               possible_actions = self.getAllPossibleNextAction(state) 
               if possible_actions :  
                  action = random.choice(possible_actions) # Explore action space                              
                  next_state = self.try_action(action, player, state)
                  reward, done = self.win_or_loss(next_state, player, base_reward)                  
                  #if done :
                  #   win = self.win(win, state, next_state)
                  if player == 1 :
                     player = 2                  
                     self.q_table[oldA][action] = self.q_table[oldA][action] + learning_rate * (reward + 
                        discount * max(self.q_table[next_state]) - self.q_table[oldA][action]) 
                     oldA = next_state   
                  else :
                     player = 1                   
                     self.q_table[oldB][action] = self.q_table[oldB][action] + learning_rate * (reward + 
                        discount * max(self.q_table[next_state]) - self.q_table[oldB][action])                      
                     oldB = next_state 

                  state = next_state                 
                  #end IF
               else: 
                  done = True

                  #self.debug(state)
                  #time.sleep(5)
               #end IF   
            #end While   
            print('epocks',epocks)
         #end FOR epocks
      #end Train
      def Play2(self, player, state, last_state):
         discount      = 0.9
         learning_rate = 0.1         
         possible_actions = self.getAllPossibleNextAction(state) 
         if possible_actions : 
            action = np.argmax( self.q_table[state] )
            next_state = self.try_action(action, player, state)
            reward, done = self.win_or_loss(next_state, player, base_reward) 
            self.q_table[last_state][action] = self.q_table[last_state][action] + learning_rate * (reward + 
                        discount * max(self.q_table[next_state]) - self.q_table[last_state][action])   

            if done == True :
               next_state = 0

            return next_state, done
         #end IF
         return 0, True   
      #end Play2

      def debug(self, state):
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
         print(row1,row2,row3)
         print(row4,row5,row6)
         print(row7,row8,row9)  
         print(self.q_table[state])      

      def play(self):
         state  = encode_state(1,0,0, 
                               2,1,0, 
                               2,1,2)
         self.debug(state)
         print('(1)',np.argmax( self.q_table[state] ) ,  self.q_table[state] )   

         state  = encode_state(0,0,0, 
                               0,0,1, 
                               0,2,1)
         self.debug(state)
         print('(2)',np.argmax( self.q_table[state] ) ,  self.q_table[state] )                  
                     

base_reward = [[0.01, 0, 0],[0.01, 50, 5],[0.01, 5, 50]]                     
world = World_base() 
world.try_train()
world.play()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle/<action>/<statePlayerB>/<statePlayerA>', methods=['POST','GET'])
def handle(action, statePlayerB, statePlayerA):
   statePlayerB  = int(statePlayerB)
   statePlayerA  = int(statePlayerA)
   action        = int(action)
   discount      = 0.9
   learning_rate = 0.1    
   my_state      = world.try_action(action, 1, statePlayerB)
   reward, done  = world.win_or_loss(my_state, 1, base_reward)

   world.q_table[statePlayerA][action] = world.q_table[statePlayerA][action] + learning_rate * (reward + 
               discount * max(world.q_table[my_state]) - world.q_table[statePlayerA][action])    

   if done == False :
      new_state, done = world.Play2(2, my_state, statePlayerB)
   else :
      new_state = 0   

   row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(new_state)

   ret = {
         "row1": row1,"re1":world.q_table[my_state][0],"pe1":world.q_table[new_state][0],
         "row2": row2,"re2":world.q_table[my_state][1],"pe2":world.q_table[new_state][1],
         "row3": row3,"re3":world.q_table[my_state][2],"pe3":world.q_table[new_state][2],
         "row4": row4,"re4":world.q_table[my_state][3],"pe4":world.q_table[new_state][3],
         "row5": row5,"re5":world.q_table[my_state][4],"pe5":world.q_table[new_state][4],
         "row6": row6,"re6":world.q_table[my_state][5],"pe6":world.q_table[new_state][5],
         "row7": row7,"re7":world.q_table[my_state][6],"pe7":world.q_table[new_state][6],
         "row8": row8,"re8":world.q_table[my_state][7],"pe8":world.q_table[new_state][7],
         "row9": row9,"re9":world.q_table[my_state][8],"pe9":world.q_table[new_state][8],
         "new_state":new_state,
         "my_state":my_state
   }
   return json.dumps(ret)

if __name__ == "__main__":
    app.run(debug=True)    

