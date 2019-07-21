import random, time
import numpy as np
from tools import encode_state,decode_state, getAllPossibleNextAction, try_action, win_or_loss, getAllPossibleValues

#base_reward = [[0.01, 0, 0],[0.01, 50, 5],[0.01, 5, 50]]  ##modo defencivo 
base_reward = [[0, 0, 0],[0, 2, 100],[0, 100, 2]]  ##modo agrecivo  
state_playerB= 0
state_playerA= 0
IA_win       = [[0,0,0],[0,0,0],[0,0,0]]  

class oTrain:
      def __init__(self): 
         self.width = 20000
         self.states= 9
         self.q_table = np.zeros([self.width, self.states])
         self.action  = 0
         self.oldPlayer2 = 0
         self.count_win  = 0

      def try_train(self, number):         
         discount      = 0.9
         learning_rate = 0.1                 
         alpha = 0.1
         gamma = 0.6         
         for epocks in range(number):
            state   = 0
            done    = False  
            player  = 1              
            oldA    = 0
            oldB    = 0            
            while not done:   
               possible_steps   = np.full(9, -99) 
               possible_actions = getAllPossibleNextAction(state) 
               possible_steps   = getAllPossibleValues(self.q_table[state], possible_actions)
               if possible_steps :  
                  if random.uniform(0, 1) < 0.2:                     
                     action       = random.choice(possible_actions) # Explore action space   
                  else :
                     action       = possible_actions[ np.argmax( possible_steps ) ]                                               
                  #action       = random.choice(possible_actions) # Explore action space                              

                  next_state   = try_action(action, player, state)
                  reward, done = win_or_loss(next_state, player, base_reward)                  

                  old_value = self.q_table[state, action]
                  next_max = np.max(self.q_table[next_state])
                  new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)

                  if player == 1 :
                     player = 2                  
                     self.q_table[oldA][action] = new_value
                     oldA = next_state   
                  else :
                     player = 1                   
                     self.q_table[oldB][action] = new_value                    
                     oldB = next_state 

                  state = next_state                 
                  #end IF
               else: 
                  done = True
               #end IF   
            #end While  
            self.debug_win(epocks, possible_actions, state, reward)
         #end FOR epocks
      #end Train
      
      def save_train(self, file):
         np.savetxt(file, self.q_table)

      def read_train(self, file):
         data = np.loadtxt(file)
         self.q_table = data        

      def debug_win(self, epocks, possible_actions, state, reward):
         if reward > 0.01: 
            self.count_win += 1

         if epocks % 1000 == 0:
            #print('Win :', self.count_win , epocks) 
            print(f"Epocks {epocks} - Win: {self.count_win} - State: {state}")
            self.count_win = 0

      def Play2(self, player, state, last_state):
         state         = int(state)  
         last_state    = int(last_state)                 
         discount      = 0.9
         learning_rate = 0.1   
         possible_steps   = np.full(9, -99)  
         possible_actions = getAllPossibleNextAction(state) 
         #print('possible_actions',possible_actions)
         possible_steps   = getAllPossibleValues(self.q_table[state], possible_actions)
         if possible_steps :
            #print('possible_steps',possible_steps)
            action       = possible_actions[ np.argmax( possible_steps ) ]
            next_state   = try_action(action, player, state)
            reward, done = win_or_loss(next_state, player, base_reward) 

            self.q_table[last_state][action] = self.q_table[last_state][action] + learning_rate * (reward + 
                        discount * max(self.q_table[next_state]) - self.q_table[last_state][action])   
            return next_state, done
         #end IF
         return 0, False   
      #end Play2

      def Play1(self, action, state, last_state):
        state         = int(state)
        last_state    = int(last_state)
        action        = int(action)
        discount      = 0.9
        learning_rate = 0.1       
        new_state     = try_action(action, 1, state)
        reward, done  = win_or_loss(new_state, 1, base_reward)

        self.q_table[last_state][action] = self.q_table[last_state][action] + learning_rate * (reward + 
                    discount * max(self.q_table[new_state]) - self.q_table[last_state][action])            

        return new_state, IA_win, done           
      #end Play1

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

#if __name__ == "__main__":
#Train = oTrain()         