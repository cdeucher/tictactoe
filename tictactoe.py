import random, time
import numpy as np

from tools import encode_state,decode_state

class World_base:
      def __init__(self): 
         self.width = 500000 
         self.states= 9
         self.current_state = 0
         self.q_table = np.zeros([self.width, self.states])
         self.P = np.zeros([self.width, self.states])

      def set_q(self, state, actions, player):
         self.q_table[state, actions] = player
    
      def get_q(self, state):
         return self.q_table[state] 

      def win_or_loss(self, state, player, base_reward): 
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
         if row1 == player and row2 == player and row3 == player:
            return base_reward[player], True
         if row4 == player and row5 == player and row6 == player:
            return base_reward[player], True
         if row7 == player and row8 == player and row9 == player:
            return base_reward[player], True

         if row1 == player and row5 == player and row9 == player:
            return base_reward[player], True
         if row7 == player and row5 == player and row3 == player:
            return base_reward[player], True   

         return 0.1, False
      #end win_or_loss   

      def try_action(self, action, player):
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(self.current_state) 
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

      def update_state(self, next_state, action):
         self.P[self.current_state, action] = None                                                            

      def reward(self, action, next_state, reward):
         old_value = self.q_table[self.current_state, action]
         next_max = np.max(self.q_table[next_state])
         print(alpha,old_value,alpha,reward,gamma,next_max)
         new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
         self.q_table[self.current_state, action] = new_value
         print('state',self.current_state, 'action',action, 'new_value',new_value)

      def try_train(self):
         #for state in range(362800):
         #    row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(state)
         #    print(state, row1,row2,row3,row4,row5,row6,row7,row8,row9 )
         base_reward = [0, 1, -1]
         for epocks in range(1):
            penalties, reward, player, = 0, 0, 1
            self.current_state = encode_state(0,0,0, 0,player,0, 0,0,0)
            self.P = [1,2,3, 4,5,6, 7,8,9]  
            done = False     
            count = 0     
            while not done:   
               count += 1          
               if random.uniform(0, 1) < epsilon:   
                     sort = random.randint(9)                  
                     action = self.P[ self.current_state ]
                     print( 'action P ',self.P[ self.current_state ], action ) 
               else:
                     action = np.argmax( self.q_table[self.current_state] ) # Exploit learned values
                     print( 'action P --', self.P[ self.current_state, action]) 
                     if self.P[ self.current_state, action] > 0 :
                        print( 'action Q ', self.P[ self.current_state, action] , action )
                     else :
                        action = np.argmax( self.P[ self.current_state ] ) 
                        print( 'action P ',self.P[ self.current_state ], action )   

               next_state = self.try_action(action, player)
               reward, done = self.win_or_loss(self.current_state, player, base_reward)

               print( 'win_or_loss',reward, done, action )  

               self.reward(action, next_state, reward)

               self.update_state(next_state, action)
         
               self.current_state = next_state

               if player == 1 :
                  player = 2
               else:
                  player = 1

               self.debug()
               if next_state == 0:
                  done = True 

               time.sleep(1)
            #end While   
            print('epocks',epocks, 'count',count)
         #end FOR epocks
      #end Train

      def debug(self):
         row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(self.current_state)
         print(row1,row2,row3)
         print(row4,row5,row6)
         print(row7,row8,row9)        

         
                     
world = World_base() 

alpha = 0.1
gamma = 0.6
epsilon = 0.1            
world.try_train()

#tmp = encode_state(2,2,1, 1,2,1, 2,1,2)   
#row1,row2,row3,row4,row5,row6,row7,row8,row9 = decode_state(tmp)   
#print( row1,row2,row3,row4,row5,row6,row7,row8,row9 )
#tmp = encode_state( row1,row2,row3,row4,row5,row6,row7,row8,row9 ) 
#print( tmp ) 
#world.current_state = encode_state(0,0,0, 0,0,0, 0,0,0) 
#world.q_table[ world.current_state ] = (0.3,0.5,0.3, 0.5,0.7,0.3, 0.3,0.5,0.3 )

#action = np.argmax( world.q_table[ world.current_state ] )
#print(world.q_table[ world.current_state, action ])

