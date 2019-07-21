import random, time
import numpy as np
from tools import encode_state,decode_state, getAllPossibleNextAction, try_action, win_or_loss

#base_reward = [[0.01, 0, 0],[0.01, 50, 5],[0.01, 5, 50]]  ##modo defencivo 
base_reward = [[0.001, 0, 0],[0.001, 5, 10],[0.001, 10, 5]]  ##modo agrecivo  
state_playerB= 0
state_playerA= 0
IA_win       = [[0,0,0],[0,0,0],[0,0,0]]  

class oTrain:
      def __init__(self): 
         self.width = 20000
         self.states= 9
         self.q_table = np.zeros([self.width, self.states])
         self.current = 0
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
               possible_actions = getAllPossibleNextAction(state) 
               if possible_actions :  
                  #if random.uniform(0, 1) < 0.2:
                  #   action       = np.argmax( self.q_table[state] )
                  #else :
                  #   action       = random.choice(possible_actions) # Explore action space                              
                  action       = random.choice(possible_actions) # Explore action space                              

                  next_state   = try_action(action, player, state)
                  reward, done = win_or_loss(next_state, player, base_reward)                  

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
            #print(f"Epocks {epocks}")
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
         possible_actions = getAllPossibleNextAction(state) 
         if possible_actions : 
            action       = np.argmax( self.q_table[state] )
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