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