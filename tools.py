def encode_state(row1,row2,row3,row4,row5,row6,row7,row8,row9):    
    i = row1
    i *= 3
    i += row2
    i *= 3
    i += row3
    i *= 3
    i += row4
    i *= 3
    i += row5
    i *= 3
    i += row6
    i *= 3                                
    i += row7
    i *= 3
    i += row8
    i *= 3
    i += row9   
    #print('encode', i , row1,row2,row3,row4,row5,row6,row7,row8,row9)                 
    return i 

def decode_state(state):
    out = []
    out.append(state % 3)
    state = state // 3
    out.append(state % 3)
    state = state // 3
    out.append(state % 3)
    state = state // 3
    out.append(state % 3)
    state = state // 3
    out.append(state % 3)
    state = state // 3
    out.append(state % 3)        
    state = state // 3   
    out.append(state % 3)
    state = state // 3
    out.append(state % 3)
    state = state // 3
    out.append(state % 3)                                                   
    return reversed(out) 

def win_or_loss(state, player, base_reward): 
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

def try_action(action, player, state):
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
                                                
def getAllPossibleNextAction(state):
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

def getAllPossibleValues(q_table, arr):
    action = []
    if 0 in arr :
        action.append(q_table[0]) 
    if 1 in arr :
        action.append(q_table[1])  
    if 2 in arr :
        action.append(q_table[2]) 
    if 3 in arr :
        action.append(q_table[3]) 
    if 4 in arr :
        action.append(q_table[4]) 
    if 5 in arr :
        action.append(q_table[5]) 
    if 6 in arr :
        action.append(q_table[6]) 
    if 7 in arr :
        action.append(q_table[7]) 
    if 8 in arr :
        action.append(q_table[8]) 

    return(action)        