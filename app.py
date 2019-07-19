from tools import encode_state,decode_state

print( encode_state( 1,0,0, 0,0,0, 0,0,0 )  )

a1, a2, a3, a4, a5, a6, a7, a8, a9 = decode_state(6561)

print( a1, a2, a3, a4, a5, a6, a7, a8, a9  )
