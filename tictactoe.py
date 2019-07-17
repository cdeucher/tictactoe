import random, time
import numpy as np

from tools import encode_state,decode_state

class World_base:
      def __init__(self): 
         self.width = 500000 
         self.states= 9
         self.q_table = np.zeros([self.width, self.states])

      def win_or_loss(self, state, player, base_reward): 
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
         if row1 == player and row2 == player and row3 == player:
            return base_reward[player], True
         if row4 == player and row5 == player and row6 == player:
            return base_reward[player], True
         if row7 == player and row8 == player and row9 == player:
            return base_reward[player], True

         if row1 == player and row4 == player and row7 == player:
            return base_reward[player], True
         if row2 == player and row5 == player and row8 == player:
            return base_reward[player], True
         if row3 == player and row6 == player and row9 == player:
            return base_reward[player], True                                    

         if row1 == player and row5 == player and row9 == player:
            return base_reward[player], True
         if row7 == player and row5 == player and row3 == player:
            return base_reward[player], True   

         return base_reward[0], False
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

      def try_train(self, player):
         discount      = 0.9
         learning_rate = 0.1         
         base_reward = [0.01, 100,10]
         for epocks in range(10000):
            state   = random.choice([0])
            #state   = encode_state(0,0,0, 0,player,0, 0,0,0)
            action  = random.choice([0,1,2, 3,4,5, 6,7,8])
            done    = False
            while not done:   
               possible_actions = self.getAllPossibleNextAction(state) 
               if possible_actions :  
                  action = random.choice(possible_actions)
                  next_state = self.try_action(action, player, state)

                  reward, done = self.win_or_loss(next_state, player, base_reward)

                  self.q_table[state][action] = self.q_table[state][action] + learning_rate * (reward + 
                        discount * max(self.q_table[next_state]) - self.q_table[state][action])

                  #print('player, state, action',player, state, action, self.q_table[state][action])    
                  state = next_state   
                  #if epocks > 300000:                                             
                  #   self.debug(state)
                  if player == 1 :
                     player = 2
                  else:
                     player = 1                      
               else: #end FOR
                  done = True
            #end While   
            print('epocks',epocks)
         #end FOR epocks
      #end Train

      def debug(self, state):
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
         print(row1,row2,row3)
         print(row4,row5,row6)
         print(row7,row8,row9)  
         #print(self.q_table[state])      

      def play(self):
         state  = encode_state(0,0,0, 0,0,0, 0,0,0)
         self.debug(state)
         print('(4)',np.argmax( self.q_table[state] ) , self.q_table[state] )

         state  = encode_state(1,0,2, 
                               0,1,0, 
                               0,0,2)
         self.debug(state)
         print('(5)',np.argmax( self.q_table[state] ) ,  self.q_table[state] )

         state  = encode_state(0,0,2, 
                               0,1,0, 
                               2,0,1)
         self.debug(state)
         print('(0)',np.argmax( self.q_table[state] ) ,  self.q_table[state] )      

         state  = encode_state(2,1,2, 
                               1,2,0, 
                               1,0,0)
         self.debug(state)
         print('(8)',np.argmax( self.q_table[state] ) ,  self.q_table[state] )    

         state  = encode_state(1,0,2, 
                               2,1,0, 
                               0,1,2)
         self.debug(state)
         print('(1)',np.argmax( self.q_table[state] ) ,  self.q_table[state] )           
                     
world = World_base() 

alpha = 0.1
gamma = 0.6
epsilon = 0.1            
world.try_train(1)
#world.try_train(2)
world.play()



